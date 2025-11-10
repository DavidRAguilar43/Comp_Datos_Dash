import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import axios from 'axios';
import { Download, FileText, FileJson, FileSpreadsheet, Sparkles, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * ExportPanel component for data and report export.
 * 
 * Allows exporting:
 * - Processed data (CSV, JSON, Excel)
 * - AI-generated clinical report
 */
const ExportPanel = () => {
  const [exporting, setExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState(null);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleExport = async (format) => {
    try {
      setExporting(true);
      setExportFormat(format);
      setError(null);
      setSuccess(null);

      const response = await axios.get(`${API}/data/export/${format}`, {
        responseType: 'blob',
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const extensions = {
        csv: 'csv',
        json: 'json',
        excel: 'xlsx'
      };
      
      link.setAttribute('download', `breast_cancer_data.${extensions[format]}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setSuccess(`Datos exportados exitosamente en formato ${format.toUpperCase()}`);
    } catch (err) {
      setError('Error al exportar datos. Por favor intente nuevamente.');
      console.error(err);
    } finally {
      setExporting(false);
      setExportFormat(null);
    }
  };

  const handleGenerateReport = async () => {
    try {
      setGeneratingReport(true);
      setError(null);

      const response = await axios.post(`${API}/ai/generate-report`);
      
      if (response.data.success) {
        setReport(response.data);
      } else {
        setError(response.data.error || 'Error al generar el reporte');
      }
    } catch (err) {
      setError('Error al generar el reporte. Verifique la configuración de OpenAI API.');
      console.error(err);
    } finally {
      setGeneratingReport(false);
    }
  };

  const downloadReport = () => {
    if (!report) return;

    const blob = new Blob([report.report], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'reporte_clinico.md');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Export Data Section */}
      <Card className="border-blue-200">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Download className="h-5 w-5 text-blue-600" />
            Exportar Datos Procesados
          </CardTitle>
          <CardDescription>
            Descargue los datos procesados en diferentes formatos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* CSV Export */}
            <Card className="border-pink-200 hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="pt-6">
                <div className="text-center space-y-4">
                  <div className="flex justify-center">
                    <div className="p-4 bg-pink-100 rounded-full">
                      <FileText className="h-8 w-8 text-pink-600" />
                    </div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800">CSV</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Formato compatible con Excel y análisis estadístico
                    </p>
                  </div>
                  <Button
                    onClick={() => handleExport('csv')}
                    disabled={exporting}
                    className="w-full bg-pink-500 hover:bg-pink-600"
                  >
                    {exporting && exportFormat === 'csv' ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Exportando...
                      </>
                    ) : (
                      <>
                        <Download className="w-4 h-4 mr-2" />
                        Descargar CSV
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* JSON Export */}
            <Card className="border-blue-200 hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="pt-6">
                <div className="text-center space-y-4">
                  <div className="flex justify-center">
                    <div className="p-4 bg-blue-100 rounded-full">
                      <FileJson className="h-8 w-8 text-blue-600" />
                    </div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800">JSON</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Formato para integración con aplicaciones web
                    </p>
                  </div>
                  <Button
                    onClick={() => handleExport('json')}
                    disabled={exporting}
                    className="w-full bg-blue-500 hover:bg-blue-600"
                  >
                    {exporting && exportFormat === 'json' ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Exportando...
                      </>
                    ) : (
                      <>
                        <Download className="w-4 h-4 mr-2" />
                        Descargar JSON
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Excel Export */}
            <Card className="border-green-200 hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="pt-6">
                <div className="text-center space-y-4">
                  <div className="flex justify-center">
                    <div className="p-4 bg-green-100 rounded-full">
                      <FileSpreadsheet className="h-8 w-8 text-green-600" />
                    </div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-800">Excel</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Formato XLSX para Microsoft Excel
                    </p>
                  </div>
                  <Button
                    onClick={() => handleExport('excel')}
                    disabled={exporting}
                    className="w-full bg-green-500 hover:bg-green-600"
                  >
                    {exporting && exportFormat === 'excel' ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Exportando...
                      </>
                    ) : (
                      <>
                        <Download className="w-4 h-4 mr-2" />
                        Descargar Excel
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      {/* Success/Error Messages */}
      {success && (
        <Alert className="border-green-300 bg-green-50 text-green-800">
          <CheckCircle2 className="h-4 w-4" />
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      )}

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* AI Report Section */}
      <Card className="border-purple-200 bg-gradient-to-br from-purple-50 to-white">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-purple-600" />
            Reporte Clínico Completo con IA
          </CardTitle>
          <CardDescription>
            Genere un reporte clínico profesional con análisis automático de todos los datos
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!report ? (
            <div className="text-center py-8">
              <p className="text-gray-600 mb-4">
                Genere un reporte clínico completo que incluye resumen ejecutivo, análisis demográfico,
                factores de riesgo identificados, y recomendaciones para investigación futura.
              </p>
              <Button
                onClick={handleGenerateReport}
                disabled={generatingReport}
                className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                size="lg"
              >
                {generatingReport ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Generando Reporte...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    Generar Reporte Clínico
                  </>
                )}
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-purple-100 rounded-lg">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="h-6 w-6 text-purple-600" />
                  <div>
                    <p className="font-semibold text-purple-900">Reporte Generado</p>
                    <p className="text-sm text-purple-700">
                      Listo para descargar en formato Markdown
                    </p>
                  </div>
                </div>
                <Button
                  onClick={downloadReport}
                  className="bg-purple-600 hover:bg-purple-700"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Descargar Reporte
                </Button>
              </div>

              <div className="p-6 bg-white rounded-lg border border-purple-200 max-h-96 overflow-y-auto">
                <div className="prose prose-sm max-w-none">
                  <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                    {report.report}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-xs">
                  Modelo: {report.model_used}
                </Badge>
                <Badge variant="outline" className="text-xs">
                  Tokens: {report.tokens_used}
                </Badge>
              </div>

              <Button
                onClick={() => setReport(null)}
                variant="outline"
                className="w-full"
              >
                Generar Nuevo Reporte
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ExportPanel;

