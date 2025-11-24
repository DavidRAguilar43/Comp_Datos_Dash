"""
AI-powered dataset structure analysis service.

This module analyzes CSV datasets to automatically detect column types,
suggest appropriate visualizations, and generate dynamic analysis configurations
for breast cancer datasets.
"""

import os
from typing import Dict, Any, List, Optional
import json
import pandas as pd
from openai import OpenAI


class DatasetStructureAnalyzer:
    """
    Analyzes dataset structure using AI to determine optimal visualizations
    and analysis strategies for breast cancer datasets.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the dataset structure analyzer.

        Args:
            api_key (str, optional): OpenAI API key. If not provided, reads from environment.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")

        # Check if using OpenRouter (API key starts with sk-or-v1-)
        if self.api_key.startswith('sk-or-v1-'):
            # Configure for OpenRouter
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            # Standard OpenAI configuration
            self.client = OpenAI(api_key=self.api_key)

        self.model = "gpt-4o"
    
    def analyze_dataset_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze dataset structure and recommend visualizations.
        
        Args:
            df (pd.DataFrame): The dataset to analyze.
            
        Returns:
            dict: Analysis results including column types, visualizations, and insights.
        """
        try:
            # Extract dataset metadata
            metadata = self._extract_metadata(df)
            
            # Build prompt for AI analysis
            prompt = self._build_structure_analysis_prompt(metadata)
            
            # Get AI recommendations
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto en análisis de datos médicos especializado en 
                        cáncer de mama. Tu tarea es analizar la estructura de datasets CSV y determinar:
                        1. El tipo de cada columna (numérica continua, categórica, binaria, fecha, etc.)
                        2. Qué visualizaciones son más apropiadas para cada variable
                        3. Qué análisis estadísticos son relevantes
                        4. Qué correlaciones deberían explorarse
                        
                        Responde SIEMPRE en formato JSON válido."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent JSON output
                max_tokens=1500,  # Reduced from 2000 to fit within credit limits
                response_format={"type": "json_object"}
            )
            
            # Parse AI response
            ai_analysis = json.loads(response.choices[0].message.content)
            
            # Enhance with automatic detection
            enhanced_analysis = self._enhance_with_auto_detection(df, ai_analysis)
            
            return {
                "success": True,
                "analysis": enhanced_analysis,
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_metadata(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract metadata from dataframe.
        
        Args:
            df (pd.DataFrame): The dataset.
            
        Returns:
            dict: Dataset metadata.
        """
        metadata = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": []
        }
        
        for col in df.columns:
            col_info = {
                "name": col,
                "dtype": str(df[col].dtype),
                "non_null_count": int(df[col].count()),
                "null_count": int(df[col].isnull().sum()),
                "unique_values": int(df[col].nunique()),
                "sample_values": df[col].dropna().head(5).tolist()
            }
            
            # Add statistics for numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info["statistics"] = {
                    "min": float(df[col].min()) if not df[col].isna().all() else None,
                    "max": float(df[col].max()) if not df[col].isna().all() else None,
                    "mean": float(df[col].mean()) if not df[col].isna().all() else None,
                    "median": float(df[col].median()) if not df[col].isna().all() else None
                }
            
            metadata["columns"].append(col_info)

        return metadata

    def _build_structure_analysis_prompt(self, metadata: Dict[str, Any]) -> str:
        """
        Build prompt for structure analysis.

        Args:
            metadata (dict): Dataset metadata.

        Returns:
            str: Formatted prompt.
        """
        prompt = f"""Analiza la siguiente estructura de un dataset de cáncer de mama:

Total de filas: {metadata['total_rows']}
Total de columnas: {metadata['total_columns']}

COLUMNAS:
{json.dumps(metadata['columns'], indent=2, ensure_ascii=False)}

Genera un análisis en formato JSON con la siguiente estructura:
{{
  "column_analysis": [
    {{
      "column_name": "nombre_columna",
      "detected_type": "numeric_continuous|numeric_discrete|categorical|binary|date|text",
      "is_target_variable": true/false,
      "description": "descripción breve de qué representa esta columna",
      "recommended_visualizations": ["tipo_grafica1", "tipo_grafica2"],
      "statistical_tests": ["test1", "test2"]
    }}
  ],
  "recommended_analyses": [
    {{
      "analysis_type": "correlation|distribution|comparison|trend",
      "variables": ["var1", "var2"],
      "visualization_type": "heatmap|scatter|bar|line|pie|box",
      "description": "qué insights puede revelar este análisis"
    }}
  ],
  "key_variables": {{
    "target": "nombre de la variable objetivo (diagnóstico/resultado)",
    "demographic": ["variables demográficas"],
    "clinical": ["variables clínicas"],
    "risk_factors": ["factores de riesgo identificados"]
  }},
  "data_quality_notes": [
    "observaciones sobre calidad de datos, valores faltantes, etc."
  ]
}}

IMPORTANTE:
- Identifica automáticamente cuál es la variable objetivo (diagnóstico de cáncer)
- Clasifica las variables en demográficas, clínicas y factores de riesgo
- Sugiere visualizaciones específicas para datasets de cáncer de mama
- Considera que los valores pueden estar en español o inglés"""

        return prompt

    def _enhance_with_auto_detection(
        self,
        df: pd.DataFrame,
        ai_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enhance AI analysis with automatic detection.

        Args:
            df (pd.DataFrame): The dataset.
            ai_analysis (dict): AI-generated analysis.

        Returns:
            dict: Enhanced analysis.
        """
        enhanced = ai_analysis.copy()

        # Add actual value distributions for categorical variables
        for col_analysis in enhanced.get("column_analysis", []):
            col_name = col_analysis["column_name"]

            if col_name in df.columns:
                # Add value counts for categorical/binary variables
                if col_analysis["detected_type"] in ["categorical", "binary"]:
                    value_counts = df[col_name].value_counts().to_dict()
                    col_analysis["value_distribution"] = {
                        str(k): int(v) for k, v in value_counts.items()
                    }

                # Add percentiles for numeric variables
                elif col_analysis["detected_type"] in ["numeric_continuous", "numeric_discrete"]:
                    if pd.api.types.is_numeric_dtype(df[col_name]):
                        col_analysis["percentiles"] = {
                            "p25": float(df[col_name].quantile(0.25)),
                            "p50": float(df[col_name].quantile(0.50)),
                            "p75": float(df[col_name].quantile(0.75))
                        }

        return enhanced

    def generate_visualization_config(
        self,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate visualization configuration based on analysis.

        Args:
            analysis (dict): Dataset analysis.

        Returns:
            dict: Visualization configuration for frontend.
        """
        config = {
            "summary_cards": [],
            "charts": [],
            "correlation_config": {
                "variables": [],
                "method": "pearson"
            }
        }

        # Generate summary cards
        key_vars = analysis.get("key_variables", {})
        target_var = key_vars.get("target")

        if target_var:
            config["summary_cards"].append({
                "type": "distribution",
                "variable": target_var,
                "title": "Distribución de Diagnóstico",
                "chart_type": "pie"
            })

        # Generate charts from recommended analyses
        for rec_analysis in analysis.get("recommended_analyses", []):
            chart_config = {
                "type": rec_analysis["analysis_type"],
                "variables": rec_analysis["variables"],
                "visualization": rec_analysis["visualization_type"],
                "title": rec_analysis["description"]
            }
            config["charts"].append(chart_config)

        # Configure correlation analysis
        numeric_vars = [
            col["column_name"]
            for col in analysis.get("column_analysis", [])
            if col["detected_type"] in ["numeric_continuous", "numeric_discrete"]
        ]
        config["correlation_config"]["variables"] = numeric_vars

        return config

