import React, { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * FileUploader component for CSV data upload.
 * 
 * Handles file selection, validation, upload, and processing.
 * Provides visual feedback during upload and processing.
 */
const FileUploader = ({ onDataUploaded }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    
    if (selectedFile) {
      // Validate file type
      if (!selectedFile.name.endsWith('.csv')) {
        setError('Por favor seleccione un archivo CSV válido');
        setFile(null);
        return;
      }

      // Validate file size (max 50MB)
      const maxSize = 50 * 1024 * 1024; // 50MB in bytes
      if (selectedFile.size > maxSize) {
        setError('El archivo es demasiado grande. Tamaño máximo: 50MB');
        setFile(null);
        return;
      }

      setFile(selectedFile);
      setError(null);
      setSuccess(false);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Por favor seleccione un archivo');
      return;
    }

    setUploading(true);
    setProgress(0);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await axios.post(`${API}/data/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (response.data.success) {
        setSuccess(true);
        setTimeout(() => {
          onDataUploaded(response.data);
        }, 500);
      } else {
        setError('Error al procesar el archivo');
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Error al cargar el archivo. Por favor intente nuevamente.'
      );
      setProgress(0);
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      const event = { target: { files: [droppedFile] } };
      handleFileChange(event);
    }
  }, []);

  return (
    <div className="space-y-4">
      {/* Drag and Drop Area */}
      <Card
        className={`border-2 border-dashed transition-all ${
          file
            ? 'border-pink-400 bg-pink-50'
            : 'border-gray-300 hover:border-pink-300 hover:bg-pink-50/50'
        }`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <CardContent className="flex flex-col items-center justify-center py-12">
          <div className="text-center space-y-4">
            {file ? (
              <>
                <FileText className="w-16 h-16 mx-auto text-pink-500" />
                <div>
                  <p className="font-semibold text-gray-800">{file.name}</p>
                  <p className="text-sm text-gray-600">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </>
            ) : (
              <>
                <Upload className="w-16 h-16 mx-auto text-gray-400" />
                <div>
                  <p className="font-semibold text-gray-800">
                    Arrastre su archivo CSV aquí
                  </p>
                  <p className="text-sm text-gray-600">o haga clic para seleccionar</p>
                </div>
              </>
            )}

            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
              disabled={uploading}
            />
            <label htmlFor="file-upload">
              <Button
                variant="outline"
                className="cursor-pointer border-pink-300 text-pink-700 hover:bg-pink-50"
                disabled={uploading}
                asChild
              >
                <span>Seleccionar Archivo</span>
              </Button>
            </label>
          </div>
        </CardContent>
      </Card>

      {/* Upload Progress */}
      {uploading && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Procesando archivo...</span>
            <span className="font-semibold text-pink-600">{progress}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>
      )}

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="border-red-300 bg-red-50">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Success Alert */}
      {success && (
        <Alert className="border-green-300 bg-green-50 text-green-800">
          <CheckCircle2 className="h-4 w-4" />
          <AlertDescription>
            ¡Archivo cargado y procesado exitosamente!
          </AlertDescription>
        </Alert>
      )}

      {/* Upload Button */}
      <Button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="w-full bg-gradient-to-r from-pink-500 to-blue-500 hover:from-pink-600 hover:to-blue-600 text-white"
      >
        {uploading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Procesando...
          </>
        ) : (
          <>
            <Upload className="w-4 h-4 mr-2" />
            Cargar y Analizar Datos
          </>
        )}
      </Button>

      {/* Info */}
      <div className="text-xs text-gray-500 text-center space-y-1">
        <p>Formatos aceptados: CSV</p>
        <p>Tamaño máximo: 50 MB</p>
      </div>
    </div>
  );
};

export default FileUploader;

