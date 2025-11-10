"""
AI-powered analysis service using OpenAI GPT-4.

This module provides automated insights and descriptive analysis
of breast cancer clinical data using GPT-4.
"""

import os
from typing import Dict, Any, List, Optional
import json
from openai import OpenAI


class AIAnalyzer:
    """
    Generates AI-powered insights from clinical data using GPT-4.
    
    Analyzes statistical patterns, correlations, and clinical trends
    to provide human-readable insights for medical professionals.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI analyzer.

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

        self.model = "gpt-4o"  # Using GPT-4o as specified
    
    def analyze_summary_statistics(self, summary_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights from summary statistics.
        
        Args:
            summary_stats (dict): Summary statistics from DataProcessor.
            
        Returns:
            dict: AI-generated insights and key findings.
        """
        try:
            prompt = self._build_summary_prompt(summary_stats)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto en epidemiología y análisis de datos médicos, 
                        especializado en factores de riesgo de cáncer de mama. Analiza los datos 
                        proporcionados y genera insights clínicos relevantes en español. 
                        Sé conciso, preciso y enfócate en hallazgos clínicamente significativos."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            insights = response.choices[0].message.content
            
            return {
                "success": True,
                "insights": insights,
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_correlations(self, correlations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights from correlation analysis.
        
        Args:
            correlations (dict): Correlation data from DataProcessor.
            
        Returns:
            dict: AI-generated interpretation of correlations.
        """
        try:
            prompt = self._build_correlation_prompt(correlations)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un bioestadístico experto en análisis de correlaciones 
                        en datos médicos. Interpreta las correlaciones encontradas en el contexto 
                        de factores de riesgo de cáncer de mama. Explica qué significan estas 
                        relaciones desde una perspectiva clínica y epidemiológica. Responde en español."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            insights = response.choices[0].message.content
            
            return {
                "success": True,
                "insights": insights,
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_clinical_report(
        self, 
        summary_stats: Dict[str, Any],
        correlations: Dict[str, Any],
        filters_applied: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive clinical report.
        
        Args:
            summary_stats (dict): Summary statistics.
            correlations (dict): Correlation analysis.
            filters_applied (dict, optional): Any filters applied to the data.
            
        Returns:
            dict: Comprehensive AI-generated clinical report.
        """
        try:
            prompt = self._build_report_prompt(summary_stats, correlations, filters_applied)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un oncólogo e investigador clínico especializado en 
                        cáncer de mama. Genera un reporte clínico profesional basado en los datos 
                        proporcionados. El reporte debe incluir:
                        1. Resumen ejecutivo de hallazgos principales
                        2. Análisis demográfico de la población
                        3. Factores de riesgo identificados
                        4. Patrones y tendencias observadas
                        5. Recomendaciones para investigación futura
                        
                        Usa lenguaje médico apropiado pero accesible. Responde en español."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            report = response.choices[0].message.content
            
            return {
                "success": True,
                "report": report,
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens,
                "filters_applied": filters_applied or {}
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_summary_prompt(self, summary_stats: Dict[str, Any]) -> str:
        """
        Build prompt for summary statistics analysis.
        
        Args:
            summary_stats (dict): Summary statistics.
            
        Returns:
            str: Formatted prompt.
        """
        prompt = f"""Analiza las siguientes estadísticas de un estudio sobre factores de riesgo 
de cáncer de mama en mujeres cubanas:

Total de registros: {summary_stats.get('total_records', 'N/A')}

Distribución de diagnóstico de cáncer:
{json.dumps(summary_stats.get('cancer_distribution', {}), indent=2, ensure_ascii=False)}

Estadísticas de edad:
{json.dumps(summary_stats.get('age_statistics', {}), indent=2, ensure_ascii=False)}

Variables categóricas principales:
{json.dumps(summary_stats.get('categorical_stats', {}), indent=2, ensure_ascii=False)}

Genera un análisis conciso destacando:
1. Principales hallazgos demográficos
2. Patrones en la distribución de casos
3. Observaciones clínicamente relevantes
4. Áreas que requieren mayor atención
"""
        return prompt
    
    def _build_correlation_prompt(self, correlations: Dict[str, Any]) -> str:
        """
        Build prompt for correlation analysis.
        
        Args:
            correlations (dict): Correlation data.
            
        Returns:
            str: Formatted prompt.
        """
        significant = correlations.get('significant_correlations', [])
        
        prompt = f"""Analiza las siguientes correlaciones significativas encontradas en un 
estudio de factores de riesgo de cáncer de mama:

Correlaciones significativas (|r| > 0.3):
{json.dumps(significant[:10], indent=2, ensure_ascii=False)}

Interpreta estas correlaciones desde una perspectiva clínica:
1. ¿Qué relaciones son esperadas y cuáles son sorprendentes?
2. ¿Qué implicaciones tienen para la comprensión del riesgo de cáncer de mama?
3. ¿Qué factores parecen estar más interrelacionados?
4. ¿Hay alguna correlación que sugiera causalidad o confusión?
"""
        return prompt
    
    def _build_report_prompt(
        self,
        summary_stats: Dict[str, Any],
        correlations: Dict[str, Any],
        filters_applied: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build prompt for comprehensive clinical report.
        
        Args:
            summary_stats (dict): Summary statistics.
            correlations (dict): Correlation data.
            filters_applied (dict, optional): Applied filters.
            
        Returns:
            str: Formatted prompt.
        """
        filter_info = ""
        if filters_applied:
            filter_info = f"\nFiltros aplicados: {json.dumps(filters_applied, indent=2, ensure_ascii=False)}"
        
        prompt = f"""Genera un reporte clínico completo basado en los siguientes datos de un 
estudio sobre factores de riesgo de cáncer de mama en mujeres cubanas:
{filter_info}

ESTADÍSTICAS GENERALES:
Total de casos: {summary_stats.get('total_records', 'N/A')}

Distribución de diagnóstico:
{json.dumps(summary_stats.get('cancer_distribution', {}), indent=2, ensure_ascii=False)}

Estadísticas de edad:
{json.dumps(summary_stats.get('age_statistics', {}), indent=2, ensure_ascii=False)}

CORRELACIONES SIGNIFICATIVAS:
{json.dumps(correlations.get('significant_correlations', [])[:10], indent=2, ensure_ascii=False)}

VARIABLES CATEGÓRICAS:
{json.dumps(summary_stats.get('categorical_stats', {}), indent=2, ensure_ascii=False)}

Genera un reporte estructurado y profesional que incluya:
1. Resumen ejecutivo (2-3 párrafos)
2. Perfil demográfico de la población estudiada
3. Análisis de factores de riesgo identificados
4. Patrones y tendencias observadas
5. Limitaciones del análisis
6. Recomendaciones para investigación futura

Usa formato markdown para mejor legibilidad.
"""
        return prompt

