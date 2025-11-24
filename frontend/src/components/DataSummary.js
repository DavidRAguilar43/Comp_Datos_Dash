import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { Users, Activity, TrendingUp, Sparkles, Loader2, AlertCircle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * DataSummary component displays general statistics and AI insights.
 *
 * Shows:
 * - Key metrics cards (based on dataset)
 * - Distribution charts (static based on dataset structure)
 * - AI-generated insights
 */
const DataSummary = () => {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [aiInsights, setAiInsights] = useState(null);
  const [loadingAI, setLoadingAI] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/data/summary`);
      setSummary(response.data);
      setError(null);
    } catch (err) {
      setError('Error al cargar el resumen de datos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAIInsights = async () => {
    try {
      setLoadingAI(true);
      const response = await axios.post(`${API}/ai/analyze-summary`);
      setAiInsights(response.data);
    } catch (err) {
      console.error('Error fetching AI insights:', err);
      setAiInsights({
        success: false,
        error: 'Error al generar insights con IA. Verifique la configuración de OpenAI API.'
      });
    } finally {
      setLoadingAI(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-4 w-24" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-8 w-16" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  const cancerDist = summary?.cancer_distribution || {};
  const ageStats = summary?.age_statistics || {};

  // Prepare cancer distribution chart
  const cancerChartData = cancerDist.counts ? [{
    values: Object.values(cancerDist.counts),
    labels: Object.keys(cancerDist.counts),
    type: 'pie',
    marker: {
      colors: ['#fda4af', '#93c5fd', '#86efac'],
    },
    textinfo: 'label+percent',
    textposition: 'inside',
    hovertemplate: '<b>%{label}</b><br>Casos: %{value}<br>Porcentaje: %{percent}<extra></extra>',
  }] : [];

  // Prepare age distribution chart
  const ageGroupsData = ageStats.age_groups ? [{
    x: Object.keys(ageStats.age_groups),
    y: Object.values(ageStats.age_groups),
    type: 'bar',
    marker: {
      color: '#f472b6',
      line: {
        color: '#ec4899',
        width: 1.5
      }
    },
    hovertemplate: '<b>Grupo: %{x}</b><br>Pacientes: %{y}<extra></extra>',
  }] : [];

  // Prepare BIRADS distribution chart (or menopause if BIRADS not available)
  const categoricalStats = summary?.categorical_stats || {};
  let thirdChartData = [];
  let thirdChartTitle = '';
  let thirdChartDescription = '';

  if (categoricalStats['birads']) {
    thirdChartData = [{
      values: Object.values(categoricalStats['birads']),
      labels: Object.keys(categoricalStats['birads']),
      type: 'pie',
      marker: {
        colors: ['#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa'],
      },
      textinfo: 'label+percent',
      textposition: 'inside',
      hovertemplate: '<b>%{label}</b><br>Casos: %{value}<br>Porcentaje: %{percent}<extra></extra>',
    }];
    thirdChartTitle = 'Distribución BIRADS';
    thirdChartDescription = 'Clasificación de hallazgos mamográficos';
  } else if (categoricalStats['menopause']) {
    thirdChartData = [{
      values: Object.values(categoricalStats['menopause']),
      labels: Object.keys(categoricalStats['menopause']),
      type: 'pie',
      marker: {
        colors: ['#60a5fa', '#f87171', '#fbbf24'],
      },
      textinfo: 'label+percent',
      textposition: 'inside',
      hovertemplate: '<b>%{label}</b><br>Casos: %{value}<br>Porcentaje: %{percent}<extra></extra>',
    }];
    thirdChartTitle = 'Distribución por Menopausia';
    thirdChartDescription = 'Estado menopáusico de las pacientes';
  } else if (categoricalStats['breastfeeding']) {
    thirdChartData = [{
      values: Object.values(categoricalStats['breastfeeding']),
      labels: Object.keys(categoricalStats['breastfeeding']),
      type: 'pie',
      marker: {
        colors: ['#60a5fa', '#f87171'],
      },
      textinfo: 'label+percent',
      textposition: 'inside',
      hovertemplate: '<b>%{label}</b><br>Casos: %{value}<br>Porcentaje: %{percent}<extra></extra>',
    }];
    thirdChartTitle = 'Historial de Lactancia';
    thirdChartDescription = 'Distribución de pacientes por historial de lactancia';
  }

  const chartLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'Inter, system-ui, sans-serif' },
    margin: { t: 40, r: 20, b: 40, l: 40 },
  };

  return (
    <div className="space-y-6">

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border-pink-200 bg-gradient-to-br from-pink-50 to-white">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">
              Total de Registros
            </CardTitle>
            <Users className="h-4 w-4 text-pink-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-pink-700">
              {summary?.total_records?.toLocaleString() || 0}
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Pacientes en el estudio
            </p>
          </CardContent>
        </Card>

        {/* Static metric cards */}
        <Card className="border-blue-200 bg-gradient-to-br from-blue-50 to-white">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-700">
                  Edad Promedio
                </CardTitle>
                <Activity className="h-4 w-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-blue-700">
                  {ageStats.mean_age?.toFixed(1) || 'N/A'}
                </div>
                <p className="text-xs text-gray-600 mt-1">
                  Rango: {ageStats.age_range?.min || 'N/A'} - {ageStats.age_range?.max || 'N/A'} años
                </p>
              </CardContent>
            </Card>

            <Card className="border-green-200 bg-gradient-to-br from-green-50 to-white">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-700">
                  Casos Positivos
                </CardTitle>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-green-700">
                  {cancerDist.percentages?.Yes?.toFixed(1) || 'N/A'}%
                </div>
                <p className="text-xs text-gray-600 mt-1">
                  {cancerDist.counts?.Yes?.toLocaleString() || 0} pacientes
                </p>
              </CardContent>
            </Card>
      </div>

      {/* Charts - Static based on dataset */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="border-pink-200">
            <CardHeader>
              <CardTitle className="text-lg">Distribución de Diagnóstico</CardTitle>
              <CardDescription>
                Proporción de casos positivos y negativos
              </CardDescription>
            </CardHeader>
            <CardContent>
              {cancerChartData.length > 0 ? (
                <Plot
                  data={cancerChartData}
                  layout={{
                    ...chartLayout,
                    showlegend: true,
                    legend: { orientation: 'h', y: -0.1 },
                  }}
                  config={{ displayModeBar: false, responsive: true }}
                  style={{ width: '100%', height: '300px' }}
                />
              ) : (
                <p className="text-center text-gray-500">No hay datos disponibles</p>
              )}
            </CardContent>
          </Card>

          <Card className="border-blue-200">
            <CardHeader>
              <CardTitle className="text-lg">Distribución por Edad</CardTitle>
              <CardDescription>
                Número de pacientes por grupo etario
              </CardDescription>
            </CardHeader>
            <CardContent>
              {ageGroupsData.length > 0 ? (
                <Plot
                  data={ageGroupsData}
                  layout={{
                    ...chartLayout,
                    xaxis: { title: 'Grupo de Edad' },
                    yaxis: { title: 'Número de Pacientes' },
                  }}
                  config={{ displayModeBar: false, responsive: true }}
                  style={{ width: '100%', height: '300px' }}
                />
              ) : (
                <p className="text-center text-gray-500">No hay datos disponibles</p>
              )}
            </CardContent>
          </Card>

          {thirdChartData.length > 0 && (
            <Card className="border-green-200">
              <CardHeader>
                <CardTitle className="text-lg">{thirdChartTitle}</CardTitle>
                <CardDescription>
                  {thirdChartDescription}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Plot
                  data={thirdChartData}
                  layout={{
                    ...chartLayout,
                    showlegend: true,
                    legend: { orientation: 'h', y: -0.1 },
                  }}
                  config={{ displayModeBar: false, responsive: true }}
                  style={{ width: '100%', height: '300px' }}
                />
              </CardContent>
            </Card>
          )}
      </div>

      {/* AI Insights */}
      <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                Insights Generados por IA
              </CardTitle>
              <CardDescription>
                Análisis automático de patrones y hallazgos clave
              </CardDescription>
            </div>
            {!aiInsights && (
              <Button
                onClick={fetchAIInsights}
                disabled={loadingAI}
                className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
              >
                {loadingAI ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generando...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
                    Generar Insights
                  </>
                )}
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {aiInsights ? (
            aiInsights.success ? (
              <div className="prose prose-sm max-w-none">
                <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                  {aiInsights.insights}
                </div>
                <div className="mt-4 flex items-center gap-2">
                  <Badge variant="outline" className="text-xs">
                    Modelo: {aiInsights.model_used}
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    Tokens: {aiInsights.tokens_used}
                  </Badge>
                </div>
              </div>
            ) : (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{aiInsights.error}</AlertDescription>
              </Alert>
            )
          ) : (
            <p className="text-gray-500 text-center py-8">
              Haga clic en "Generar Insights" para obtener un análisis automático de los datos
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default DataSummary;

