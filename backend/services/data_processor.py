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
        Clean the loaded dataset.
        
        Performs:
        - Duplicate removal
        - Missing value handling
        - Data type normalization
        - Text standardization
        
        Returns:
            dict: Cleaning report with statistics.
        """
        if self.df is None:
            return {"success": False, "error": "No data loaded"}
        
        initial_rows = len(self.df)
        
        # Remove duplicates
        duplicates_removed = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()
        
        # Handle missing values
        missing_before = self.df.isnull().sum().to_dict()
        
        # Normalize text values (Yes/No, Sí/No, etc.)
        text_columns = self.df.select_dtypes(include=['object']).columns
        for col in text_columns:
            if col in self.df.columns:
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
        
        missing_after = self.df.isnull().sum().to_dict()
        
        return {
            "success": True,
            "initial_rows": initial_rows,
            "final_rows": len(self.df),
            "duplicates_removed": int(duplicates_removed),
            "missing_values_before": {k: int(v) for k, v in missing_before.items() if v > 0},
            "missing_values_after": {k: int(v) for k, v in missing_after.items() if v > 0}
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

        # Age filter
        if filters.get('ageMin') is not None and filters.get('ageMax') is not None:
            if 'age' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['age'] >= filters['ageMin']) &
                    (filtered_df['age'] <= filters['ageMax'])
                ]

        # Diagnosis filter
        if filters.get('diagnosis') and filters['diagnosis'] != 'all':
            if 'cancer' in filtered_df.columns:
                # Map diagnosis to cancer values
                if filters['diagnosis'] == 'Maligno':
                    filtered_df = filtered_df[filtered_df['cancer'] == 'Yes']
                elif filters['diagnosis'] == 'Benigno':
                    filtered_df = filtered_df[filtered_df['cancer'] == 'No']

        # Menopause filter
        if filters.get('menopause') and filters['menopause'] != 'all':
            if 'menopause' in filtered_df.columns:
                # Check if menopause column has the value
                if filters['menopause'] == 'Premenopáusica':
                    filtered_df = filtered_df[filtered_df['menopause'] == 'No']
                elif filters['menopause'] == 'Posmenopáusica':
                    filtered_df = filtered_df[filtered_df['menopause'] != 'No']

        # BIRADS filter
        if filters.get('birads') and filters['birads'] != 'all':
            if 'birads' in filtered_df.columns:
                # Convert birads to string for comparison
                filtered_df = filtered_df[filtered_df['birads'].astype(str).str.startswith(filters['birads'])]

        # Breastfeeding filter
        if filters.get('breastfeeding') and filters['breastfeeding'] != 'all':
            if 'breastfeeding' in filtered_df.columns:
                if filters['breastfeeding'] == 'Sí':
                    filtered_df = filtered_df[filtered_df['breastfeeding'] != 'No']
                elif filters['breastfeeding'] == 'No':
                    filtered_df = filtered_df[filtered_df['breastfeeding'] == 'No']

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

            # 3. Outliers detection (for numeric columns using IQR method)
            outliers = {}
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                outlier_count = outlier_mask.sum()

                if outlier_count > 0:
                    outliers[col] = {
                        "count": int(outlier_count),
                        "percentage": round((outlier_count / total_rows) * 100, 2),
                        "lower_bound": float(lower_bound),
                        "upper_bound": float(upper_bound)
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

