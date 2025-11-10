# Estructura del Proyecto - Dashboard Clínico

## Descripción General

Dashboard web para análisis de factores de riesgo de cáncer de mama en mujeres cubanas. Arquitectura full-stack con React + FastAPI + MongoDB, integración con OpenAI GPT-4 para análisis automático.

## Arquitectura

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  React Frontend │ ◄─────► │  FastAPI Backend│ ◄─────► │   MongoDB       │
│  (Port 3000)    │  HTTP   │  (Port 8000)    │         │                 │
│                 │         │                 │         │                 │
└─────────────────┘         └────────┬────────┘         └─────────────────┘
                                     │
                                     │ API Calls
                                     ▼
                            ┌─────────────────┐
                            │   OpenAI GPT-4  │
                            │   (AI Analysis) │
                            └─────────────────┘
```

## Estructura de Carpetas

```
Comp_Datos_Dash/
│
├── backend/                          # Backend FastAPI
│   ├── services/                     # Servicios de negocio
│   │   ├── __init__.py
│   │   ├── data_processor.py        # Procesamiento de datos CSV
│   │   └── ai_analyzer.py           # Análisis con OpenAI GPT-4
│   │
│   ├── server.py                     # Aplicación FastAPI principal
│   ├── requirements.txt              # Dependencias Python
│   └── .env.example                  # Variables de entorno de ejemplo
│
├── frontend/                         # Frontend React
│   ├── public/                       # Archivos estáticos
│   │
│   ├── src/
│   │   ├── components/               # Componentes React
│   │   │   ├── ui/                   # Componentes shadcn/ui
│   │   │   │   ├── button.jsx
│   │   │   │   ├── card.jsx
│   │   │   │   ├── tabs.jsx
│   │   │   │   ├── alert.jsx
│   │   │   │   ├── badge.jsx
│   │   │   │   ├── progress.jsx
│   │   │   │   ├── select.jsx
│   │   │   │   ├── skeleton.jsx
│   │   │   │   └── ... (otros componentes UI)
│   │   │   │
│   │   │   ├── Dashboard.js          # Componente principal del dashboard
│   │   │   ├── FileUploader.js       # Carga de archivos CSV
│   │   │   ├── DataSummary.js        # Resumen estadístico y visualizaciones
│   │   │   ├── ClinicalFactors.js    # Análisis de factores clínicos
│   │   │   ├── CorrelationsView.js   # Visualización de correlaciones
│   │   │   └── ExportPanel.js        # Exportación de datos y reportes
│   │   │
│   │   ├── App.js                    # Componente raíz de la aplicación
│   │   ├── App.css                   # Estilos de la aplicación
│   │   ├── index.js                  # Punto de entrada
│   │   └── index.css                 # Estilos globales y tema
│   │
│   ├── package.json                  # Dependencias Node.js
│   ├── tailwind.config.js            # Configuración de Tailwind CSS
│   ├── craco.config.js               # Configuración de CRACO
│   └── .env                          # Variables de entorno (crear)
│
├── CubanDataset.csv                  # Dataset de ejemplo
├── README.md                         # Documentación principal
└── ProjectStructure.md               # Este archivo
```

## Componentes del Backend

### 1. `server.py`
**Responsabilidad**: API REST principal con FastAPI

**Endpoints**:
- `GET /` - Health check
- `POST /api/data/upload` - Cargar y procesar CSV
- `GET /api/data/summary` - Obtener resumen estadístico
- `GET /api/data/correlations` - Obtener matriz de correlaciones
- `GET /api/data/preview` - Vista previa de datos
- `POST /api/ai/analyze-summary` - Análisis de resumen con IA
- `POST /api/ai/analyze-correlations` - Análisis de correlaciones con IA
- `POST /api/ai/generate-report` - Generar reporte clínico completo
- `GET /api/data/export/{format}` - Exportar datos (csv/json/excel)

**Tecnologías**:
- FastAPI
- Motor (MongoDB async driver)
- CORS middleware

### 2. `services/data_processor.py`
**Responsabilidad**: Procesamiento y análisis de datos

**Clase Principal**: `DataProcessor`

**Métodos**:
- `load_from_bytes(file_bytes, filename)` - Cargar CSV desde bytes
- `clean_data()` - Limpiar datos (duplicados, nulos, normalización)
- `get_summary_statistics()` - Calcular estadísticas descriptivas
- `get_correlations(method)` - Calcular correlaciones (Pearson/Spearman/Kendall)
- `get_data_preview(n_rows)` - Obtener vista previa
- `export_to_dict()` - Exportar a diccionario
- `_get_age_groups()` - Agrupar por edad
- `_normalize_yes_no(value)` - Normalizar valores Yes/No

**Tecnologías**:
- pandas
- numpy
- scipy

### 3. `services/ai_analyzer.py`
**Responsabilidad**: Análisis con IA usando OpenAI GPT-4

**Clase Principal**: `AIAnalyzer`

**Métodos**:
- `analyze_summary_statistics(summary_data)` - Analizar estadísticas
- `analyze_correlations(correlations_data)` - Interpretar correlaciones
- `generate_clinical_report(summary_data, correlations_data)` - Generar reporte completo

**Tecnologías**:
- OpenAI Python SDK
- GPT-4o model

## Componentes del Frontend

### 1. `Dashboard.js`
**Responsabilidad**: Componente principal con navegación por pestañas

**Estado**:
- `dataLoaded` - Indica si hay datos cargados
- `uploadInfo` - Información del archivo cargado
- `activeTab` - Pestaña activa

**Pestañas**:
1. Exploración General
2. Factores Clínicos
3. Correlaciones y Patrones
4. Exportar Resultados

### 2. `FileUploader.js`
**Responsabilidad**: Carga de archivos CSV

**Características**:
- Drag & drop
- Validación de formato y tamaño (max 50MB)
- Barra de progreso
- Mensajes de error/éxito

### 3. `DataSummary.js`
**Responsabilidad**: Visualización de estadísticas generales

**Visualizaciones**:
- Cards con métricas clave
- Gráfica de pie (distribución de diagnóstico)
- Gráfica de barras (distribución por edad)
- Panel de insights con IA

### 4. `ClinicalFactors.js`
**Responsabilidad**: Análisis de factores clínicos

**Visualizaciones**:
- Gráfica de barras (clasificación BIRADS)
- Gráficas de pie (menopausia, lactancia, raza)
- Gráficas de barras (clase histológica)
- Pestañas para factores adicionales (alcohol, tabaco, ejercicio, estado emocional)

### 5. `CorrelationsView.js`
**Responsabilidad**: Análisis de correlaciones

**Características**:
- Selector de método (Pearson/Spearman/Kendall)
- Heatmap de correlaciones
- Lista de correlaciones significativas
- Interpretación con IA

### 6. `ExportPanel.js`
**Responsabilidad**: Exportación de datos y reportes

**Funcionalidades**:
- Exportar datos en CSV, JSON, Excel
- Generar reporte clínico con IA
- Descargar reporte en Markdown

## Flujo de Datos

### 1. Carga de Datos
```
Usuario → FileUploader → POST /api/data/upload → DataProcessor.load_from_bytes()
                                                → DataProcessor.clean_data()
                                                → Respuesta con info del dataset
```

### 2. Visualización de Resumen
```
DataSummary → GET /api/data/summary → DataProcessor.get_summary_statistics()
                                    → Respuesta con estadísticas
                                    → Renderizar gráficas con Plotly
```

### 3. Análisis con IA
```
Usuario → Botón "Generar Insights" → POST /api/ai/analyze-summary
                                    → AIAnalyzer.analyze_summary_statistics()
                                    → OpenAI GPT-4 API
                                    → Respuesta con insights
```

### 4. Exportación
```
Usuario → Botón "Descargar CSV" → GET /api/data/export/csv
                                 → DataProcessor.export_to_dict()
                                 → pandas.to_csv()
                                 → StreamingResponse con archivo
```

## Tecnologías y Librerías

### Backend
| Librería | Versión | Propósito |
|----------|---------|-----------|
| fastapi | Latest | Framework web |
| uvicorn | Latest | Servidor ASGI |
| motor | Latest | MongoDB async driver |
| pandas | Latest | Procesamiento de datos |
| numpy | Latest | Operaciones numéricas |
| scipy | Latest | Análisis estadístico |
| plotly | Latest | Visualizaciones |
| openai | Latest | API de OpenAI |
| openpyxl | Latest | Exportación a Excel |
| python-multipart | Latest | Manejo de archivos |

### Frontend
| Librería | Versión | Propósito |
|----------|---------|-----------|
| react | 19.0.0 | Framework UI |
| react-router-dom | 7.5.1 | Enrutamiento |
| axios | 1.8.4 | Cliente HTTP |
| plotly.js | 3.2.0 | Gráficas |
| react-plotly.js | 2.6.0 | Wrapper de Plotly para React |
| lucide-react | 0.507.0 | Iconos |
| tailwindcss | 3.4.17 | Estilos utility-first |
| @radix-ui/* | Latest | Componentes UI primitivos |
| class-variance-authority | 0.7.1 | Variantes de componentes |
| clsx | 2.1.1 | Utilidad para clases CSS |

## Variables de Entorno

### Backend (`.env`)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=http://localhost:3000
OPENAI_API_KEY=sk-...
```

### Frontend (`.env`)
```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

## Tema Visual

### Paleta de Colores Pastel
- **Rosa claro**: `#f472b6` (primary)
- **Azul suave**: `#93c5fd` (secondary)
- **Verde menta**: `#86efac` (accent)
- **Amarillo pastel**: `#fcd34d` (complementary)
- **Lavanda**: `#c4b5fd` (complementary)

### Gradientes
- Background principal: `from-pink-50 via-blue-50 to-green-50`
- Botones IA: `from-purple-500 to-pink-500`
- Cards: `from-{color}-50 to-white`

## Comandos Útiles

### Backend
```bash
# Activar entorno virtual
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Instalar dependencias
cd frontend
yarn install

# Ejecutar en desarrollo
yarn start

# Build para producción
yarn build
```

## Próximos Pasos

- [ ] Implementar filtros interactivos
- [ ] Agregar más visualizaciones (boxplots, scatter plots)
- [ ] Implementar caché para análisis de IA
- [ ] Agregar tests unitarios
- [ ] Optimizar rendimiento para datasets grandes
- [ ] Implementar autenticación de usuarios
- [ ] Agregar soporte para múltiples idiomas
- [ ] Crear documentación de API con Swagger

## Notas de Desarrollo

- Los datos NO se almacenan en MongoDB, solo se procesan en memoria
- El sistema soporta archivos CSV de hasta 50MB
- Las visualizaciones son completamente responsivas
- Todos los prompts de IA están en español para contexto médico
- El código sigue PEP-8 (Python) y estándares de React

