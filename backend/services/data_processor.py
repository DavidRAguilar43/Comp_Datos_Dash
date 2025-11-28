"""
Data processing service for breast cancer dataset.

This module handles CSV file processing, data cleaning, and statistical analysis
for the Cuban breast cancer risk factors dataset.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import io
from scipy import stats


class DataProcessor:
    """
    Processes and analyzes breast cancer clinical data.
    
    Handles data cleaning, validation, statistical analysis, and correlation
    calculations for medical datasets.
    """
    
    def __init__(self):
        """Initialize the data processor."""
        self.df: Optional[pd.DataFrame] = None
        self.original_df: Optional[pd.DataFrame] = None
        self.preparation_log: Dict[str, Any] = {
            "missing_data": {},
            "imputation": {},
            "duplicates": {},
            "outliers": {},
            "type_corrections": {},
            "transformations": [],
            "date_formatting": {},
            "column_renaming": {}
        }
        
    def load_from_bytes(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Load CSV data from bytes.
        
        Args:
            file_bytes (bytes): CSV file content as bytes.
            filename (str): Original filename.
            
        Returns:
            dict: Summary of loaded data including row count, columns, and data types.
        """
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
                try:
                    self.df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if self.df is None:
                raise ValueError("Could not decode file with any supported encoding")
            
            # Store original for reference
            self.original_df = self.df.copy()
            
            return {
                "success": True,
                "filename": filename,
                "rows": len(self.df),
                "columns": len(self.df.columns),
                "column_names": list(self.df.columns),
                "data_types": {col: str(dtype) for col, dtype in self.df.dtypes.items()}
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def clean_data(self) -> Dict[str, Any]:
        """
        Clean the loaded dataset with comprehensive logging.

        Performs:
        - Duplicate removal
        - Missing value detection and imputation
        - Data type normalization
        - Text standardization
        - Outlier detection and treatment

        Returns:
            dict: Cleaning report with statistics.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        # Reset transformation log to avoid duplicates
        self.preparation_log["transformations"] = []

        initial_rows = len(self.df)

        # 1. Detect missing values BEFORE any processing
        missing_before = {}
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                missing_before[col] = {
                    "count": int(missing_count),
                    "percentage": round((missing_count / initial_rows) * 100, 2)
                }
        self.preparation_log["missing_data"]["before"] = missing_before

        # 2. Remove duplicates
        duplicates_removed = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()
        self.preparation_log["duplicates"] = {
            "total_detected": int(duplicates_removed),
            "removed": int(duplicates_removed),
            "method": "drop_duplicates"
        }

        # 3. Impute missing values
        imputation_log = {}
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns

        # Impute numeric columns with mean
        for col in numeric_cols:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                mean_value = self.df[col].mean()
                self.df[col] = self.df[col].fillna(mean_value)
                imputation_log[col] = {
                    "values_imputed": int(missing_count),
                    "method": "mean",
                    "fill_value": float(mean_value)
                }

        # Impute categorical columns with mode
        for col in categorical_cols:
            # First, normalize text values
            self.df[col] = self.df[col].astype(str).str.strip()
            # Normalize Yes/No values
            self.df[col] = self.df[col].replace({
                'Sí': 'Yes',
                'Si': 'Yes',
                'sí': 'Yes',
                'si': 'Yes',
                'YES': 'Yes',
                'yes': 'Yes',
                'NO': 'No',
                'no': 'No',
                'nan': np.nan,
                'NaN': np.nan,
                'None': np.nan
            })

            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                mode_values = self.df[col].mode()
                if len(mode_values) > 0:
                    mode_value = mode_values[0]
                    self.df[col] = self.df[col].fillna(mode_value)
                    imputation_log[col] = {
                        "values_imputed": int(missing_count),
                        "method": "mode",
                        "fill_value": str(mode_value)
                    }

        self.preparation_log["imputation"] = imputation_log

        # 4. Detect and log outliers (no processing, just logging for reference)
        # Reason: We don't remove outliers in clinical data, just flag them
        outliers_log = {}
        # Note: Outlier detection is done in get_quality_summary() for reporting
        # Here we just initialize an empty log since we don't process outliers
        self.preparation_log["outliers"] = outliers_log

        # 5. Missing values AFTER processing
        missing_after = {}
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                missing_after[col] = {
                    "count": int(missing_count),
                    "percentage": round((missing_count / len(self.df)) * 100, 2)
                }
        self.preparation_log["missing_data"]["after"] = missing_after

        # Log text standardization
        self.preparation_log["transformations"].append({
            "operation": "text_standardization",
            "columns_affected": list(categorical_cols),
            "description": "Trimmed whitespace and normalized Yes/No values"
        })

        return {
            "success": True,
            "initial_rows": initial_rows,
            "final_rows": len(self.df),
            "duplicates_removed": int(duplicates_removed),
            "missing_values_before": {k: int(v["count"]) for k, v in missing_before.items()},
            "missing_values_after": {k: int(v["count"]) for k, v in missing_after.items()}
        }
    
    def apply_filters(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply filters to the dataset.

        Args:
            filters (dict): Dictionary containing filter criteria:
                - ageMin (int): Minimum age
                - ageMax (int): Maximum age
                - diagnosis (str): Diagnosis filter ('all', 'Benigno', 'Maligno')
                - menopause (str): Menopause status filter
                - birads (str): BIRADS classification filter
                - breastfeeding (str): Breastfeeding history filter

        Returns:
            pd.DataFrame: Filtered dataframe
        """
        if self.df is None:
            return None

        filtered_df = self.df.copy()
        initial_count = len(filtered_df)
        print(f"DEBUG: Starting with {initial_count} records")
        print(f"DEBUG: Filters received: {filters}")

        # Age filter
        if filters.get('ageMin') is not None and filters.get('ageMax') is not None:
            if 'age' in filtered_df.columns:
                before_count = len(filtered_df)
                filtered_df = filtered_df[
                    (filtered_df['age'] >= filters['ageMin']) &
                    (filtered_df['age'] <= filters['ageMax'])
                ]
                after_count = len(filtered_df)
                print(f"DEBUG: Age filter ({filters['ageMin']}-{filters['ageMax']}): {before_count} -> {after_count} records")

        # Diagnosis filter
        if filters.get('diagnosis') and filters['diagnosis'] != 'all':
            if 'cancer' in filtered_df.columns:
                # Map diagnosis to cancer values
                try:
                    before_count = len(filtered_df)
                    print(f"DEBUG: Unique cancer values: {filtered_df['cancer'].unique()}")
                    if filters['diagnosis'] == 'Maligno':
                        filtered_df = filtered_df[filtered_df['cancer'] == 'Yes']
                    elif filters['diagnosis'] == 'Benigno':
                        filtered_df = filtered_df[filtered_df['cancer'] == 'No']
                    after_count = len(filtered_df)
                    print(f"DEBUG: Diagnosis filter ({filters['diagnosis']}): {before_count} -> {after_count} records")
                except Exception as e:
                    print(f"Warning: Error applying diagnosis filter: {e}")

        # Menopause filter
        if filters.get('menopause') and filters['menopause'] != 'all':
            if 'menopause' in filtered_df.columns:
                # Check if menopause column has the value
                try:
                    before_count = len(filtered_df)
                    print(f"DEBUG: Unique menopause values (first 20): {filtered_df['menopause'].unique()[:20]}")
                    print(f"DEBUG: Menopause column dtype: {filtered_df['menopause'].dtype}")

                    # Convert to string for consistent comparison
                    menopause_str = filtered_df['menopause'].astype(str).str.strip()

                    if filters['menopause'] == 'Premenopáusica':
                        # Premenopause = "No" value
                        filtered_df = filtered_df[menopause_str == 'No']
                    elif filters['menopause'] == 'Posmenopáusica':
                        # Postmenopause = any value that is NOT "No" (numbers indicating menopause age)
                        filtered_df = filtered_df[menopause_str != 'No']

                    after_count = len(filtered_df)
                    print(f"DEBUG: Menopause filter ({filters['menopause']}): {before_count} -> {after_count} records")
                except Exception as e:
                    print(f"Warning: Error applying menopause filter: {e}")
                    import traceback
                    traceback.print_exc()

        # BIRADS filter
        if filters.get('birads') and filters['birads'] != 'all':
            if 'birads' in filtered_df.columns:
                try:
                    before_count = len(filtered_df)
                    print(f"DEBUG: Unique BIRADS values: {filtered_df['birads'].unique()}")
                    print(f"DEBUG: BIRADS filter value: '{filters['birads']}'")
                    # Convert birads to string and check if it starts with the filter value
                    # Handle both numeric (1, 2, 3) and alphanumeric (3A, 3B, 4C) BIRADS values
                    birads_str = filtered_df['birads'].astype(str).str.strip()
                    # Filter by BIRADS number (e.g., "3" matches "3", "3A", "3B", "3C")
                    filtered_df = filtered_df[birads_str.str.startswith(str(filters['birads']))]
                    after_count = len(filtered_df)
                    print(f"DEBUG: BIRADS filter ({filters['birads']}): {before_count} -> {after_count} records")
                except Exception as e:
                    print(f"Warning: Error applying BIRADS filter: {e}")
                    import traceback
                    traceback.print_exc()

        # Breastfeeding filter
        if filters.get('breastfeeding') and filters['breastfeeding'] != 'all':
            if 'breastfeeding' in filtered_df.columns:
                try:
                    before_count = len(filtered_df)
                    print(f"DEBUG: Unique breastfeeding values: {filtered_df['breastfeeding'].unique()}")
                    if filters['breastfeeding'] == 'Sí':
                        filtered_df = filtered_df[filtered_df['breastfeeding'] != 'No']
                    elif filters['breastfeeding'] == 'No':
                        filtered_df = filtered_df[filtered_df['breastfeeding'] == 'No']
                    after_count = len(filtered_df)
                    print(f"DEBUG: Breastfeeding filter ({filters['breastfeeding']}): {before_count} -> {after_count} records")
                except Exception as e:
                    print(f"Warning: Error applying breastfeeding filter: {e}")

        final_count = len(filtered_df)
        print(f"DEBUG: Final filtered records: {final_count} (from {initial_count})")

        return filtered_df

    def get_summary_statistics(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate summary statistics for the dataset.

        Args:
            filters (dict, optional): Filter criteria to apply before calculating statistics

        Returns:
            dict: Comprehensive statistical summary including:
                - Descriptive statistics for numeric columns
                - Frequency distributions for categorical columns
                - Cancer diagnosis distribution
                - Age statistics
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        # Apply filters if provided
        df_to_analyze = self.apply_filters(filters) if filters else self.df

        # Check if filtered dataset is empty
        if len(df_to_analyze) == 0:
            return {
                "success": True,
                "total_records": 0,
                "filtered_records": 0,
                "original_records": len(self.df),
                "numeric_stats": {},
                "categorical_stats": {},
                "cancer_distribution": {},
                "age_statistics": {},
                "message": "No records match the selected filters"
            }

        summary = {
            "success": True,
            "total_records": len(df_to_analyze),
            "filtered_records": len(df_to_analyze),
            "original_records": len(self.df),
            "numeric_stats": {},
            "categorical_stats": {},
            "cancer_distribution": {},
            "age_statistics": {}
        }

        # Numeric columns statistics
        numeric_cols = df_to_analyze.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            summary["numeric_stats"][col] = {
                "mean": float(df_to_analyze[col].mean()) if not pd.isna(df_to_analyze[col].mean()) else None,
                "median": float(df_to_analyze[col].median()) if not pd.isna(df_to_analyze[col].median()) else None,
                "std": float(df_to_analyze[col].std()) if not pd.isna(df_to_analyze[col].std()) else None,
                "min": float(df_to_analyze[col].min()) if not pd.isna(df_to_analyze[col].min()) else None,
                "max": float(df_to_analyze[col].max()) if not pd.isna(df_to_analyze[col].max()) else None,
                "q25": float(df_to_analyze[col].quantile(0.25)) if not pd.isna(df_to_analyze[col].quantile(0.25)) else None,
                "q75": float(df_to_analyze[col].quantile(0.75)) if not pd.isna(df_to_analyze[col].quantile(0.75)) else None
            }

        # Categorical columns frequency
        categorical_cols = df_to_analyze.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            value_counts = df_to_analyze[col].value_counts().head(10).to_dict()
            summary["categorical_stats"][col] = {
                str(k): int(v) for k, v in value_counts.items()
            }

        # Force histologicalclass to be treated as categorical even if numeric
        if 'histologicalclass' in df_to_analyze.columns and 'histologicalclass' not in summary["categorical_stats"]:
            value_counts = df_to_analyze['histologicalclass'].value_counts().head(10).to_dict()
            summary["categorical_stats"]['histologicalclass'] = {
                str(k): int(v) for k, v in value_counts.items()
            }

        # Cancer diagnosis distribution
        if 'cancer' in df_to_analyze.columns:
            cancer_counts = df_to_analyze['cancer'].value_counts().to_dict()
            total = len(df_to_analyze)
            summary["cancer_distribution"] = {
                "counts": {str(k): int(v) for k, v in cancer_counts.items()},
                "percentages": {str(k): round(float(v) / total * 100, 2) for k, v in cancer_counts.items()}
            }

        # Age-specific statistics
        if 'age' in df_to_analyze.columns:
            summary["age_statistics"] = {
                "mean_age": float(df_to_analyze['age'].mean()),
                "median_age": float(df_to_analyze['age'].median()),
                "age_range": {
                    "min": int(df_to_analyze['age'].min()),
                    "max": int(df_to_analyze['age'].max())
                },
                "age_groups": self._get_age_groups(df_to_analyze)
            }

        return summary

    def _get_age_groups(self, df: pd.DataFrame = None) -> Dict[str, int]:
        """
        Categorize patients into age groups.

        Args:
            df (pd.DataFrame, optional): Dataframe to analyze. Uses self.df if None.

        Returns:
            dict: Count of patients in each age group.
        """
        df_to_use = df if df is not None else self.df

        if 'age' not in df_to_use.columns:
            return {}

        bins = [0, 30, 40, 50, 60, 100]
        labels = ['<30', '30-39', '40-49', '50-59', '60+']

        age_groups = pd.cut(df_to_use['age'], bins=bins, labels=labels, right=False)
        counts = age_groups.value_counts().to_dict()

        return {str(k): int(v) for k, v in counts.items()}
    
    def get_correlations(self, method: str = 'pearson') -> Dict[str, Any]:
        """
        Calculate correlations between numeric variables.
        
        Args:
            method (str): Correlation method ('pearson', 'spearman', 'kendall').
            
        Returns:
            dict: Correlation matrix and significant correlations.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}
        
        # Select only numeric columns
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {"success": False, "error": "No numeric columns found"}
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr(method=method)
        
        # Convert to serializable format
        corr_dict = {}
        for col in corr_matrix.columns:
            corr_dict[col] = {
                row: float(corr_matrix.loc[row, col]) 
                for row in corr_matrix.index
                if not pd.isna(corr_matrix.loc[row, col])
            }
        
        # Find significant correlations (|r| > 0.3, excluding diagonal)
        significant = []
        for i, col1 in enumerate(corr_matrix.columns):
            for j, col2 in enumerate(corr_matrix.columns):
                if i < j:  # Avoid duplicates and diagonal
                    corr_value = corr_matrix.loc[col1, col2]
                    if not pd.isna(corr_value) and abs(corr_value) > 0.3:
                        significant.append({
                            "variable1": col1,
                            "variable2": col2,
                            "correlation": float(corr_value),
                            "strength": self._correlation_strength(abs(corr_value))
                        })
        
        # Sort by absolute correlation value
        significant.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            "success": True,
            "method": method,
            "correlation_matrix": corr_dict,
            "significant_correlations": significant
        }
    
    def _correlation_strength(self, abs_corr: float) -> str:
        """
        Classify correlation strength.

        Args:
            abs_corr (float): Absolute correlation value.

        Returns:
            str: Strength classification.
        """
        if abs_corr >= 0.7:
            return "strong"
        elif abs_corr >= 0.5:
            return "moderate"
        elif abs_corr >= 0.3:
            return "weak"
        else:
            return "very weak"

    def get_data_quality_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive data quality report.

        Returns:
            dict: Data quality metrics including missing values, outliers,
                  duplicates, and class balance.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        try:
            # 1. Missing values analysis
            missing_values = {}
            total_rows = len(self.df)
            for col in self.df.columns:
                missing_count = self.df[col].isnull().sum()
                if missing_count > 0:
                    missing_values[col] = {
                        "count": int(missing_count),
                        "percentage": round((missing_count / total_rows) * 100, 2)
                    }

            # 2. Duplicates analysis
            duplicates_count = int(self.df.duplicated().sum())
            duplicates_percentage = round((duplicates_count / total_rows) * 100, 2)

            # 3. Outliers detection (using percentiles and clinical ranges)
            # Reason: Percentiles are more robust for clinical data with non-normal distributions
            outliers = {}
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns

            # Define clinical ranges for specific variables
            # Reason: Clinical data has known valid ranges based on medical knowledge
            clinical_ranges = {
                'age': (18, 90),      # Valid age range for adult patients
                'imc': (15, 50),      # Valid BMI range (extreme underweight to extreme obesity)
                'weight': (40, 150)   # Valid weight range in kg
            }

            for col in numeric_cols:
                # Skip if all values are the same
                if self.df[col].nunique() <= 1:
                    continue

                # Determine bounds based on clinical ranges or percentiles
                if col in clinical_ranges:
                    # Use predefined clinical ranges
                    lower_bound, upper_bound = clinical_ranges[col]
                    method = f"Clinical range ({lower_bound}-{upper_bound})"
                else:
                    # Use percentiles (1% and 99%) for other numeric variables
                    lower_bound = self.df[col].quantile(0.01)
                    upper_bound = self.df[col].quantile(0.99)
                    method = "Percentiles (1%-99%)"

                # Detect outliers outside the bounds
                outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                outlier_count = outlier_mask.sum()

                if outlier_count > 0:
                    outliers[col] = {
                        "count": int(outlier_count),
                        "percentage": round((outlier_count / total_rows) * 100, 2),
                        "lower_bound": float(lower_bound),
                        "upper_bound": float(upper_bound),
                        "method": method
                    }

            # 4. Class balance (for categorical columns)
            class_balance = {}
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                value_counts = self.df[col].value_counts()
                total_valid = value_counts.sum()
                class_balance[col] = {
                    str(k): {
                        "count": int(v),
                        "percentage": round((v / total_valid) * 100, 2)
                    }
                    for k, v in value_counts.items()
                }

            # 5. Data types summary
            data_types = {
                "numeric": list(numeric_cols),
                "categorical": list(categorical_cols),
                "total_columns": len(self.df.columns)
            }

            # 6. Basic statistics
            basic_stats = {
                "total_rows": total_rows,
                "total_columns": len(self.df.columns),
                "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            }

            # 7. Inconsistencies (example: check for unexpected values)
            inconsistencies = []

            # Check for negative ages if 'age' column exists
            if 'age' in self.df.columns:
                negative_ages = (self.df['age'] < 0).sum()
                if negative_ages > 0:
                    inconsistencies.append({
                        "column": "age",
                        "issue": "negative_values",
                        "count": int(negative_ages)
                    })

            return {
                "success": True,
                "basic_stats": basic_stats,
                "missing_values": missing_values,
                "duplicates": {
                    "count": duplicates_count,
                    "percentage": duplicates_percentage
                },
                "outliers": outliers,
                "class_balance": class_balance,
                "data_types": data_types,
                "inconsistencies": inconsistencies
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_data_preview(self, n_rows: int = 10) -> Dict[str, Any]:
        """
        Get a preview of the dataset.
        
        Args:
            n_rows (int): Number of rows to return.
            
        Returns:
            dict: Preview data with column info.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}
        
        preview_df = self.df.head(n_rows)
        
        return {
            "success": True,
            "rows": preview_df.to_dict(orient='records'),
            "columns": list(self.df.columns),
            "total_rows": len(self.df)
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """
        Export entire dataset as dictionary.

        Returns:
            dict: Complete dataset.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        return {
            "success": True,
            "data": self.df.to_dict(orient='records'),
            "columns": list(self.df.columns),
            "total_rows": len(self.df)
        }

    def apply_type_corrections(self) -> Dict[str, Any]:
        """
        Detect and correct data type inconsistencies.

        Returns:
            dict: Type correction report.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        type_corrections = {}

        for col in self.df.columns:
            original_type = str(self.df[col].dtype)

            # Try to convert string columns that look like numbers
            if self.df[col].dtype == 'object':
                # Remove common symbols from numeric strings
                sample = self.df[col].dropna().head(100)

                # Check if values look like numbers with symbols
                if sample.astype(str).str.match(r'^[\$\€\£]?[\d,\.]+$').any():
                    try:
                        # Clean and convert
                        cleaned = self.df[col].astype(str).str.replace(r'[\$\€\£,]', '', regex=True)
                        self.df[col] = pd.to_numeric(cleaned, errors='coerce')

                        if str(self.df[col].dtype) != original_type:
                            type_corrections[col] = {
                                "original_type": original_type,
                                "new_type": str(self.df[col].dtype),
                                "reason": "Numeric values stored as text with symbols"
                            }
                    except:
                        pass

                # Check if values look like dates
                elif sample.astype(str).str.match(r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}').any():
                    try:
                        self.df[col] = pd.to_datetime(self.df[col], errors='coerce')

                        if str(self.df[col].dtype) != original_type:
                            type_corrections[col] = {
                                "original_type": original_type,
                                "new_type": str(self.df[col].dtype),
                                "reason": "Date values stored as text"
                            }
                    except:
                        pass

        self.preparation_log["type_corrections"] = type_corrections

        if type_corrections:
            self.preparation_log["transformations"].append({
                "operation": "type_correction",
                "columns_affected": list(type_corrections.keys()),
                "description": "Corrected data types for better analysis"
            })

        return {
            "success": True,
            "corrections": type_corrections
        }

    def standardize_date_formats(self, date_format: str = "%Y-%m-%d") -> Dict[str, Any]:
        """
        Standardize all date columns to a consistent format.

        Args:
            date_format (str): Target date format (default: YYYY-MM-DD).

        Returns:
            dict: Date formatting report.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        date_formatting = {}

        # Find datetime columns
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns

        for col in datetime_cols:
            # Convert to string with specified format
            original_sample = str(self.df[col].iloc[0]) if len(self.df) > 0 else "N/A"
            self.df[col] = self.df[col].dt.strftime(date_format)

            date_formatting[col] = {
                "format_applied": date_format,
                "example_before": original_sample,
                "example_after": str(self.df[col].iloc[0]) if len(self.df) > 0 else "N/A"
            }

        self.preparation_log["date_formatting"] = date_formatting

        if date_formatting:
            self.preparation_log["transformations"].append({
                "operation": "date_standardization",
                "columns_affected": list(datetime_cols),
                "description": f"Standardized date format to {date_format}"
            })

        return {
            "success": True,
            "formatted_columns": date_formatting
        }

    def rename_columns_for_clarity(self, rename_map: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Rename columns for better clarity and consistency.

        Args:
            rename_map (dict, optional): Dictionary mapping old names to new names.
                                        If None, applies automatic cleaning.

        Returns:
            dict: Column renaming report.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        renaming_log = {}

        if rename_map:
            # Use provided mapping
            self.df.rename(columns=rename_map, inplace=True)
            renaming_log = {old: new for old, new in rename_map.items() if old in self.df.columns or new in self.df.columns}
        else:
            # Automatic cleaning: lowercase, replace spaces with underscores
            new_columns = {}
            for col in self.df.columns:
                new_name = col.lower().strip().replace(' ', '_').replace('-', '_')
                if new_name != col:
                    new_columns[col] = new_name

            if new_columns:
                self.df.rename(columns=new_columns, inplace=True)
                renaming_log = new_columns

        self.preparation_log["column_renaming"] = renaming_log

        if renaming_log:
            self.preparation_log["transformations"].append({
                "operation": "column_renaming",
                "columns_affected": list(renaming_log.keys()),
                "description": "Renamed columns for clarity and consistency"
            })

        return {
            "success": True,
            "renamed_columns": renaming_log
        }

    def get_preparation_report(self) -> Dict[str, Any]:
        """
        Get comprehensive data preparation report.

        Returns:
            dict: Complete log of all data preparation operations performed.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        return {
            "success": True,
            "report": self.preparation_log,
            "summary": {
                "total_transformations": len(self.preparation_log["transformations"]),
                "columns_with_missing_data_before": len(self.preparation_log["missing_data"].get("before", {})),
                "columns_with_missing_data_after": len(self.preparation_log["missing_data"].get("after", {})),
                "columns_imputed": len(self.preparation_log["imputation"]),
                "duplicates_removed": self.preparation_log["duplicates"].get("removed", 0),
                "columns_with_outliers": len(self.preparation_log["outliers"]),
                "type_corrections_made": len(self.preparation_log["type_corrections"]),
                "columns_renamed": len(self.preparation_log["column_renaming"])
            }
        }

    def get_dynamic_summary_statistics(
        self,
        column_analysis: List[Dict[str, Any]],
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate summary statistics dynamically based on detected column types.

        Args:
            column_analysis (list): Column analysis from DatasetStructureAnalyzer.
            filters (dict, optional): Filter criteria to apply.

        Returns:
            dict: Dynamic statistical summary based on detected structure.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        # Apply filters if provided
        df_to_analyze = self.apply_filters(filters) if filters else self.df

        summary = {
            "success": True,
            "total_records": len(df_to_analyze),
            "numeric_stats": {},
            "categorical_stats": {},
            "binary_stats": {},
            "target_variable": None
        }

        # Process each column based on detected type
        for col_info in column_analysis:
            col_name = col_info["column_name"]
            col_type = col_info["detected_type"]

            if col_name not in df_to_analyze.columns:
                continue

            # Handle target variable
            if col_info.get("is_target_variable", False):
                summary["target_variable"] = {
                    "name": col_name,
                    "distribution": df_to_analyze[col_name].value_counts().to_dict()
                }

            # Handle numeric columns
            if col_type in ["numeric_continuous", "numeric_discrete"]:
                if pd.api.types.is_numeric_dtype(df_to_analyze[col_name]):
                    summary["numeric_stats"][col_name] = {
                        "mean": float(df_to_analyze[col_name].mean()),
                        "median": float(df_to_analyze[col_name].median()),
                        "std": float(df_to_analyze[col_name].std()),
                        "min": float(df_to_analyze[col_name].min()),
                        "max": float(df_to_analyze[col_name].max()),
                        "q25": float(df_to_analyze[col_name].quantile(0.25)),
                        "q75": float(df_to_analyze[col_name].quantile(0.75))
                    }

            # Handle categorical columns
            elif col_type == "categorical":
                value_counts = df_to_analyze[col_name].value_counts()
                summary["categorical_stats"][col_name] = {
                    "unique_values": int(df_to_analyze[col_name].nunique()),
                    "distribution": value_counts.to_dict(),
                    "top_value": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                    "top_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
                }

            # Handle binary columns
            elif col_type == "binary":
                value_counts = df_to_analyze[col_name].value_counts()
                summary["binary_stats"][col_name] = {
                    "distribution": value_counts.to_dict(),
                    "positive_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                    "negative_count": int(value_counts.iloc[1]) if len(value_counts) > 1 else 0
                }

        return summary

    def get_dynamic_correlations(
        self,
        column_analysis: List[Dict[str, Any]],
        method: str = 'pearson',
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate correlations dynamically based on detected numeric columns.

        Args:
            column_analysis (list): Column analysis from DatasetStructureAnalyzer.
            method (str): Correlation method ('pearson', 'spearman', 'kendall').
            filters (dict, optional): Filter criteria to apply.

        Returns:
            dict: Dynamic correlation analysis.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        # Apply filters if provided
        df_to_analyze = self.apply_filters(filters) if filters else self.df

        # Extract numeric columns from analysis
        numeric_cols = [
            col_info["column_name"]
            for col_info in column_analysis
            if col_info["detected_type"] in ["numeric_continuous", "numeric_discrete"]
            and col_info["column_name"] in df_to_analyze.columns
        ]

        if len(numeric_cols) < 2:
            return {
                "success": False,
                "error": "Not enough numeric columns for correlation analysis"
            }

        # Calculate correlations using existing method
        return self.get_correlations(method=method, filters=filters)

    def get_raw_data_sample(
        self,
        variables: List[str],
        max_samples: int = 1000,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get raw data samples for specific variables (for scatter plots, histograms, etc.).

        Args:
            variables (list): List of variable names to retrieve.
            max_samples (int): Maximum number of samples to return (default: 1000).
            filters (dict, optional): Filter criteria to apply.

        Returns:
            dict: Raw data arrays for each variable.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}

        # Apply filters if provided
        df_to_analyze = self.apply_filters(filters) if filters else self.df

        if len(df_to_analyze) == 0:
            return {
                "success": True,
                "total_records": 0,
                "sampled_records": 0,
                "data": {}
            }

        # Sample data if dataset is too large
        if len(df_to_analyze) > max_samples:
            df_sample = df_to_analyze.sample(n=max_samples, random_state=42)
        else:
            df_sample = df_to_analyze

        # Extract data for requested variables
        raw_data = {}
        for variable in variables:
            if variable in df_sample.columns:
                # Convert to list, handling NaN values
                values = df_sample[variable].dropna().tolist()
                raw_data[variable] = values

        return {
            "success": True,
            "total_records": len(df_to_analyze),
            "sampled_records": len(df_sample),
            "data": raw_data
        }

