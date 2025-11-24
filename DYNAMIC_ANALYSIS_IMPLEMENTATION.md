# Implementación de Análisis Dinámico con IA

## Resumen

Se ha implementado un sistema completo de análisis dinámico que permite al dashboard adaptarse automáticamente a cualquier dataset de cáncer de mama que el usuario suba. El sistema utiliza IA (GPT-4o) para analizar la estructura del dataset y generar visualizaciones apropiadas.

## Cambios Realizados

### Backend

#### 1. Nuevo Servicio: `dataset_structure_analyzer.py`
- **Ubicación**: `backend/services/dataset_structure_analyzer.py`
- **Funcionalidad**:
  - Analiza automáticamente la estructura de cualquier CSV
  - Detecta tipos de columnas: numeric_continuous, numeric_discrete, categorical, binary, date, text
  - Recomienda visualizaciones apropiadas: pie, bar, scatter, line, box, heatmap
  - Identifica variables clave y variables objetivo
  - Genera configuración de visualización para el frontend

#### 2. Modificaciones en `data_processor.py`
- **Nuevos métodos**:
  - `get_dynamic_summary_statistics()`: Genera estadísticas basadas en columnas detectadas
  - `get_dynamic_correlations()`: Calcula correlaciones entre variables numéricas detectadas
- **Líneas agregadas**: 143 líneas (760-902)

#### 3. Modificaciones en `server.py`
- **Endpoint modificado**: `POST /api/data/upload`
  - Ahora incluye análisis automático de estructura al subir CSV
  - Retorna `structure_analysis` y `visualization_config` en la respuesta
  
- **Nuevos endpoints**:
  - `GET /api/data/structure-analysis`: Obtiene análisis de estructura del dataset actual
  - `POST /api/data/dynamic-summary`: Genera estadísticas dinámicas basadas en análisis
  - `POST /api/data/dynamic-correlations`: Calcula correlaciones dinámicas

### Frontend

#### 1. Nuevo Componente: `DynamicVisualization.js`
- **Ubicación**: `frontend/src/components/DynamicVisualization.js`
- **Funcionalidad**:
  - Genera gráficas dinámicamente basándose en configuración de IA
  - Soporta 6 tipos de visualizaciones:
    - Pie charts (distribuciones)
    - Bar charts (categorías)
    - Scatter plots (correlaciones)
    - Line charts (tendencias)
    - Box plots (distribuciones)
    - Heatmaps (matrices de correlación)

#### 2. Modificaciones en `Dashboard.js`
- **Nuevos estados**:
  - `structureAnalysis`: Almacena análisis de estructura del dataset
  - `visualizationConfig`: Almacena configuración de visualizaciones
- **Props pasados a componentes hijos**:
  - DataSummary, ClinicalFactors, CorrelationsView reciben análisis de estructura

#### 3. Modificaciones en `DataSummary.js`
- **Nuevas funcionalidades**:
  - Detecta si hay análisis de estructura disponible
  - Usa endpoint dinámico cuando está disponible
  - Muestra indicador visual de "Análisis Dinámico Activado"
  - Genera tarjetas de métricas adaptadas al dataset
  - Renderiza visualizaciones dinámicas basadas en recomendaciones de IA
  - Fallback a visualizaciones estáticas si no hay análisis disponible

#### 4. Modificaciones en `CorrelationsView.js`
- **Nuevas funcionalidades**:
  - Usa endpoint dinámico de correlaciones cuando está disponible
  - Calcula correlaciones solo entre variables numéricas detectadas
  - Muestra indicador de análisis dinámico
  - Adapta heatmap al número variable de columnas

## Flujo de Trabajo

### 1. Usuario sube CSV
```
Usuario → FileUploader → POST /api/data/upload
```

### 2. Backend procesa y analiza
```
server.py → DataProcessor.load_data()
         → DatasetStructureAnalyzer.analyze_dataset_structure()
         → GPT-4o analiza columnas y recomienda visualizaciones
         → Retorna: data_info + structure_analysis + visualization_config
```

### 3. Frontend almacena análisis
```
Dashboard.handleDataUploaded() → setStructureAnalysis()
                                → setVisualizationConfig()
```

### 4. Componentes usan análisis dinámico
```
DataSummary → POST /api/data/dynamic-summary → Estadísticas adaptadas
CorrelationsView → POST /api/data/dynamic-correlations → Correlaciones adaptadas
DynamicVisualization → Renderiza gráficas según recomendaciones
```

## Tipos de Columnas Detectadas

- **numeric_continuous**: Variables numéricas continuas (ej: edad, peso)
- **numeric_discrete**: Variables numéricas discretas (ej: número de hijos)
- **categorical**: Variables categóricas (ej: tipo de tumor)
- **binary**: Variables binarias (ej: diagnóstico Yes/No)
- **date**: Fechas
- **text**: Texto libre

## Visualizaciones Recomendadas

| Tipo de Análisis | Visualización | Uso |
|------------------|---------------|-----|
| Distribución categórica | Pie Chart | Proporciones de categorías |
| Comparación categórica | Bar Chart | Comparar valores entre categorías |
| Correlación numérica | Scatter Plot | Relación entre 2 variables numéricas |
| Tendencia temporal | Line Chart | Evolución en el tiempo |
| Distribución numérica | Box Plot | Distribución y outliers |
| Matriz de correlación | Heatmap | Correlaciones múltiples |

## Configuración Requerida

### Variables de Entorno
```bash
OPENAI_API_KEY=sk-... # o sk-or-v1-... para OpenRouter
```

### Dependencias Backend
- openai>=1.0.0
- pandas
- numpy
- scipy

### Dependencias Frontend
- react-plotly.js
- plotly.js

## Próximos Pasos

1. **Testing con diferentes datasets** (Tarea pendiente)
   - Probar con datasets de diferentes estructuras
   - Validar detección correcta de columnas
   - Verificar visualizaciones apropiadas

2. **Mejoras potenciales**:
   - Cache de análisis de estructura
   - Permitir al usuario editar tipos de columnas detectados
   - Agregar más tipos de visualizaciones
   - Soporte para datasets muy grandes (>100k filas)

## Notas Técnicas

- El análisis de estructura es **opcional**: si no hay API key de OpenAI, el sistema funciona con visualizaciones estáticas
- Los datos **no se almacenan en MongoDB**: todo el procesamiento es en memoria
- El análisis de IA se ejecuta **una sola vez** al subir el CSV
- Las visualizaciones dinámicas tienen **fallback** a estáticas si falla el análisis

