from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
import io
import pandas as pd

# Import our services
from services.data_processor import DataProcessor
from services.ai_analyzer import AIAnalyzer

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


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

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

    Args:
        file: CSV file upload.

    Returns:
        dict: Upload summary and initial data info.
    """
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