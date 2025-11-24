from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from jose import JWTError, jwt
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone, timedelta
import io
import pandas as pd

# Import our services
from services.data_processor import DataProcessor
from services.ai_analyzer import AIAnalyzer
from services.dataset_structure_analyzer import DatasetStructureAnalyzer
from services.ml_models import MLModelsService
from services.auth import AuthService, UserCreate, UserLogin, Token, User

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL')
db_name = os.environ.get('DB_NAME', 'breast_cancer_dashboard')

# Initialize MongoDB client only if URL is provided
client = None
db = None
if mongo_url:
    try:
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        logging.info(f"MongoDB connected to database: {db_name}")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
else:
    logging.warning("MONGO_URL not set. MongoDB features will be disabled.")

# Create the main app without a prefix
app = FastAPI(
    title="Dashboard Clínico - Cáncer de Mama",
    description="API para análisis de factores de riesgo de cáncer de mama en mujeres cubanas",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize services
data_processor = DataProcessor()
ai_analyzer = None  # Will be initialized when API key is available
structure_analyzer = None  # Will be initialized when API key is available
ml_service = MLModelsService()
auth_service = AuthService(db)

# Security
security = HTTPBearer()
SECRET_KEY = os.environ.get("JWT_SECRET", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await auth_service.get_user(email=email)
    if user is None:
        raise credentials_exception

    return user


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@api_router.post("/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user.

    Args:
        user_data: User registration data (email, password, full_name)

    Returns:
        Token: JWT access token and user information

    Raises:
        HTTPException: If user already exists or database error
    """
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )

    # Check if user already exists
    existing_user = await auth_service.get_user(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = auth_service.get_password_hash(user_data.password)
    user_dict = {
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        await db.users.insert_one(user_dict)
        logger.info(f"New user registered: {user_data.email}")
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": user_data.email}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user={
            "email": user_data.email,
            "full_name": user_data.full_name
        }
    )


@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    Login with email and password.

    Args:
        user_credentials: User login credentials (email, password)

    Returns:
        Token: JWT access token and user information

    Raises:
        HTTPException: If credentials are invalid
    """
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )

    # Authenticate user
    user = await auth_service.authenticate_user(
        user_credentials.email,
        user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": user.email}
    )

    logger.info(f"User logged in: {user.email}")

    return Token(
        access_token=access_token,
        token_type="bearer",
        user={
            "email": user.email,
            "full_name": user.full_name
        }
    )


@api_router.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Args:
        current_user: Current authenticated user (from JWT token)

    Returns:
        dict: User information
    """
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active
    }


# ============================================================================
# PUBLIC ENDPOINTS
# ============================================================================

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)

    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])

    return status_checks


# ============================================================================
# DASHBOARD ENDPOINTS - Breast Cancer Data Analysis
# ============================================================================

@api_router.post("/data/upload")
async def upload_data(file: UploadFile = File(...)):
    """
    Upload and process CSV file with breast cancer data.
    Automatically analyzes dataset structure using AI.

    Args:
        file: CSV file upload.

    Returns:
        dict: Upload summary, cleaning info, and structure analysis.
    """
    global structure_analyzer

    try:
        # Read file content
        content = await file.read()

        # Load data
        result = data_processor.load_from_bytes(content, file.filename)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        # Auto-clean data
        clean_result = data_processor.clean_data()

        return {
            "success": True,
            "upload_info": result,
            "cleaning_info": clean_result
        }

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/data/summary")
async def get_data_summary(
    ageMin: int = None,
    ageMax: int = None,
    diagnosis: str = None,
    menopause: str = None,
    birads: str = None,
    breastfeeding: str = None
):
    """
    Get summary statistics of the loaded dataset with optional filters.

    Args:
        ageMin (int, optional): Minimum age filter
        ageMax (int, optional): Maximum age filter
        diagnosis (str, optional): Diagnosis filter ('all', 'Benigno', 'Maligno')
        menopause (str, optional): Menopause status filter
        birads (str, optional): BIRADS classification filter
        breastfeeding (str, optional): Breastfeeding history filter

    Returns:
        dict: Comprehensive statistical summary.
    """
    try:
        # Build filters dictionary
        filters = {}
        if ageMin is not None:
            filters['ageMin'] = ageMin
        if ageMax is not None:
            filters['ageMax'] = ageMax
        if diagnosis:
            filters['diagnosis'] = diagnosis
        if menopause:
            filters['menopause'] = menopause
        if birads:
            filters['birads'] = birads
        if breastfeeding:
            filters['breastfeeding'] = breastfeeding

        # Get summary with filters
        summary = data_processor.get_summary_statistics(filters if filters else None)

        if not summary.get("success"):
            raise HTTPException(status_code=400, detail=summary.get("error"))

        return summary

    except Exception as e:
        logger.error(f"Error getting summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/data/correlations")
async def get_correlations(method: str = "pearson"):
    """
    Get correlation analysis of numeric variables.

    Args:
        method: Correlation method (pearson, spearman, kendall).

    Returns:
        dict: Correlation matrix and significant correlations.
    """
    try:
        if method not in ["pearson", "spearman", "kendall"]:
            raise HTTPException(status_code=400, detail="Invalid correlation method")

        correlations = data_processor.get_correlations(method=method)

        if not correlations.get("success"):
            raise HTTPException(status_code=400, detail=correlations.get("error"))

        return correlations

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating correlations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/data/preview")
async def get_data_preview(n_rows: int = 10):
    """
    Get a preview of the dataset.

    Args:
        n_rows: Number of rows to return (default: 10).

    Returns:
        dict: Preview data.
    """
    try:
        preview = data_processor.get_data_preview(n_rows=n_rows)

        if not preview.get("success"):
            raise HTTPException(status_code=400, detail=preview.get("error"))

        return preview

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting preview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/data/quality")
async def get_data_quality():
    """
    Get comprehensive data quality report.

    Returns:
        dict: Data quality metrics including missing values, outliers,
              duplicates, and class balance.
    """
    try:
        quality_report = data_processor.get_data_quality_report()

        if not quality_report.get("success"):
            raise HTTPException(status_code=400, detail=quality_report.get("error"))

        return quality_report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting data quality report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/data/preparation-report")
async def get_preparation_report():
    """
    Get comprehensive data preparation report.

    Returns detailed information about all data preparation operations:
    - Missing data detection and imputation
    - Duplicate removal
    - Outlier detection
    - Type corrections
    - Transformations applied
    - Date formatting
    - Column renaming

    Returns:
        dict: Complete data preparation log with summary statistics.
    """
    try:
        preparation_report = data_processor.get_preparation_report()

        if not preparation_report.get("success"):
            raise HTTPException(status_code=400, detail=preparation_report.get("error"))

        return preparation_report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting preparation report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DYNAMIC ANALYSIS ENDPOINTS (AI-POWERED)
# ============================================================================

@api_router.get("/data/structure-analysis")
async def get_structure_analysis():
    """
    Get the AI-powered structure analysis of the current dataset.

    Returns:
        dict: Dataset structure analysis including column types and visualization recommendations.
    """
    global structure_analyzer

    try:
        if data_processor.df is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a CSV file first.")

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file."
            )

        try:
            if structure_analyzer is None:
                structure_analyzer = DatasetStructureAnalyzer(api_key=api_key)

            # Analyze structure
            analysis_result = structure_analyzer.analyze_dataset_structure(data_processor.df)

            if not analysis_result.get("success"):
                raise HTTPException(status_code=500, detail=analysis_result.get("error"))

            # Generate visualization config
            visualization_config = structure_analyzer.generate_visualization_config(
                analysis_result["analysis"]
            )

            return {
                "success": True,
                "analysis": analysis_result["analysis"],
                "visualization_config": visualization_config,
                "model_used": analysis_result.get("model_used"),
                "tokens_used": analysis_result.get("tokens_used")
            }

        except Exception as init_error:
            logger.error(f"Error in structure analysis: {str(init_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in structure analysis: {str(init_error)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting structure analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class DynamicSummaryRequest(BaseModel):
    column_analysis: List[Dict[str, Any]]
    filters: Optional[Dict[str, Any]] = None


@api_router.post("/data/dynamic-summary")
async def get_dynamic_summary(request: DynamicSummaryRequest):
    """
    Get dynamic summary statistics based on AI-detected column types.

    Args:
        request: Contains column_analysis from structure analyzer and optional filters.

    Returns:
        dict: Dynamic statistical summary.
    """
    try:
        if data_processor.df is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a CSV file first.")

        summary = data_processor.get_dynamic_summary_statistics(
            column_analysis=request.column_analysis,
            filters=request.filters
        )

        if not summary.get("success"):
            raise HTTPException(status_code=400, detail=summary.get("error"))

        return summary

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dynamic summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class DynamicCorrelationsRequest(BaseModel):
    column_analysis: List[Dict[str, Any]]
    method: str = "pearson"
    filters: Optional[Dict[str, Any]] = None


@api_router.post("/data/dynamic-correlations")
async def get_dynamic_correlations(request: DynamicCorrelationsRequest):
    """
    Get dynamic correlation analysis based on AI-detected numeric columns.

    Args:
        request: Contains column_analysis, correlation method, and optional filters.

    Returns:
        dict: Dynamic correlation analysis.
    """
    try:
        if data_processor.df is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a CSV file first.")

        if request.method not in ["pearson", "spearman", "kendall"]:
            raise HTTPException(status_code=400, detail="Invalid correlation method")

        correlations = data_processor.get_dynamic_correlations(
            column_analysis=request.column_analysis,
            method=request.method,
            filters=request.filters
        )

        if not correlations.get("success"):
            raise HTTPException(status_code=400, detail=correlations.get("error"))

        return correlations

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dynamic correlations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class RawDataRequest(BaseModel):
    variables: List[str]
    max_samples: int = 1000
    filters: Optional[Dict[str, Any]] = None


@api_router.post("/data/raw-data")
async def get_raw_data(request: RawDataRequest):
    """
    Get raw data samples for specific variables (for scatter plots, histograms, etc.).

    Args:
        request: Contains variables list, max_samples, and optional filters.

    Returns:
        dict: Raw data arrays for each variable.
    """
    try:
        if data_processor.df is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a CSV file first.")

        if not request.variables:
            raise HTTPException(status_code=400, detail="No variables specified")

        raw_data = data_processor.get_raw_data_sample(
            variables=request.variables,
            max_samples=request.max_samples,
            filters=request.filters
        )

        if not raw_data.get("success"):
            raise HTTPException(status_code=400, detail=raw_data.get("error"))

        return raw_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting raw data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AI INSIGHTS ENDPOINTS
# ============================================================================

@api_router.post("/ai/analyze-summary")
async def ai_analyze_summary():
    """
    Generate AI-powered insights from summary statistics.

    Returns:
        dict: AI-generated insights.
    """
    try:
        # Check if data is loaded
        if data_processor.df is None:
            raise HTTPException(
                status_code=400,
                detail="No data loaded. Please upload a CSV file first."
            )

        # Initialize AI analyzer if not already done
        global ai_analyzer
        if ai_analyzer is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(
                    status_code=500,
                    detail="OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file."
                )
            try:
                ai_analyzer = AIAnalyzer(api_key=api_key)
            except Exception as init_error:
                logger.error(f"Error initializing AI analyzer: {str(init_error)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error initializing AI analyzer: {str(init_error)}"
                )

        # Get summary statistics
        summary = data_processor.get_summary_statistics()
        if not summary.get("success"):
            error_msg = summary.get("error", "Unknown error getting summary")
            logger.error(f"Error getting summary: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        # Generate AI insights
        logger.info("Generating AI insights for summary statistics")
        insights = ai_analyzer.analyze_summary_statistics(summary)

        if not insights.get("success"):
            error_msg = insights.get("error", "Unknown error generating AI insights")
            logger.error(f"Error generating AI insights: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        logger.info("AI insights generated successfully")
        return insights

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in AI analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@api_router.post("/ai/analyze-correlations")
async def ai_analyze_correlations(method: str = "pearson"):
    """
    Generate AI-powered insights from correlation analysis.

    Args:
        method: Correlation method.

    Returns:
        dict: AI-generated correlation insights.
    """
    try:
        # Check if data is loaded
        if data_processor.df is None:
            raise HTTPException(
                status_code=400,
                detail="No data loaded. Please upload a CSV file first."
            )

        # Initialize AI analyzer if not already done
        global ai_analyzer
        if ai_analyzer is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(
                    status_code=500,
                    detail="OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file."
                )
            try:
                ai_analyzer = AIAnalyzer(api_key=api_key)
            except Exception as init_error:
                logger.error(f"Error initializing AI analyzer: {str(init_error)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error initializing AI analyzer: {str(init_error)}"
                )

        # Get correlations
        correlations = data_processor.get_correlations(method=method)
        if not correlations.get("success"):
            error_msg = correlations.get("error", "Unknown error getting correlations")
            logger.error(f"Error getting correlations: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        # Generate AI insights
        logger.info(f"Generating AI insights for correlations using method: {method}")
        insights = ai_analyzer.analyze_correlations(correlations)

        if not insights.get("success"):
            error_msg = insights.get("error", "Unknown error generating AI insights")
            logger.error(f"Error generating AI insights: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        logger.info("AI insights generated successfully")
        return insights

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in AI correlation analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@api_router.post("/ai/generate-report")
async def generate_clinical_report():
    """
    Generate comprehensive AI-powered clinical report.

    Returns:
        dict: Complete clinical report with insights.
    """
    try:
        # Check if data is loaded
        if data_processor.df is None:
            raise HTTPException(
                status_code=400,
                detail="No data loaded. Please upload a CSV file first."
            )

        # Initialize AI analyzer if not already done
        global ai_analyzer
        if ai_analyzer is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(
                    status_code=500,
                    detail="OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file."
                )
            try:
                ai_analyzer = AIAnalyzer(api_key=api_key)
            except Exception as init_error:
                logger.error(f"Error initializing AI analyzer: {str(init_error)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error initializing AI analyzer: {str(init_error)}"
                )

        # Get summary and correlations
        summary = data_processor.get_summary_statistics()
        correlations = data_processor.get_correlations()

        if not summary.get("success"):
            error_msg = summary.get("error", "Unknown error getting summary")
            logger.error(f"Error getting summary for report: {error_msg}")
            raise HTTPException(status_code=400, detail=f"Error getting summary: {error_msg}")

        if not correlations.get("success"):
            error_msg = correlations.get("error", "Unknown error getting correlations")
            logger.error(f"Error getting correlations for report: {error_msg}")
            raise HTTPException(status_code=400, detail=f"Error getting correlations: {error_msg}")

        # Generate report
        logger.info("Generating comprehensive clinical report")
        report = ai_analyzer.generate_clinical_report(summary, correlations)

        if not report.get("success"):
            error_msg = report.get("error", "Unknown error generating report")
            logger.error(f"Error generating report: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        logger.info("Clinical report generated successfully")
        return report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@api_router.post("/ai/analyze-model")
async def ai_analyze_model(model_data: dict):
    """
    Generate AI-powered insights from ML model performance.

    Args:
        model_data: Model performance data including metrics and confusion matrix.

    Returns:
        dict: AI-generated model analysis.
    """
    try:
        # Initialize AI analyzer if not already done
        global ai_analyzer
        if ai_analyzer is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(
                    status_code=500,
                    detail="OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file."
                )
            try:
                ai_analyzer = AIAnalyzer(api_key=api_key)
            except Exception as init_error:
                logger.error(f"Error initializing AI analyzer: {str(init_error)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error initializing AI analyzer: {str(init_error)}"
                )

        # Generate AI insights
        logger.info(f"Generating AI insights for model: {model_data.get('model_name', 'Unknown')}")
        insights = ai_analyzer.analyze_ml_model(model_data)

        if not insights.get("success"):
            error_msg = insights.get("error", "Unknown error generating AI insights")
            logger.error(f"Error generating AI insights: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        logger.info("AI model insights generated successfully")
        return insights

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in AI model analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@api_router.get("/data/export/{format}")
async def export_data(format: str):
    """
    Export processed data in various formats.

    Args:
        format: Export format (csv, json, excel).

    Returns:
        StreamingResponse: File download.
    """
    try:
        if format not in ["csv", "json", "excel"]:
            raise HTTPException(status_code=400, detail="Invalid export format")

        data_dict = data_processor.export_to_dict()
        if not data_dict.get("success"):
            raise HTTPException(status_code=400, detail=data_dict.get("error"))

        df = pd.DataFrame(data_dict["data"])

        if format == "csv":
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=breast_cancer_data.csv"}
            )

        elif format == "json":
            output = io.StringIO()
            df.to_json(output, orient="records", indent=2)
            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="application/json",
                headers={"Content-Disposition": "attachment; filename=breast_cancer_data.json"}
            )

        elif format == "excel":
            output = io.BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=breast_cancer_data.xlsx"}
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ML MODELS ENDPOINTS
# ============================================================================

@api_router.get("/ml/models")
async def get_ml_models():
    """
    Get information about available ML models.

    Returns:
        dict: Available models and their status.
    """
    try:
        return {
            "neural_network": {
                "name": "Red Neuronal",
                "description": "Modelo de Deep Learning con capas ocultas",
                "type": "classification",
                "trained": "neural_network" in ml_service.models
            },
            "random_forest": {
                "name": "Random Forest",
                "description": "Ensemble de árboles de decisión",
                "type": "classification",
                "trained": "random_forest" in ml_service.models
            },
            "svm": {
                "name": "Support Vector Machine",
                "description": "Clasificador basado en vectores de soporte",
                "type": "classification",
                "trained": "svm" in ml_service.models
            },
            "logistic_regression": {
                "name": "Regresión Logística",
                "description": "Modelo lineal de clasificación (baseline)",
                "type": "classification",
                "trained": "logistic_regression" in ml_service.models
            }
        }
    except Exception as e:
        logger.error(f"Error getting ML models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ml/train-all")
async def train_all_models():
    """
    Train all 4 ML models.

    Returns:
        dict: Training results for all models.
    """
    try:
        if data_processor.df is None:
            raise HTTPException(
                status_code=400,
                detail="No data loaded. Please upload a CSV file first."
            )

        # Prepare data
        prep_result = ml_service.prepare_data(data_processor.df)
        if not prep_result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=prep_result.get("error", "Error preparing data")
            )

        # Train all models
        results = ml_service.train_all_models()

        return {
            "success": True,
            "data_preparation": prep_result,
            "models": results
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error training models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ml/train/{model_name}")
async def train_single_model(model_name: str):
    """
    Train a single ML model.

    Args:
        model_name: Name of the model to train (neural_network, random_forest, svm, logistic_regression).

    Returns:
        dict: Training results.
    """
    try:
        if data_processor.df is None:
            raise HTTPException(
                status_code=400,
                detail="No data loaded. Please upload a CSV file first."
            )

        # Prepare data if not already prepared
        if ml_service.X_train is None:
            prep_result = ml_service.prepare_data(data_processor.df)
            if not prep_result.get("success"):
                raise HTTPException(
                    status_code=400,
                    detail=prep_result.get("error", "Error preparing data")
                )

        # Train specific model
        if model_name == "neural_network":
            result = ml_service.train_neural_network()
        elif model_name == "random_forest":
            result = ml_service.train_random_forest()
        elif model_name == "svm":
            result = ml_service.train_svm()
        elif model_name == "logistic_regression":
            result = ml_service.train_logistic_regression()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown model: {model_name}"
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error training model {model_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class PredictionRequest(BaseModel):
    """Request model for cancer prediction."""
    age: Optional[float] = None
    menarche: Optional[float] = None
    menopause: Optional[float] = None
    agefirst: Optional[float] = None
    children: Optional[float] = None
    biopsies: Optional[float] = None
    imc: Optional[float] = None
    weight: Optional[float] = None
    histologicalclass: Optional[float] = None
    model_name: str = "random_forest"


@api_router.post("/ml/predict")
async def predict_cancer(request: PredictionRequest):
    """
    Predict cancer probability for a single patient.

    Args:
        request: Patient data and model selection.

    Returns:
        dict: Prediction results with probability and risk level.
    """
    try:
        # Check if models are trained
        if not ml_service.models:
            raise HTTPException(
                status_code=400,
                detail="No models trained yet. Please train models first by going to the 'Modelos ML' tab."
            )

        # Convert request to dict
        input_data = request.model_dump(exclude={'model_name'})

        # Remove None values
        input_data = {k: v for k, v in input_data.items() if v is not None}

        # Make prediction
        result = ml_service.predict_single(input_data, model_name=request.model_name)

        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Error making prediction")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)