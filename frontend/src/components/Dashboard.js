import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/contexts/AuthContext';
import FileUploader from './FileUploader';
import DataSummary from './DataSummary';
import ClinicalFactors from './ClinicalFactors';
import CorrelationsView from './CorrelationsView';
import MLModels from './MLModels';
import PredictionForm from './PredictionForm';
import DataUnderstandingPanel from './DataUnderstandingPanel';
import DataQuality from './DataQuality';
import { Activity, BarChart3, Network, Brain, Shield, Target, LogOut, User } from 'lucide-react';

/**
 * Main Dashboard component for breast cancer data analysis.
 *
 * Provides tabbed interface for:
 * - General exploration
 * - Data quality and preparation report
 * - Clinical factors analysis
 * - Correlations and patterns
 * - Data export
 */
const Dashboard = () => {
  const [dataLoaded, setDataLoaded] = useState(false);
  const [uploadInfo, setUploadInfo] = useState(null);
  const [activeTab, setActiveTab] = useState('exploration');
  const { user, logout } = useAuth();

  const handleDataUploaded = (info) => {
    setUploadInfo(info);
    setDataLoaded(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-green-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-pink-200 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-pink-600 via-blue-600 to-green-600 bg-clip-text text-transparent">
                Dashboard Clínico
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Análisis de Factores de Riesgo de Cáncer de Mama en Mujeres Cubanas
              </p>
            </div>
            <div className="flex items-center gap-4">
              {/* Data Understanding Panel Button */}
              <DataUnderstandingPanel />

              {dataLoaded && (
                <div className="text-right">
                  <p className="text-sm text-gray-600">
                    Datos cargados: <span className="font-semibold text-pink-600">
                      {uploadInfo?.upload_info?.rows || 0} registros
                    </span>
                  </p>
                  <p className="text-xs text-gray-500">
                    {uploadInfo?.upload_info?.filename}
                  </p>
                </div>
              )}

              {/* User Info and Logout */}
              <div className="flex items-center gap-3 border-l border-gray-300 pl-4">
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <User className="w-4 h-4" />
                  <span className="font-medium">{user?.full_name || user?.email}</span>
                </div>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-white bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 rounded-md transition-all"
                  title="Cerrar sesión"
                >
                  <LogOut className="w-4 h-4" />
                  Salir
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {!dataLoaded ? (
          <Card className="max-w-2xl mx-auto border-pink-200 shadow-lg">
            <CardHeader className="bg-gradient-to-r from-pink-50 to-blue-50">
              <CardTitle className="text-2xl text-center text-gray-800">
                Bienvenido al Dashboard Clínico
              </CardTitle>
              <CardDescription className="text-center">
                Cargue un archivo CSV con datos de pacientes para comenzar el análisis
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <FileUploader onDataUploaded={handleDataUploaded} />
            </CardContent>
          </Card>
        ) : (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-6 bg-white/80 backdrop-blur-sm border border-pink-200 p-1">
              <TabsTrigger
                value="exploration"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-100 data-[state=active]:to-pink-200 data-[state=active]:text-pink-900"
              >
                <Activity className="w-4 h-4 mr-2" />
                Exploración General
              </TabsTrigger>
              <TabsTrigger
                value="quality"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-teal-100 data-[state=active]:to-teal-200 data-[state=active]:text-teal-900"
              >
                <Shield className="w-4 h-4 mr-2" />
                Calidad de Datos
              </TabsTrigger>
              <TabsTrigger
                value="clinical"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-100 data-[state=active]:to-blue-200 data-[state=active]:text-blue-900"
              >
                <BarChart3 className="w-4 h-4 mr-2" />
                Factores Clínicos
              </TabsTrigger>
              <TabsTrigger
                value="correlations"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-green-100 data-[state=active]:to-green-200 data-[state=active]:text-green-900"
              >
                <Network className="w-4 h-4 mr-2" />
                Correlaciones
              </TabsTrigger>
              <TabsTrigger
                value="models"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-100 data-[state=active]:to-purple-200 data-[state=active]:text-purple-900"
              >
                <Brain className="w-4 h-4 mr-2" />
                Modelos ML
              </TabsTrigger>
              <TabsTrigger
                value="prediction"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-orange-100 data-[state=active]:to-orange-200 data-[state=active]:text-orange-900"
              >
                <Target className="w-4 h-4 mr-2" />
                Predicción
              </TabsTrigger>
            </TabsList>

            <TabsContent value="exploration" className="space-y-6">
              <DataSummary />
            </TabsContent>

            <TabsContent value="quality" className="space-y-6">
              <DataQuality />
            </TabsContent>

            <TabsContent value="clinical" className="space-y-6">
              <ClinicalFactors />
            </TabsContent>

            <TabsContent value="correlations" className="space-y-6">
              <CorrelationsView />
            </TabsContent>

            <TabsContent value="models" className="space-y-6">
              <MLModels />
            </TabsContent>

            <TabsContent value="prediction" className="space-y-6">
              <PredictionForm />
            </TabsContent>
          </Tabs>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white/80 backdrop-blur-sm border-t border-pink-200 mt-12">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-sm text-gray-600">
            Dashboard Clínico - Patrones de Comportamiento de Datos © 2025
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;

