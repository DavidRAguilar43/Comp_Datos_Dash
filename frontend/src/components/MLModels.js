import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import axios from 'axios';
import { Brain, Zap, Target, TrendingUp, AlertCircle, CheckCircle2, Loader2, BarChart3, ArrowLeft, Eye, Sparkles } from 'lucide-react';
import Plot from 'react-plotly.js';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * MLModels component for training and comparing machine learning models.
 * 
 * Implements 4 classification models:
 * - Neural Network (Deep Learning)
 * - Random Forest (Ensemble)
 * - Support Vector Machine (SVM)
 * - Logistic Regression (Baseline)
 */
const MLModels = () => {
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState(null);
  const [trainingResults, setTrainingResults] = useState(null);
  const [error, setError] = useState(null);
  const [trainingModel, setTrainingModel] = useState(null);
  const [selectedModel, setSelectedModel] = useState(null); // For detailed view
  const [aiInsights, setAiInsights] = useState({}); // Store insights per model
  const [loadingAI, setLoadingAI] = useState(false);

  const fetchAIInsights = async (modelKey) => {
    try {
      setLoadingAI(true);
      const modelData = trainingResults[modelKey];
      const response = await axios.post(`${API}/ai/analyze-model`, modelData);
      setAiInsights(prev => ({
        ...prev,
        [modelKey]: response.data
      }));
    } catch (err) {
      console.error('Error fetching AI insights:', err);
      setAiInsights(prev => ({
        ...prev,
        [modelKey]: {
          success: false,
          error: 'Error al generar insights con IA. Verifique la configuración de OpenAI API.'
        }
      }));
    } finally {
      setLoadingAI(false);
    }
  };

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/ml/models`);
      setModels(response.data);
      setError(null);
    } catch (err) {
      setError('Error al cargar los modelos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const trainAllModels = async () => {
    try {
      setLoading(true);
      setTrainingModel('all');
      const response = await axios.post(`${API}/ml/train-all`);

      console.log('Full training response:', response.data);
      console.log('Models in response:', response.data.models);

      // Check if response has the expected structure
      if (!response.data.models) {
        console.error('No models in response!');
        setError('Respuesta del servidor inválida');
        return;
      }

      // Update models status
      const updatedModels = { ...models };
      Object.keys(response.data.models).forEach(modelKey => {
        if (updatedModels[modelKey]) {
          updatedModels[modelKey].trained = true;
        }
      });
      setModels(updatedModels);

      // Set training results
      setTrainingResults(response.data.models);
      setError(null);

      console.log('Training results state updated:', response.data.models);
      console.log('Example model data:', response.data.models.neural_network);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al entrenar los modelos');
      console.error('Training error:', err);
    } finally {
      setLoading(false);
      setTrainingModel(null);
    }
  };

  useEffect(() => {
    fetchModels();
  }, []);

  if (loading && !models) {
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-48" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-32 w-full" />
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

  const modelIcons = {
    'neural_network': Brain,
    'random_forest': TrendingUp,
    'svm': Target,
    'logistic_regression': Zap
  };

  const modelNames = {
    'neural_network': 'Red Neuronal',
    'random_forest': 'Random Forest',
    'svm': 'Support Vector Machine',
    'logistic_regression': 'Regresión Logística'
  };

  const modelColors = {
    'neural_network': 'purple',
    'random_forest': 'green',
    'svm': 'blue',
    'logistic_regression': 'orange'
  };

  // Render detailed view for a specific model
  const renderDetailedView = (modelKey) => {
    const modelData = trainingResults[modelKey];
    const Icon = modelIcons[modelKey];
    const color = modelColors[modelKey];

    if (!modelData || !modelData.test_metrics) {
      return null;
    }

    const confusionMatrix = modelData.confusion_matrix.test;
    const rocData = modelData.roc_curve;
    const metrics = modelData.test_metrics;

    return (
      <div className="space-y-6">
        {/* Back Button */}
        <Button
          onClick={() => setSelectedModel(null)}
          variant="outline"
          className="mb-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Volver a Comparación
        </Button>

        {/* Model Header */}
        <Card className={`border-${color}-200 bg-gradient-to-br from-${color}-50 to-white`}>
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-2">
              <Icon className={`h-6 w-6 text-${color}-600`} />
              {modelNames[modelKey]} - Vista Detallada
            </CardTitle>
            <CardDescription>
              Análisis completo del rendimiento del modelo
            </CardDescription>
          </CardHeader>
        </Card>

        {/* Metrics Summary */}
        <Card>
          <CardHeader>
            <CardTitle>Resumen de Métricas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <p className="text-sm text-gray-600">Exactitud</p>
                <p className="text-2xl font-bold text-blue-700">
                  {(metrics.accuracy * 100).toFixed(1)}%
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg text-center">
                <p className="text-sm text-gray-600">Precisión</p>
                <p className="text-2xl font-bold text-green-700">
                  {(metrics.precision * 100).toFixed(1)}%
                </p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg text-center">
                <p className="text-sm text-gray-600">Recall</p>
                <p className="text-2xl font-bold text-orange-700">
                  {(metrics.recall * 100).toFixed(1)}%
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg text-center">
                <p className="text-sm text-gray-600">F1-Score</p>
                <p className="text-2xl font-bold text-purple-700">
                  {(metrics.f1_score * 100).toFixed(1)}%
                </p>
              </div>
              <div className="bg-indigo-50 p-4 rounded-lg text-center">
                <p className="text-sm text-gray-600">ROC-AUC</p>
                <p className="text-2xl font-bold text-indigo-700">
                  {(metrics.roc_auc * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Confusion Matrix */}
          <Card>
            <CardHeader>
              <CardTitle>Matriz de Confusión</CardTitle>
              <CardDescription>Clasificación de casos en el conjunto de prueba</CardDescription>
            </CardHeader>
            <CardContent>
              <Plot
                data={[
                  {
                    z: confusionMatrix,
                    x: ['Predicho: No Cáncer', 'Predicho: Cáncer'],
                    y: ['Real: No Cáncer', 'Real: Cáncer'],
                    type: 'heatmap',
                    colorscale: 'Blues',
                    showscale: true,
                    text: confusionMatrix.map(row => row.map(val => val.toString())),
                    texttemplate: '%{text}',
                    textfont: { size: 16, color: 'white' },
                    hovertemplate: '%{y}<br>%{x}<br>Casos: %{z}<extra></extra>'
                  }
                ]}
                layout={{
                  autosize: true,
                  margin: { l: 120, r: 20, t: 20, b: 80 },
                  xaxis: { side: 'bottom' },
                  yaxis: { autorange: 'reversed' },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)'
                }}
                config={{ responsive: true, displayModeBar: false }}
                style={{ width: '100%', height: '350px' }}
              />
            </CardContent>
          </Card>

          {/* ROC Curve */}
          <Card>
            <CardHeader>
              <CardTitle>Curva ROC</CardTitle>
              <CardDescription>Relación entre sensibilidad y especificidad</CardDescription>
            </CardHeader>
            <CardContent>
              <Plot
                data={[
                  {
                    x: rocData.fpr,
                    y: rocData.tpr,
                    type: 'scatter',
                    mode: 'lines',
                    name: `ROC (AUC = ${(metrics.roc_auc * 100).toFixed(1)}%)`,
                    line: { color: '#8b5cf6', width: 3 },
                    fill: 'tozeroy',
                    fillcolor: 'rgba(139, 92, 246, 0.1)'
                  },
                  {
                    x: [0, 1],
                    y: [0, 1],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Línea Base',
                    line: { color: 'gray', width: 2, dash: 'dash' }
                  }
                ]}
                layout={{
                  autosize: true,
                  margin: { l: 60, r: 20, t: 20, b: 60 },
                  xaxis: { title: 'Tasa de Falsos Positivos (1 - Especificidad)', range: [0, 1] },
                  yaxis: { title: 'Tasa de Verdaderos Positivos (Sensibilidad)', range: [0, 1] },
                  showlegend: true,
                  legend: { x: 0.6, y: 0.1 },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)'
                }}
                config={{ responsive: true, displayModeBar: false }}
                style={{ width: '100%', height: '350px' }}
              />
            </CardContent>
          </Card>
        </div>

        {/* Metrics Bar Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Comparación de Métricas</CardTitle>
            <CardDescription>Visualización de todas las métricas de rendimiento</CardDescription>
          </CardHeader>
          <CardContent>
            <Plot
              data={[
                {
                  x: ['Exactitud', 'Precisión', 'Recall', 'F1-Score', 'ROC-AUC'],
                  y: [
                    metrics.accuracy * 100,
                    metrics.precision * 100,
                    metrics.recall * 100,
                    metrics.f1_score * 100,
                    metrics.roc_auc * 100
                  ],
                  type: 'bar',
                  marker: {
                    color: ['#3b82f6', '#10b981', '#f97316', '#a855f7', '#6366f1']
                  },
                  text: [
                    `${(metrics.accuracy * 100).toFixed(1)}%`,
                    `${(metrics.precision * 100).toFixed(1)}%`,
                    `${(metrics.recall * 100).toFixed(1)}%`,
                    `${(metrics.f1_score * 100).toFixed(1)}%`,
                    `${(metrics.roc_auc * 100).toFixed(1)}%`
                  ],
                  textposition: 'outside'
                }
              ]}
              layout={{
                autosize: true,
                margin: { l: 60, r: 20, t: 20, b: 60 },
                yaxis: { title: 'Porcentaje (%)', range: [0, 105] },
                xaxis: { title: 'Métrica' },
                showlegend: false,
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
              }}
              config={{ responsive: true, displayModeBar: false }}
              style={{ width: '100%', height: '400px' }}
            />
          </CardContent>
        </Card>

        {/* Feature Importance (if available) */}
        {modelData.feature_importance && modelData.feature_names && (
          <Card>
            <CardHeader>
              <CardTitle>Importancia de Características</CardTitle>
              <CardDescription>Variables más relevantes para la predicción</CardDescription>
            </CardHeader>
            <CardContent>
              <Plot
                data={[
                  {
                    x: modelData.feature_importance,
                    y: modelData.feature_names,
                    type: 'bar',
                    orientation: 'h',
                    marker: { color: '#8b5cf6' }
                  }
                ]}
                layout={{
                  autosize: true,
                  margin: { l: 150, r: 20, t: 20, b: 60 },
                  xaxis: { title: 'Importancia' },
                  yaxis: { title: '' },
                  showlegend: false,
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)'
                }}
                config={{ responsive: true, displayModeBar: false }}
                style={{ width: '100%', height: `${Math.max(400, modelData.feature_names.length * 30)}px` }}
              />
            </CardContent>
          </Card>
        )}

        {/* AI Insights */}
        <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-purple-600" />
                  Análisis del Modelo con IA
                </CardTitle>
                <CardDescription>
                  Evaluación automática del rendimiento y recomendaciones clínicas
                </CardDescription>
              </div>
              {!aiInsights[modelKey] && (
                <Button
                  onClick={() => fetchAIInsights(modelKey)}
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
                      Analizar con IA
                    </>
                  )}
                </Button>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {aiInsights[modelKey] ? (
              aiInsights[modelKey].success ? (
                <div className="prose prose-sm max-w-none">
                  <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                    {aiInsights[modelKey].insights}
                  </div>
                  <div className="mt-4 flex items-center gap-2">
                    <Badge variant="outline" className="text-xs">
                      Modelo: {aiInsights[modelKey].model_used}
                    </Badge>
                    <Badge variant="outline" className="text-xs">
                      Tokens: {aiInsights[modelKey].tokens_used}
                    </Badge>
                  </div>
                </div>
              ) : (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{aiInsights[modelKey].error}</AlertDescription>
                </Alert>
              )
            ) : (
              <p className="text-gray-500 text-center py-8">
                Haga clic en "Analizar con IA" para obtener una evaluación detallada del modelo
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    );
  };

  // If a model is selected, show detailed view
  if (selectedModel && trainingResults && trainingResults[selectedModel]) {
    return renderDetailedView(selectedModel);
  }

  // Otherwise, show main view
  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl flex items-center gap-2">
                <Brain className="h-6 w-6 text-purple-600" />
                Modelos de Machine Learning
              </CardTitle>
              <CardDescription>
                Entrenamiento y comparación de modelos de clasificación para predicción de cáncer de mama
              </CardDescription>
            </div>
            <Button
              onClick={trainAllModels}
              disabled={loading}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Entrenando...
                </>
              ) : (
                <>
                  <Zap className="mr-2 h-4 w-4" />
                  Entrenar Todos los Modelos
                </>
              )}
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Comparison Table */}
      {trainingResults && Object.keys(trainingResults).length > 0 && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-purple-600" />
              Comparación de Modelos
            </CardTitle>
            <CardDescription>
              Compara el rendimiento de todos los modelos entrenados
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Modelo</th>
                    <th className="text-center p-2">Exactitud</th>
                    <th className="text-center p-2">Precisión</th>
                    <th className="text-center p-2">Recall</th>
                    <th className="text-center p-2">F1-Score</th>
                    <th className="text-center p-2">ROC-AUC</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(trainingResults).map(([modelKey, result]) => {
                    if (!result.test_metrics) return null;
                    const metrics = result.test_metrics;
                    return (
                      <tr key={modelKey} className="border-b hover:bg-gray-50">
                        <td className="p-2 font-medium">{modelNames[modelKey]}</td>
                        <td className="text-center p-2">{(metrics.accuracy * 100).toFixed(1)}%</td>
                        <td className="text-center p-2">{(metrics.precision * 100).toFixed(1)}%</td>
                        <td className="text-center p-2 font-bold text-orange-600">
                          {(metrics.recall * 100).toFixed(1)}%
                        </td>
                        <td className="text-center p-2">{(metrics.f1_score * 100).toFixed(1)}%</td>
                        <td className="text-center p-2">{(metrics.roc_auc * 100).toFixed(1)}%</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <div className="mt-4 p-3 bg-yellow-50 rounded-lg">
              <p className="text-xs text-gray-600">
                <strong>💡 Tip:</strong> Para detección de cáncer, prioriza <strong>Recall</strong> (sensibilidad)
                para no perder casos positivos. Un modelo con alto Recall detecta más casos de cáncer.
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Models Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {models && Object.entries(models).map(([modelKey, modelData]) => {
          const Icon = modelIcons[modelKey];
          const color = modelColors[modelKey];
          const isTrained = modelData.trained;

          return (
            <Card key={modelKey} className={`border-${color}-200 hover:shadow-lg transition-shadow`}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2">
                    <Icon className={`h-5 w-5 text-${color}-600`} />
                    {modelNames[modelKey]}
                  </CardTitle>
                  {isTrained && (
                    <Badge variant="success" className="bg-green-100 text-green-800">
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Entrenado
                    </Badge>
                  )}
                </div>
                <CardDescription>{modelData.description}</CardDescription>
              </CardHeader>
              <CardContent>
                {/* Debug info */}
                {console.log(`Model ${modelKey}:`, {
                  isTrained,
                  hasResults: !!trainingResults?.[modelKey],
                  trainingResults: trainingResults?.[modelKey],
                  hasTestMetrics: !!trainingResults?.[modelKey]?.test_metrics
                })}

                {!isTrained ? (
                  <div className="text-center py-8">
                    <p className="text-sm text-gray-500 mb-4">
                      Modelo no entrenado. Haz clic en "Entrenar Todos los Modelos" para comenzar.
                    </p>
                  </div>
                ) : trainingResults && trainingResults[modelKey] && trainingResults[modelKey].test_metrics ? (
                  <div className="space-y-4">
                    {/* Test Metrics */}
                    <div>
                      <h4 className="text-sm font-semibold mb-3 text-gray-700">Métricas de Prueba</h4>
                      <div className="grid grid-cols-2 gap-3">
                        <div className="bg-blue-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600">Exactitud</p>
                          <p className="text-lg font-bold text-blue-700">
                            {(trainingResults[modelKey].test_metrics.accuracy * 100).toFixed(1)}%
                          </p>
                        </div>
                        <div className="bg-green-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600">Precisión</p>
                          <p className="text-lg font-bold text-green-700">
                            {(trainingResults[modelKey].test_metrics.precision * 100).toFixed(1)}%
                          </p>
                        </div>
                        <div className="bg-orange-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600">Recall</p>
                          <p className="text-lg font-bold text-orange-700">
                            {(trainingResults[modelKey].test_metrics.recall * 100).toFixed(1)}%
                          </p>
                        </div>
                        <div className="bg-purple-50 p-3 rounded-lg">
                          <p className="text-xs text-gray-600">F1-Score</p>
                          <p className="text-lg font-bold text-purple-700">
                            {(trainingResults[modelKey].test_metrics.f1_score * 100).toFixed(1)}%
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* ROC-AUC */}
                    <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-lg">
                      <p className="text-xs text-gray-600 mb-1">ROC-AUC Score</p>
                      <div className="flex items-center gap-2">
                        <Progress
                          value={trainingResults[modelKey].test_metrics.roc_auc * 100}
                          className="flex-1"
                        />
                        <span className="text-sm font-bold text-indigo-700">
                          {(trainingResults[modelKey].test_metrics.roc_auc * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    {/* View Details Button */}
                    <Button
                      onClick={() => setSelectedModel(modelKey)}
                      className={`w-full bg-${color}-500 hover:bg-${color}-600 text-white`}
                    >
                      <Eye className="mr-2 h-4 w-4" />
                      Ver Gráficas Detalladas
                    </Button>
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <p className="text-sm text-green-600 font-medium">
                      ✓ Modelo entrenado exitosamente
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default MLModels;

