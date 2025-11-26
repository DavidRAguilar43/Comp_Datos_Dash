import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2, Activity, AlertCircle, CheckCircle2, AlertTriangle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API = `${BACKEND_URL}/api`;

/**
 * PredictionForm component for breast cancer risk prediction.
 *
 * Allows users to input their clinical data and get a risk assessment.
 */
const PredictionForm = () => {
  const [formData, setFormData] = useState({
    age: '',
    menarche: '',
    menopause: '',
    agefirst: '',
    children: '',
    biopsies: '',
    imc: '',
    weight: '',
    histologicalclass: '',
    model_name: 'random_forest'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleModelChange = (value) => {
    setFormData(prev => ({
      ...prev,
      model_name: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Convert string values to numbers
      const payload = {
        ...formData,
        age: formData.age ? parseFloat(formData.age) : null,
        menarche: formData.menarche ? parseFloat(formData.menarche) : null,
        menopause: formData.menopause ? parseFloat(formData.menopause) : null,
        agefirst: formData.agefirst ? parseFloat(formData.agefirst) : null,
        children: formData.children ? parseFloat(formData.children) : null,
        biopsies: formData.biopsies ? parseFloat(formData.biopsies) : null,
        imc: formData.imc ? parseFloat(formData.imc) : null,
        weight: formData.weight ? parseFloat(formData.weight) : null,
        histologicalclass: formData.histologicalclass ? parseFloat(formData.histologicalclass) : null,
      };

      const response = await axios.post(`${API}/ml/predict`, payload);

      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || 'Error al realizar la predicción');
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Error al realizar la predicción. Asegúrese de que los modelos estén entrenados.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      age: '',
      menarche: '',
      menopause: '',
      agefirst: '',
      children: '',
      biopsies: '',
      imc: '',
      weight: '',
      histologicalclass: '',
      model_name: 'random_forest'
    });
    setResult(null);
    setError(null);
  };

  const getRiskIcon = (riskColor) => {
    switch (riskColor) {
      case 'green':
        return <CheckCircle2 className="h-12 w-12 text-green-600" />;
      case 'yellow':
        return <AlertTriangle className="h-12 w-12 text-yellow-600" />;
      case 'orange':
        return <AlertTriangle className="h-12 w-12 text-orange-600" />;
      case 'red':
        return <AlertCircle className="h-12 w-12 text-red-600" />;
      default:
        return <Activity className="h-12 w-12 text-gray-600" />;
    }
  };

  const getRiskColorClass = (riskColor) => {
    switch (riskColor) {
      case 'green':
        return 'from-green-50 to-green-100 border-green-300';
      case 'yellow':
        return 'from-yellow-50 to-yellow-100 border-yellow-300';
      case 'orange':
        return 'from-orange-50 to-orange-100 border-orange-300';
      case 'red':
        return 'from-red-50 to-red-100 border-red-300';
      default:
        return 'from-gray-50 to-gray-100 border-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      <Card className="border-purple-200">
        <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50">
          <CardTitle className="text-2xl flex items-center gap-2">
            <Activity className="h-6 w-6 text-purple-600" />
            Predicción de Riesgo de Cáncer de Mama
          </CardTitle>
          <CardDescription>
            Ingrese los datos clínicos para obtener una estimación del riesgo
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Model Selection */}
            <div className="space-y-2">
              <Label htmlFor="model_name">Modelo de Predicción</Label>
              <Select value={formData.model_name} onValueChange={handleModelChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Seleccione un modelo" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="random_forest">Random Forest (Recomendado)</SelectItem>
                  <SelectItem value="neural_network">Red Neuronal</SelectItem>
                  <SelectItem value="svm">SVM</SelectItem>
                  <SelectItem value="logistic_regression">Regresión Logística</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Input Fields Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Age */}
              <div className="space-y-2">
                <Label htmlFor="age">Edad (años)</Label>
                <Input
                  id="age"
                  name="age"
                  type="number"
                  placeholder="Ej: 45"
                  value={formData.age}
                  onChange={handleInputChange}
                />
              </div>

              {/* Menarche */}
              <div className="space-y-2">
                <Label htmlFor="menarche">Edad de Menarquia (años)</Label>
                <Input
                  id="menarche"
                  name="menarche"
                  type="number"
                  placeholder="Ej: 12"
                  value={formData.menarche}
                  onChange={handleInputChange}
                />
              </div>

              {/* Menopause */}
              <div className="space-y-2">
                <Label htmlFor="menopause">Edad de Menopausia (años)</Label>
                <Input
                  id="menopause"
                  name="menopause"
                  type="number"
                  placeholder="Ej: 50 (dejar vacío si no aplica)"
                  value={formData.menopause}
                  onChange={handleInputChange}
                />
              </div>

              {/* Age First Pregnancy */}
              <div className="space-y-2">
                <Label htmlFor="agefirst">Edad Primer Embarazo (años)</Label>
                <Input
                  id="agefirst"
                  name="agefirst"
                  type="number"
                  placeholder="Ej: 25 (dejar vacío si no aplica)"
                  value={formData.agefirst}
                  onChange={handleInputChange}
                />
              </div>

              {/* Children */}
              <div className="space-y-2">
                <Label htmlFor="children">Número de Hijos</Label>
                <Input
                  id="children"
                  name="children"
                  type="number"
                  placeholder="Ej: 2"
                  value={formData.children}
                  onChange={handleInputChange}
                />
              </div>

              {/* Biopsies */}
              <div className="space-y-2">
                <Label htmlFor="biopsies">Número de Biopsias</Label>
                <Input
                  id="biopsies"
                  name="biopsies"
                  type="number"
                  placeholder="Ej: 1"
                  value={formData.biopsies}
                  onChange={handleInputChange}
                />
              </div>

              {/* IMC */}
              <div className="space-y-2">
                <Label htmlFor="imc">IMC (Índice de Masa Corporal)</Label>
                <Input
                  id="imc"
                  name="imc"
                  type="number"
                  step="0.1"
                  placeholder="Ej: 24.5"
                  value={formData.imc}
                  onChange={handleInputChange}
                />
              </div>

              {/* Weight */}
              <div className="space-y-2">
                <Label htmlFor="weight">Peso (kg)</Label>
                <Input
                  id="weight"
                  name="weight"
                  type="number"
                  step="0.1"
                  placeholder="Ej: 65.5"
                  value={formData.weight}
                  onChange={handleInputChange}
                />
              </div>

              {/* Histological Class */}
              <div className="space-y-2">
                <Label htmlFor="histologicalclass">Clase Histológica</Label>
                <Input
                  id="histologicalclass"
                  name="histologicalclass"
                  type="number"
                  placeholder="Ej: 3"
                  value={formData.histologicalclass}
                  onChange={handleInputChange}
                />
              </div>
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <Button
                type="submit"
                disabled={loading}
                className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Analizando...
                  </>
                ) : (
                  <>
                    <Activity className="w-4 h-4 mr-2" />
                    Calcular Riesgo
                  </>
                )}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleReset}
                disabled={loading}
              >
                Limpiar
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Results */}
      {result && (
        <Card className={`border-2 bg-gradient-to-br ${getRiskColorClass(result.risk_color)}`}>
          <CardHeader>
            <CardTitle className="text-2xl flex items-center justify-center gap-3">
              {getRiskIcon(result.risk_color)}
              Resultado del Análisis
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Risk Level */}
            <div className="text-center space-y-2">
              <p className="text-sm text-gray-600 font-medium">Nivel de Riesgo</p>
              <p className="text-4xl font-bold">{result.risk_level}</p>
            </div>

            {/* Probability */}
            <div className="text-center space-y-2">
              <p className="text-sm text-gray-600 font-medium">Probabilidad Estimada</p>
              <p className="text-5xl font-bold">{result.probability_percentage}%</p>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${
                  result.risk_color === 'green' ? 'bg-green-500' :
                  result.risk_color === 'yellow' ? 'bg-yellow-500' :
                  result.risk_color === 'orange' ? 'bg-orange-500' :
                  'bg-red-500'
                }`}
                style={{ width: `${result.probability_percentage}%` }}
              />
            </div>

            {/* Interpretation */}
            <Alert>
              <AlertDescription className="text-sm leading-relaxed">
                {result.interpretation}
              </AlertDescription>
            </Alert>

            {/* Model Info */}
            <div className="text-center text-xs text-gray-500">
              Modelo utilizado: {result.model_used === 'random_forest' ? 'Random Forest' :
                                result.model_used === 'neural_network' ? 'Red Neuronal' :
                                result.model_used === 'svm' ? 'SVM' :
                                'Regresión Logística'}
            </div>

            {/* Disclaimer */}
            <Alert className="bg-blue-50 border-blue-200">
              <AlertDescription className="text-xs text-blue-800">
                <strong>Nota importante:</strong> Este resultado es una estimación basada en modelos estadísticos
                y NO reemplaza el diagnóstico médico profesional. Consulte siempre con un especialista en salud.
              </AlertDescription>
            </Alert>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default PredictionForm;

