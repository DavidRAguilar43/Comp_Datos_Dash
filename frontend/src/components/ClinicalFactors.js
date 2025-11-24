import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { AlertCircle, BarChart3, PieChart, Sparkles, Loader2 } from 'lucide-react';
import FilterPanel from './FilterPanel';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * ClinicalFactors component displays clinical variables analysis.
 *
 * Shows distribution and relationships of:
 * - BIRADS classification
 * - Menopause status
 * - Breastfeeding history
 * - Other clinical factors
 */
const ClinicalFactors = () => {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState(null);
  const [isFilteringData, setIsFilteringData] = useState(false);
  const [aiInsights, setAiInsights] = useState(null);
  const [loadingAI, setLoadingAI] = useState(false);
  const debounceTimerRef = useRef(null);

  // Reason: Memoize fetchSummary to prevent unnecessary re-renders
  const fetchSummary = useCallback(async (currentFilters, isInitialLoad = false) => {
    try {
      console.log('🔍 ClinicalFactors: fetchSummary called', { currentFilters, isInitialLoad });

      // Reason: Only show skeleton on initial load, not on filter changes
      if (isInitialLoad) {
        setLoading(true);
      } else {
        setIsFilteringData(true);
      }

      // Build query parameters from filters
      const params = new URLSearchParams();
      if (currentFilters) {
        if (currentFilters.ageMin !== undefined) params.append('ageMin', currentFilters.ageMin);
        if (currentFilters.ageMax !== undefined) params.append('ageMax', currentFilters.ageMax);
        if (currentFilters.diagnosis && currentFilters.diagnosis !== 'all') params.append('diagnosis', currentFilters.diagnosis);
        if (currentFilters.menopause && currentFilters.menopause !== 'all') params.append('menopause', currentFilters.menopause);
        if (currentFilters.birads && currentFilters.birads !== 'all') params.append('birads', currentFilters.birads);
        if (currentFilters.breastfeeding && currentFilters.breastfeeding !== 'all') params.append('breastfeeding', currentFilters.breastfeeding);
      }

      const url = `${API}/data/summary${params.toString() ? '?' + params.toString() : ''}`;
      console.log('📡 ClinicalFactors: Fetching URL:', url);

      const response = await axios.get(url);
      console.log('✅ ClinicalFactors: Response received', {
        total_records: response.data.total_records,
        filtered_records: response.data.filtered_records
      });

      setSummary(response.data);
      setError(null);
    } catch (err) {
      console.error('❌ ClinicalFactors: Error fetching summary', err);
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status
      });
      setError('Error al cargar datos clínicos: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
      setIsFilteringData(false);
    }
  }, []);

  // Reason: Memoize handleFilterChange to prevent FilterPanel re-renders
  const handleFilterChange = useCallback((newFilters) => {
    setFilters(newFilters);
  }, []);

  // Reason: Initial data load on component mount
  useEffect(() => {
    fetchSummary(null, true);
  }, [fetchSummary]);

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

  // Reason: Debounced filter changes to prevent excessive API calls
  useEffect(() => {
    if (filters !== null) {
      // Clear existing timer
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }

      // Set new timer for debounced API call
      debounceTimerRef.current = setTimeout(() => {
        fetchSummary(filters, false);
        // Reset AI insights when filters change
        setAiInsights(null);
      }, 300); // 300ms debounce delay

      // Cleanup function
      return () => {
        if (debounceTimerRef.current) {
          clearTimeout(debounceTimerRef.current);
        }
      };
    }
  }, [filters, fetchSummary]);

  if (loading) {
    return (
      <div className="space-y-6">
        {[1, 2].map((i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-6 w-48" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-64 w-full" />
            </CardContent>
          </Card>
        ))}
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

  // Check if no records match the filters
  if (summary && summary.filtered_records === 0) {
    return (
      <div className="space-y-6">
        <FilterPanel onFilterChange={handleFilterChange} summary={summary} />
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            No se encontraron registros que coincidan con los filtros seleccionados.
            Por favor, ajusta los filtros para ver los datos.
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  const categoricalStats = summary?.categorical_stats || {};

  // Helper function to create bar chart
  const createBarChart = (data, title, color = '#f472b6') => {
    if (!data || Object.keys(data).length === 0) {
      return null;
    }

    const sortedEntries = Object.entries(data)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10);

    return [{
      x: sortedEntries.map(([key]) => key),
      y: sortedEntries.map(([, value]) => value),
      type: 'bar',
      marker: {
        color: color,
        line: {
          color: color === '#f472b6' ? '#ec4899' : color,
          width: 1.5
        }
      },
      hovertemplate: '<b>%{x}</b><br>Casos: %{y}<extra></extra>',
    }];
  };

  // Helper function to create pie chart
  const createPieChart = (data, colors = ['#fda4af', '#93c5fd', '#86efac', '#fcd34d', '#c4b5fd']) => {
    if (!data || Object.keys(data).length === 0) {
      return null;
    }

    return [{
      values: Object.values(data),
      labels: Object.keys(data),
      type: 'pie',
      marker: { colors },
      textinfo: 'label+percent',
      textposition: 'inside',
      hovertemplate: '<b>%{label}</b><br>Casos: %{value}<br>%{percent}<extra></extra>',
    }];
  };

  const chartLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'Inter, system-ui, sans-serif' },
    margin: { t: 40, r: 20, b: 80, l: 60 },
  };

  return (
    <div className="space-y-6">
      {/* Filter Panel */}
      <FilterPanel onFilterChange={handleFilterChange} summary={summary} />

      {/* Loading indicator for filter changes */}
      {isFilteringData && (
        <Alert className="border-blue-200 bg-blue-50">
          <AlertDescription className="text-blue-800">
            🔄 Actualizando datos...
          </AlertDescription>
        </Alert>
      )}

      {/* Filter Status */}
      {summary && summary.filtered_records !== summary.original_records && (
        <Alert className="border-blue-200 bg-blue-50">
          <AlertDescription className="text-blue-800">
            📊 Mostrando <strong>{summary.filtered_records}</strong> de <strong>{summary.original_records}</strong> registros
            {summary.filtered_records < summary.original_records && (
              <span className="ml-2">
                ({Math.round((summary.filtered_records / summary.original_records) * 100)}% de los datos)
              </span>
            )}
          </AlertDescription>
        </Alert>
      )}

      {/* BIRADS Classification */}
      <Card className="border-pink-200">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-pink-600" />
            Clasificación BIRADS
          </CardTitle>
          <CardDescription>
            Distribución de casos según la clasificación BI-RADS (Breast Imaging Reporting and Data System)
          </CardDescription>
        </CardHeader>
        <CardContent>
          {categoricalStats.birads ? (
            <Plot
              data={createBarChart(categoricalStats.birads, 'BIRADS', '#f472b6')}
              layout={{
                ...chartLayout,
                xaxis: { title: 'Clasificación BIRADS' },
                yaxis: { title: 'Número de Casos' },
              }}
              config={{ displayModeBar: false, responsive: true }}
              style={{ width: '100%', height: '350px' }}
            />
          ) : (
            <p className="text-center text-gray-500 py-8">No hay datos de BIRADS disponibles</p>
          )}
        </CardContent>
      </Card>

      {/* Clinical Factors Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Menopause */}
        <Card className="border-blue-200">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <PieChart className="h-5 w-5 text-blue-600" />
              Estado de Menopausia
            </CardTitle>
            <CardDescription>
              Distribución según estado menopáusico
            </CardDescription>
          </CardHeader>
          <CardContent>
            {categoricalStats.menopause ? (
              <Plot
                data={createPieChart(categoricalStats.menopause, ['#93c5fd', '#fda4af', '#86efac'])}
                layout={{
                  ...chartLayout,
                  showlegend: true,
                  legend: { orientation: 'h', y: -0.2 },
                }}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: '100%', height: '300px' }}
              />
            ) : (
              <p className="text-center text-gray-500 py-8">No hay datos disponibles</p>
            )}
          </CardContent>
        </Card>

        {/* Breastfeeding */}
        <Card className="border-green-200">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <PieChart className="h-5 w-5 text-green-600" />
              Lactancia Materna
            </CardTitle>
            <CardDescription>
              Historial de lactancia materna
            </CardDescription>
          </CardHeader>
          <CardContent>
            {categoricalStats.breastfeeding ? (
              <Plot
                data={createPieChart(categoricalStats.breastfeeding, ['#86efac', '#fda4af', '#93c5fd', '#fcd34d'])}
                layout={{
                  ...chartLayout,
                  showlegend: true,
                  legend: { orientation: 'h', y: -0.2 },
                }}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: '100%', height: '300px' }}
              />
            ) : (
              <p className="text-center text-gray-500 py-8">No hay datos disponibles</p>
            )}
          </CardContent>
        </Card>

        {/* Race */}
        <Card className="border-purple-200">
          <CardHeader>
            <CardTitle className="text-lg">Distribución Étnica</CardTitle>
            <CardDescription>
              Casos según grupo étnico
            </CardDescription>
          </CardHeader>
          <CardContent>
            {categoricalStats.race ? (
              <Plot
                data={createBarChart(categoricalStats.race, 'Raza', '#c4b5fd')}
                layout={{
                  ...chartLayout,
                  xaxis: { title: 'Grupo Étnico' },
                  yaxis: { title: 'Número de Casos' },
                }}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: '100%', height: '300px' }}
              />
            ) : (
              <p className="text-center text-gray-500 py-8">No hay datos disponibles</p>
            )}
          </CardContent>
        </Card>

        {/* Histological Class */}
        <Card className="border-orange-200">
          <CardHeader>
            <CardTitle className="text-lg">Clase Histológica</CardTitle>
            <CardDescription>
              Distribución de clasificación histológica
            </CardDescription>
          </CardHeader>
          <CardContent>
            {categoricalStats.histologicalclass ? (
              <Plot
                data={createBarChart(categoricalStats.histologicalclass, 'Clase Histológica', '#fb923c')}
                layout={{
                  ...chartLayout,
                  xaxis: { title: 'Clase Histológica' },
                  yaxis: { title: 'Número de Casos' },
                }}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: '100%', height: '300px' }}
              />
            ) : (
              <p className="text-center text-gray-500 py-8">No hay datos disponibles</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Additional Factors */}
      <Card className="border-indigo-200">
        <CardHeader>
          <CardTitle className="text-lg">Factores de Riesgo Adicionales</CardTitle>
          <CardDescription>
            Distribución de otros factores clínicos relevantes
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="alcohol" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="alcohol">Alcohol</TabsTrigger>
              <TabsTrigger value="tobacco">Tabaco</TabsTrigger>
              <TabsTrigger value="exercise">Ejercicio</TabsTrigger>
              <TabsTrigger value="emotional">Estado Emocional</TabsTrigger>
            </TabsList>

            <TabsContent value="alcohol" className="mt-4">
              {categoricalStats.alcohol && (
                <Plot
                  data={createPieChart(categoricalStats.alcohol, ['#fda4af', '#93c5fd'])}
                  layout={{
                    ...chartLayout,
                    showlegend: true,
                    height: 300,
                  }}
                  config={{ displayModeBar: false, responsive: true }}
                  style={{ width: '100%', height: '300px' }}
                />
              )}
            </TabsContent>

            <TabsContent value="tobacco" className="mt-4">
              {categoricalStats.tobacco && (
                <Plot
                  data={createPieChart(categoricalStats.tobacco, ['#fda4af', '#93c5fd'])}
                  layout={{
                    ...chartLayout,
                    showlegend: true,
                    height: 300,
                  }}
                  config={{ displayModeBar: false, responsive: true }}
                  style={{ width: '100%', height: '300px' }}
                />
              )}
            </TabsContent>

            <TabsContent value="exercise" className="mt-4">
              {categoricalStats.exercise && (
                <Plot
                  data={createBarChart(categoricalStats.exercise, 'Ejercicio', '#86efac')}
                  layout={{
                    ...chartLayout,
                    xaxis: { title: 'Frecuencia de Ejercicio' },
                    yaxis: { title: 'Número de Casos' },
                    height: 300,
                  }}
                  config={{ displayModeBar: false, responsive: true }}
                  style={{ width: '100%', height: '300px' }}
                />
              )}
            </TabsContent>

            <TabsContent value="emotional" className="mt-4">
              {categoricalStats.emotional && (
                <Plot
                  data={createPieChart(categoricalStats.emotional, ['#fcd34d', '#fda4af', '#93c5fd'])}
                  layout={{
                    ...chartLayout,
                    showlegend: true,
                    height: 300,
                  }}
                  config={{ displayModeBar: false, responsive: true }}
                  style={{ width: '100%', height: '300px' }}
                />
              )}
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* AI Insights */}
      <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                Insights de Factores Clínicos con IA
              </CardTitle>
              <CardDescription>
                Análisis automático de patrones en factores clínicos y de riesgo
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
              Haga clic en "Generar Insights" para obtener un análisis automático de los factores clínicos
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ClinicalFactors;

