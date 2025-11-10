import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import Plot from 'react-plotly.js';
import axios from 'axios';
import { Network, Sparkles, Loader2, AlertCircle, TrendingUp, TrendingDown } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * CorrelationsView component displays correlation analysis.
 *
 * Shows:
 * - Correlation heatmap
 * - Significant correlations list
 * - AI-generated correlation insights
 */
const CorrelationsView = () => {
  const [loading, setLoading] = useState(true);
  const [correlations, setCorrelations] = useState(null);
  const [method, setMethod] = useState('pearson');
  const [aiInsights, setAiInsights] = useState(null);
  const [loadingAI, setLoadingAI] = useState(false);
  const [error, setError] = useState(null);
  const [isChangingMethod, setIsChangingMethod] = useState(false);
  const isInitialMount = useRef(true);

  // Reason: Memoize fetchCorrelations to prevent unnecessary re-renders
  const fetchCorrelations = useCallback(async (isInitialLoad = false) => {
    try {
      // Reason: Only show skeleton on initial load, not on method changes
      if (isInitialLoad) {
        setLoading(true);
      } else {
        setIsChangingMethod(true);
      }

      const response = await axios.get(`${API}/data/correlations?method=${method}`);
      setCorrelations(response.data);
      setError(null);
    } catch (err) {
      setError('Error al cargar correlaciones');
      console.error(err);
    } finally {
      setLoading(false);
      setIsChangingMethod(false);
    }
  }, [method]);

  // Reason: Initial data load and method changes
  useEffect(() => {
    if (isInitialMount.current) {
      fetchCorrelations(true);
      isInitialMount.current = false;
    } else {
      fetchCorrelations(false);
    }
  }, [fetchCorrelations]);

  const fetchAIInsights = async () => {
    try {
      setLoadingAI(true);
      const response = await axios.post(`${API}/ai/analyze-correlations?method=${method}`);
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
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-48" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-96 w-full" />
          </CardContent>
        </Card>
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

  const corrMatrix = correlations?.correlation_matrix || {};
  const significantCorrs = correlations?.significant_correlations || [];

  // Prepare heatmap data
  const variables = Object.keys(corrMatrix);
  const zValues = variables.map(var1 => 
    variables.map(var2 => corrMatrix[var1]?.[var2] || 0)
  );

  const heatmapData = [{
    z: zValues,
    x: variables,
    y: variables,
    type: 'heatmap',
    colorscale: [
      [0, '#3b82f6'],      // Blue for negative
      [0.5, '#ffffff'],    // White for zero
      [1, '#f43f5e']       // Pink/Red for positive
    ],
    zmid: 0,
    zmin: -1,
    zmax: 1,
    hovertemplate: '<b>%{y} vs %{x}</b><br>Correlación: %{z:.3f}<extra></extra>',
    colorbar: {
      title: 'Correlación',
      titleside: 'right',
    }
  }];

  const heatmapLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'Inter, system-ui, sans-serif', size: 10 },
    margin: { t: 80, r: 100, b: 120, l: 120 },
    xaxis: { 
      tickangle: -45,
      side: 'bottom'
    },
    yaxis: {
      autorange: 'reversed'
    },
  };

  const getStrengthColor = (strength) => {
    const colors = {
      'strong': 'bg-red-100 text-red-800 border-red-300',
      'moderate': 'bg-orange-100 text-orange-800 border-orange-300',
      'weak': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      'very weak': 'bg-gray-100 text-gray-800 border-gray-300',
    };
    return colors[strength] || colors['very weak'];
  };

  return (
    <div className="space-y-6">
      {/* Controls */}
      <Card className="border-purple-200">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg">Método de Correlación</CardTitle>
              <CardDescription>
                Seleccione el método estadístico para calcular correlaciones
              </CardDescription>
            </div>
            <Select value={method} onValueChange={setMethod}>
              <SelectTrigger className="w-[180px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="pearson">Pearson</SelectItem>
                <SelectItem value="spearman">Spearman</SelectItem>
                <SelectItem value="kendall">Kendall</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
      </Card>

      {/* Loading indicator for method changes */}
      {isChangingMethod && (
        <Alert className="border-purple-200 bg-purple-50">
          <AlertDescription className="text-purple-800">
            🔄 Recalculando correlaciones con método {method}...
          </AlertDescription>
        </Alert>
      )}

      {/* Heatmap */}
      <Card className="border-pink-200">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Network className="h-5 w-5 text-pink-600" />
            Mapa de Calor de Correlaciones
          </CardTitle>
          <CardDescription>
            Matriz de correlaciones entre variables numéricas (método: {method})
          </CardDescription>
        </CardHeader>
        <CardContent>
          {variables.length > 0 ? (
            <div className="overflow-x-auto">
              <Plot
                data={heatmapData}
                layout={heatmapLayout}
                config={{ displayModeBar: true, responsive: true }}
                style={{ width: '100%', height: '600px' }}
              />
            </div>
          ) : (
            <p className="text-center text-gray-500 py-8">No hay datos de correlación disponibles</p>
          )}
        </CardContent>
      </Card>

      {/* Significant Correlations */}
      <Card className="border-blue-200">
        <CardHeader>
          <CardTitle className="text-lg">Correlaciones Significativas</CardTitle>
          <CardDescription>
            Pares de variables con correlación |r| &gt; 0.3
          </CardDescription>
        </CardHeader>
        <CardContent>
          {significantCorrs.length > 0 ? (
            <div className="space-y-3">
              {significantCorrs.map((corr, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 rounded-lg border bg-gradient-to-r from-white to-gray-50 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center gap-3 flex-1">
                    {corr.correlation > 0 ? (
                      <TrendingUp className="h-5 w-5 text-green-600" />
                    ) : (
                      <TrendingDown className="h-5 w-5 text-red-600" />
                    )}
                    <div>
                      <p className="font-semibold text-gray-800">
                        {corr.variable1} ↔ {corr.variable2}
                      </p>
                      <p className="text-sm text-gray-600">
                        Correlación: {corr.correlation.toFixed(3)}
                      </p>
                    </div>
                  </div>
                  <Badge 
                    variant="outline" 
                    className={getStrengthColor(corr.strength)}
                  >
                    {corr.strength}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-500 py-8">
              No se encontraron correlaciones significativas
            </p>
          )}
        </CardContent>
      </Card>

      {/* AI Insights */}
      <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                Interpretación de Correlaciones con IA
              </CardTitle>
              <CardDescription>
                Análisis automático del significado clínico de las correlaciones
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
                    Analizando...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
                    Interpretar con IA
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
              Haga clic en "Interpretar con IA" para obtener un análisis de las correlaciones
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CorrelationsView;

