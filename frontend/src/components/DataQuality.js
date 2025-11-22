import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  CheckCircle2, 
  AlertTriangle, 
  Info, 
  TrendingUp,
  Database,
  FileCheck,
  Zap
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const API_URL = `${BACKEND_URL}/api`;

/**
 * DataQuality component displays comprehensive data preparation report.
 * 
 * Shows:
 * - Missing data summary
 * - Imputation report
 * - Duplicate removal
 * - Outlier detection
 * - Type corrections
 * - Transformation log
 */
const DataQuality = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [report, setReport] = useState(null);

  useEffect(() => {
    fetchPreparationReport();
  }, []);

  const fetchPreparationReport = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get(`${API_URL}/data/preparation-report`);
      
      if (response.data.success) {
        setReport(response.data);
      } else {
        setError(response.data.error || 'Error al obtener el reporte');
      }
    } catch (err) {
      console.error('Error fetching preparation report:', err);
      setError(err.response?.data?.detail || 'Error al cargar el reporte de calidad de datos');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando reporte de calidad de datos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (!report || !report.report) {
    return (
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          No hay datos de preparación disponibles. Por favor, cargue un archivo CSV primero.
        </AlertDescription>
      </Alert>
    );
  }

  const { report: prepLog, summary } = report;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-green-200 bg-green-50">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-green-800 flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4" />
              Transformaciones
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-900">{summary.total_transformations}</div>
            <p className="text-xs text-green-700 mt-1">Operaciones aplicadas</p>
          </CardContent>
        </Card>

        <Card className="border-blue-200 bg-blue-50">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-blue-800 flex items-center gap-2">
              <Database className="h-4 w-4" />
              Imputación
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-900">{summary.columns_imputed}</div>
            <p className="text-xs text-blue-700 mt-1">Columnas imputadas</p>
          </CardContent>
        </Card>

        <Card className="border-orange-200 bg-orange-50">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-orange-800 flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              Valores Atípicos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-900">{summary.columns_with_outliers}</div>
            <p className="text-xs text-orange-700 mt-1">Columnas con outliers</p>
          </CardContent>
        </Card>

        <Card className="border-purple-200 bg-purple-50">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-purple-800 flex items-center gap-2">
              <FileCheck className="h-4 w-4" />
              Duplicados
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-900">{summary.duplicates_removed}</div>
            <p className="text-xs text-purple-700 mt-1">Registros eliminados</p>
          </CardContent>
        </Card>
      </div>

      {/* Missing Data Summary */}
      {prepLog.missing_data && (prepLog.missing_data.before || prepLog.missing_data.after) && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Info className="h-5 w-5 text-blue-600" />
              Resumen de Datos Faltantes
            </CardTitle>
            <CardDescription>
              Análisis de valores nulos antes y después del procesamiento
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Before */}
              <div>
                <h4 className="font-semibold text-sm mb-3 text-gray-700">Antes del Procesamiento</h4>
                {Object.keys(prepLog.missing_data.before || {}).length > 0 ? (
                  <div className="space-y-2">
                    {Object.entries(prepLog.missing_data.before).map(([col, data]) => (
                      <div key={col} className="flex justify-between items-center p-2 bg-red-50 rounded">
                        <span className="text-sm font-medium text-gray-700">{col}</span>
                        <div className="flex items-center gap-2">
                          <Badge variant="destructive">{data.count} valores</Badge>
                          <span className="text-xs text-gray-600">{data.percentage}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 italic">No se detectaron valores faltantes</p>
                )}
              </div>

              {/* After */}
              <div>
                <h4 className="font-semibold text-sm mb-3 text-gray-700">Después del Procesamiento</h4>
                {Object.keys(prepLog.missing_data.after || {}).length > 0 ? (
                  <div className="space-y-2">
                    {Object.entries(prepLog.missing_data.after).map(([col, data]) => (
                      <div key={col} className="flex justify-between items-center p-2 bg-yellow-50 rounded">
                        <span className="text-sm font-medium text-gray-700">{col}</span>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline">{data.count} valores</Badge>
                          <span className="text-xs text-gray-600">{data.percentage}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex items-center gap-2 text-green-600">
                    <CheckCircle2 className="h-4 w-4" />
                    <p className="text-sm font-medium">Todos los valores faltantes fueron imputados</p>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Imputation Report */}
      {prepLog.imputation && Object.keys(prepLog.imputation).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-blue-600" />
              Reporte de Imputación
            </CardTitle>
            <CardDescription>
              Métodos utilizados para completar valores faltantes
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Columna</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Valores Imputados</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Método</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Valor de Relleno</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(prepLog.imputation).map(([col, data]) => (
                    <tr key={col} className="border-b hover:bg-gray-50">
                      <td className="py-2 px-4 text-sm font-medium text-gray-900">{col}</td>
                      <td className="py-2 px-4 text-sm text-gray-700">{data.values_imputed}</td>
                      <td className="py-2 px-4">
                        <Badge variant={data.method === 'mean' ? 'default' : 'secondary'}>
                          {data.method === 'mean' ? 'Media' : 'Moda'}
                        </Badge>
                      </td>
                      <td className="py-2 px-4 text-sm text-gray-700">
                        {typeof data.fill_value === 'number'
                          ? data.fill_value.toFixed(2)
                          : data.fill_value}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Duplicate Removal Report */}
      {prepLog.duplicates && prepLog.duplicates.total_detected > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileCheck className="h-5 w-5 text-purple-600" />
              Eliminación de Duplicados
            </CardTitle>
            <CardDescription>
              Registros duplicados detectados y eliminados
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-purple-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Detectado</p>
                <p className="text-2xl font-bold text-purple-900">{prepLog.duplicates.total_detected}</p>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Eliminados</p>
                <p className="text-2xl font-bold text-purple-900">{prepLog.duplicates.removed}</p>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Método</p>
                <p className="text-lg font-semibold text-purple-900">{prepLog.duplicates.method}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Outlier Detection Report */}
      {prepLog.outliers && Object.keys(prepLog.outliers).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-600" />
              Detección de Valores Atípicos
            </CardTitle>
            <CardDescription>
              Valores atípicos detectados usando el método IQR (Rango Intercuartílico)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Columna</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Cantidad</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Porcentaje</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Límite Inferior</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Límite Superior</th>
                    <th className="text-left py-2 px-4 font-semibold text-sm text-gray-700">Tratamiento</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(prepLog.outliers).map(([col, data]) => (
                    <tr key={col} className="border-b hover:bg-gray-50">
                      <td className="py-2 px-4 text-sm font-medium text-gray-900">{col}</td>
                      <td className="py-2 px-4 text-sm text-gray-700">{data.count}</td>
                      <td className="py-2 px-4">
                        <Badge variant="outline" className="bg-orange-50">
                          {data.percentage}%
                        </Badge>
                      </td>
                      <td className="py-2 px-4 text-sm text-gray-700">{data.lower_bound.toFixed(2)}</td>
                      <td className="py-2 px-4 text-sm text-gray-700">{data.upper_bound.toFixed(2)}</td>
                      <td className="py-2 px-4">
                        <Badge variant="secondary">{data.treatment}</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Type Correction Report */}
      {prepLog.type_corrections && Object.keys(prepLog.type_corrections).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-green-600" />
              Correcciones de Tipo de Datos
            </CardTitle>
            <CardDescription>
              Columnas con tipos de datos corregidos
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(prepLog.type_corrections).map(([col, data]) => (
                <div key={col} className="p-4 bg-green-50 rounded-lg border border-green-200">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-900">{col}</h4>
                    <Badge variant="outline" className="bg-green-100">Corregido</Badge>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Tipo Original:</p>
                      <p className="font-medium text-red-700">{data.original_type}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Nuevo Tipo:</p>
                      <p className="font-medium text-green-700">{data.new_type}</p>
                    </div>
                  </div>
                  <Separator className="my-2" />
                  <p className="text-xs text-gray-600">
                    <strong>Razón:</strong> {data.reason}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Transformation Log */}
      {prepLog.transformations && prepLog.transformations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-indigo-600" />
              Registro de Transformaciones
            </CardTitle>
            <CardDescription>
              Todas las transformaciones aplicadas al conjunto de datos
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {prepLog.transformations.map((transform, index) => (
                <div key={index} className="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-900 mb-1">
                        {transform.operation.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </h4>
                      <p className="text-sm text-gray-700 mb-2">{transform.description}</p>
                      {transform.columns_affected && transform.columns_affected.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          <span className="text-xs text-gray-600">Columnas afectadas:</span>
                          {transform.columns_affected.map((col, idx) => (
                            <Badge key={idx} variant="outline" className="text-xs">
                              {col}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Column Renaming */}
      {prepLog.column_renaming && Object.keys(prepLog.column_renaming).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileCheck className="h-5 w-5 text-teal-600" />
              Renombrado de Columnas
            </CardTitle>
            <CardDescription>
              Columnas renombradas para mayor claridad
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {Object.entries(prepLog.column_renaming).map(([oldName, newName]) => (
                <div key={oldName} className="p-3 bg-teal-50 rounded-lg border border-teal-200">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="text-sm text-gray-600">Anterior:</p>
                      <p className="font-medium text-red-700 line-through">{oldName}</p>
                    </div>
                    <div className="px-2">→</div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-600">Nuevo:</p>
                      <p className="font-medium text-green-700">{newName}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Date Formatting */}
      {prepLog.date_formatting && Object.keys(prepLog.date_formatting).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Info className="h-5 w-5 text-blue-600" />
              Formato de Fechas
            </CardTitle>
            <CardDescription>
              Estandarización de formatos de fecha
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(prepLog.date_formatting).map(([col, data]) => (
                <div key={col} className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="font-semibold text-gray-900 mb-2">{col}</h4>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Formato Aplicado:</p>
                      <p className="font-medium text-blue-700">{data.format_applied}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Ejemplo Antes:</p>
                      <p className="font-medium text-gray-700">{data.example_before}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Ejemplo Después:</p>
                      <p className="font-medium text-green-700">{data.example_after}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default DataQuality;

