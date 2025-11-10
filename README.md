# Dashboard Clínico - Factores de Riesgo de Cáncer de Mama

Dashboard interactivo para análisis de factores de riesgo de cáncer de mama en mujeres cubanas, desarrollado con React, FastAPI y análisis con IA (GPT-4).

## 🎯 Características

- **Carga y procesamiento de datos CSV** con limpieza automática
- **Análisis estadístico completo** (descriptivas, correlaciones, distribuciones)
- **Visualizaciones interactivas** con Plotly (gráficas de barras, pie charts, heatmaps)
- **Insights generados por IA** usando GPT-4 para análisis clínico automático
- **Interfaz por pestañas**:
  - 📊 Exploración General
  - 🎗️ Factores Clínicos
  - 📈 Correlaciones y Patrones
  - 📋 Exportar Resultados
- **Exportación de datos** en CSV, JSON y Excel
- **Reportes clínicos completos** generados automáticamente con IA
- **Tema médico pastel** (rosa, azul, verde menta)

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno para Python
- **Pandas & NumPy** - Procesamiento y análisis de datos
- **SciPy** - Análisis estadístico avanzado
- **OpenAI GPT-4** - Generación de insights clínicos
- **Motor** - Driver asíncrono de MongoDB
- **Plotly** - Visualizaciones de datos

### Frontend
- **React** - Biblioteca de UI
- **shadcn/ui** - Componentes UI modernos
- **Tailwind CSS** - Estilos utility-first
- **Plotly.js** - Gráficas interactivas
- **Axios** - Cliente HTTP

## 📋 Requisitos Previos

- **Python 3.10+**
- **Node.js 16+** y **Yarn**
- **MongoDB** (local o en la nube)
- **Clave API de OpenAI** (para funcionalidades de IA)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
cd Comp_Datos_Dash
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

**Configuración del archivo `.env`:**

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=http://localhost:3000
OPENAI_API_KEY=tu_clave_api_de_openai
```

### 3. Configurar Frontend

```bash
cd ../frontend

# Instalar dependencias
yarn install

# Configurar variables de entorno
# Crear archivo .env en frontend/
```

**Crear archivo `frontend/.env`:**

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

## ▶️ Ejecución

### Iniciar Backend

```bash
cd backend
# Asegúrate de que el entorno virtual esté activado
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`
Documentación API: `http://localhost:8000/docs`

### Iniciar Frontend

```bash
cd frontend
yarn start
```

El frontend estará disponible en: `http://localhost:3000`

## 📊 Uso del Dashboard

### 1. Cargar Datos

1. Accede al dashboard en `http://localhost:3000`
2. Arrastra o selecciona un archivo CSV con datos de pacientes
3. El sistema procesará y limpiará automáticamente los datos

### 2. Exploración General

- Visualiza métricas clave (total de registros, edad promedio, casos positivos)
- Observa distribuciones de diagnóstico y edad
- Genera insights automáticos con IA

### 3. Factores Clínicos

- Analiza clasificación BIRADS
- Revisa distribuciones de menopausia, lactancia, raza
- Explora factores de riesgo adicionales (alcohol, tabaco, ejercicio)

### 4. Correlaciones y Patrones

- Visualiza mapa de calor de correlaciones
- Identifica correlaciones significativas
- Obtén interpretación clínica con IA

### 5. Exportar Resultados

- Descarga datos procesados en CSV, JSON o Excel
- Genera y descarga reporte clínico completo en Markdown

## 📁 Estructura del Proyecto

```
Comp_Datos_Dash/
├── backend/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_processor.py    # Procesamiento de datos
│   │   └── ai_analyzer.py       # Análisis con IA
│   ├── server.py                # API FastAPI
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── FileUploader.js
│   │   │   ├── DataSummary.js
│   │   │   ├── ClinicalFactors.js
│   │   │   ├── CorrelationsView.js
│   │   │   └── ExportPanel.js
│   │   ├── App.js
│   │   └── index.css
│   ├── package.json
│   └── .env
└── README.md
```

## 🔑 Variables del Dataset

El dashboard espera un CSV con las siguientes columnas:

- `id` - Identificador único
- `age` - Edad de la paciente
- `menarche` - Edad de menarquia
- `menopause` - Estado/edad de menopausia
- `agefirst` - Edad del primer embarazo
- `children` - Número de hijos
- `breastfeeding` - Historial de lactancia
- `nrelbc` - Familiares con cáncer de mama
- `biopsies` - Número de biopsias
- `hyperplasia` - Presencia de hiperplasia
- `race` - Grupo étnico
- `year` - Año del diagnóstico
- `imc` - Índice de masa corporal
- `weight` - Peso
- `exercise` - Frecuencia de ejercicio
- `alcohol` - Consumo de alcohol
- `tobacco` - Consumo de tabaco
- `allergies` - Alergias
- `emotional` - Estado emocional
- `depressive` - Estado depresivo
- `histologicalclass` - Clasificación histológica
- `birads` - Clasificación BI-RADS
- `cancer` - Diagnóstico de cáncer (Yes/No)

## 🤖 Funcionalidades de IA

El dashboard utiliza GPT-4 para:

1. **Análisis de Estadísticas**: Genera insights sobre patrones demográficos y clínicos
2. **Interpretación de Correlaciones**: Explica el significado clínico de las correlaciones encontradas
3. **Reportes Clínicos**: Crea reportes profesionales con:
   - Resumen ejecutivo
   - Perfil demográfico
   - Factores de riesgo identificados
   - Patrones y tendencias
   - Recomendaciones para investigación

## 🎨 Tema Visual

El dashboard utiliza una paleta de colores pasteles apropiada para contexto médico:

- **Rosa claro** (#f472b6) - Principal
- **Azul suave** (#93c5fd) - Secundario
- **Verde menta** (#86efac) - Acento
- **Amarillo pastel** (#fcd34d) - Complementario
- **Lavanda** (#c4b5fd) - Complementario

## 📝 Notas de Desarrollo

- El backend usa procesamiento asíncrono para mejor rendimiento
- Los datos se limpian automáticamente (duplicados, valores nulos, normalización)
- Soporta archivos CSV de hasta 50MB
- Las visualizaciones son completamente interactivas y responsivas
- El sistema está optimizado para despliegue en la nube

## 🚢 Despliegue

### Backend (Render, Railway, etc.)

1. Configurar variables de entorno en la plataforma
2. Comando de inicio: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel, Netlify, etc.)

1. Configurar `REACT_APP_BACKEND_URL` con la URL del backend desplegado
2. Comando de build: `yarn build`
3. Directorio de publicación: `build`

## 📄 Licencia

Este proyecto es parte de un trabajo académico sobre "Patrones de comportamiento de datos: factores de riesgo de cáncer de mama en mujeres cubanas".

## 👥 Autor

Desarrollado como parte del proyecto final de Patrones de Comportamiento de Datos.

---

**¡Dashboard listo para análisis clínico profesional! 🎗️**
