import React, { useState, useEffect } from 'react';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  BookOpen,
  Database,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Data Understanding Panel component.
 *
 * Displays real data quality metrics from the loaded dataset.
 */
const DataUnderstandingPanel = () => {
  const [qualityData, setQualityData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (isOpen && !qualityData && !loading) {
      fetchQualityData();
    }
  }, [isOpen]);

  const fetchQualityData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/data/quality`);
      if (!response.ok) {
        throw new Error('No hay datos cargados');
      }
      const data = await response.json();
      setQualityData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button
          variant="outline"
          className="bg-gradient-to-r from-indigo-50 to-purple-50 border-indigo-300 hover:from-indigo-100 hover:to-purple-100 text-indigo-700 font-semibold"
        >
          <BookOpen className="w-4 h-4 mr-2" />
          Calidad de Datos
        </Button>
      </SheetTrigger>

      <SheetContent side="right" className="w-full sm:max-w-xl overflow-y-auto">
        <SheetHeader>
          <SheetTitle className="text-2xl bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Entendimiento de los Datos
          </SheetTitle>
          <SheetDescription>
            Análisis de calidad del dataset cargado
          </SheetDescription>
        </SheetHeader>

        <ScrollArea className="h-[calc(100vh-120px)] mt-6 pr-4">
          {loading ? (
            <div className="space-y-4">
              <Skeleton className="h-32 w-full" />
              <Skeleton className="h-32 w-full" />
              <Skeleton className="h-32 w-full" />
            </div>
          ) : error ? (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          ) : qualityData ? (
            <div className="space-y-6">
              {/* Basic Statistics */}
              <Card className="border-indigo-200 bg-gradient-to-br from-indigo-50/50 to-white">
                <CardHeader>
                  <CardTitle className="text-lg text-indigo-900 flex items-center gap-2">
                    <Database className="w-5 h-5" />
                    Información General
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Total de Registros</p>
                      <p className="text-2xl font-bold text-indigo-700">
                        {qualityData.basic_stats.total_rows.toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Total de Columnas</p>
                      <p className="text-2xl font-bold text-indigo-700">
                        {qualityData.basic_stats.total_columns}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Columnas Numéricas</p>
                      <p className="text-xl font-semibold text-blue-600">
                        {qualityData.data_types.numeric.length}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Columnas Categóricas</p>
                      <p className="text-xl font-semibold text-green-600">
                        {qualityData.data_types.categorical.length}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Missing Values */}
              <Card className="border-orange-200 hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-orange-100 rounded-lg">
                      <AlertTriangle className="w-5 h-5 text-orange-600" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-base text-orange-900">
                        Valores Faltantes
                      </CardTitle>
                      <CardDescription className="mt-1">
                        Análisis de datos incompletos
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {Object.keys(qualityData.missing_values).length > 0 ? (
                    <div className="space-y-3">
                      {Object.entries(qualityData.missing_values).map(([col, data]) => (
                        <div key={col} className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                          <div className="flex-1">
                            <p className="font-medium text-sm text-gray-800">{col}</p>
                            <p className="text-xs text-gray-600">
                              {data.count} valores faltantes
                            </p>
                          </div>
                          <Badge variant="outline" className="bg-orange-100 text-orange-700 border-orange-300">
                            {data.percentage}%
                          </Badge>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-green-700 bg-green-50 p-3 rounded-lg">
                      <CheckCircle2 className="w-5 h-5" />
                      <span className="text-sm font-medium">No hay valores faltantes</span>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Duplicates */}
              <Card className="border-yellow-200 hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-yellow-100 rounded-lg">
                      <XCircle className="w-5 h-5 text-yellow-600" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-base text-yellow-900">
                        Registros Duplicados
                      </CardTitle>
                      <CardDescription className="mt-1">
                        Detección de datos repetidos
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-lg">
                    <div>
                      <p className="text-2xl font-bold text-yellow-700">
                        {qualityData.duplicates.count}
                      </p>
                      <p className="text-sm text-gray-600">duplicados encontrados</p>
                    </div>
                    <Badge variant="outline" className="bg-yellow-100 text-yellow-700 border-yellow-300">
                      {qualityData.duplicates.percentage}%
                    </Badge>
                  </div>
                </CardContent>
              </Card>

              {/* Outliers */}
              <Card className="border-red-200 hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-red-100 rounded-lg">
                      <TrendingUp className="w-5 h-5 text-red-600" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-base text-red-900">
                        Valores Atípicos (Outliers)
                      </CardTitle>
                      <CardDescription className="mt-1">
                        Detección usando método IQR
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {Object.keys(qualityData.outliers).length > 0 ? (
                    <div className="space-y-3">
                      {Object.entries(qualityData.outliers).map(([col, data]) => (
                        <div key={col} className="p-3 bg-red-50 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <p className="font-medium text-sm text-gray-800">{col}</p>
                            <Badge variant="outline" className="bg-red-100 text-red-700 border-red-300">
                              {data.percentage}%
                            </Badge>
                          </div>
                          <p className="text-xs text-gray-600">
                            {data.count} valores atípicos detectados
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            Rango normal: [{data.lower_bound.toFixed(2)}, {data.upper_bound.toFixed(2)}]
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-green-700 bg-green-50 p-3 rounded-lg">
                      <CheckCircle2 className="w-5 h-5" />
                      <span className="text-sm font-medium">No se detectaron valores atípicos significativos</span>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Class Balance */}
              <Card className="border-blue-200 hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <Database className="w-5 h-5 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-base text-blue-900">
                        Balance de Clases
                      </CardTitle>
                      <CardDescription className="mt-1">
                        Distribución de variables categóricas
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(qualityData.class_balance).slice(0, 3).map(([col, values]) => (
                      <div key={col} className="space-y-2">
                        <p className="font-medium text-sm text-gray-800">{col}</p>
                        <div className="space-y-1">
                          {Object.entries(values).map(([value, data]) => (
                            <div key={value} className="flex items-center justify-between text-xs">
                              <span className="text-gray-600">{value}</span>
                              <div className="flex items-center gap-2">
                                <div className="w-24 bg-gray-200 rounded-full h-2">
                                  <div
                                    className="bg-blue-500 h-2 rounded-full"
                                    style={{ width: `${data.percentage}%` }}
                                  />
                                </div>
                                <span className="text-gray-700 font-medium w-12 text-right">
                                  {data.percentage}%
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Inconsistencies */}
              {qualityData.inconsistencies.length > 0 && (
                <Card className="border-red-200 bg-red-50">
                  <CardHeader>
                    <CardTitle className="text-base text-red-900 flex items-center gap-2">
                      <AlertCircle className="w-5 h-5" />
                      Inconsistencias Detectadas
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {qualityData.inconsistencies.map((issue, idx) => (
                        <Alert key={idx} variant="destructive">
                          <AlertDescription>
                            <strong>{issue.column}:</strong> {issue.issue} ({issue.count} registros)
                          </AlertDescription>
                        </Alert>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          ) : (
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Cargue un dataset para ver el análisis de calidad de datos
              </AlertDescription>
            </Alert>
          )}
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
};

export default DataUnderstandingPanel;

