# Guía de Pruebas - Dashboard Clínico

## Pre-requisitos para Pruebas

### 1. Configuración del Backend

```bash
cd backend

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

**Editar `backend/.env`:**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=http://localhost:3000
OPENAI_API_KEY=tu_clave_api_aqui
```

### 2. Configuración del Frontend

```bash
cd frontend

# Instalar dependencias
yarn install

# Crear archivo .env
```

**Crear `frontend/.env`:**
```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

### 3. Iniciar MongoDB

Asegúrate de que MongoDB esté corriendo:

```bash
# Windows (si está instalado como servicio)
net start MongoDB

# Linux/Mac
sudo systemctl start mongod
# o
mongod --dbpath /path/to/data
```

## Ejecución de Pruebas

### Paso 1: Iniciar el Backend

```bash
cd backend
venv\Scripts\activate  # Activar entorno virtual
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

**Verificar que el backend esté corriendo:**
- Abrir navegador en: `http://localhost:8000`
- Deberías ver: `{"message": "Breast Cancer Risk Factors Dashboard API"}`
- Documentación API: `http://localhost:8000/docs`

### Paso 2: Iniciar el Frontend

En una nueva terminal:

```bash
cd frontend
yarn start
```

**Verificar que el frontend esté corriendo:**
- El navegador debería abrirse automáticamente en: `http://localhost:3000`
- Deberías ver el dashboard con el componente de carga de archivos

## Casos de Prueba

### Test 1: Carga de Archivo CSV

**Objetivo**: Verificar que el sistema puede cargar y procesar archivos CSV

**Pasos**:
1. En el dashboard, arrastra el archivo `CubanDataset.csv` al área de carga
2. O haz clic en "Seleccionar Archivo" y elige `CubanDataset.csv`
3. Haz clic en "Cargar y Analizar Datos"

**Resultado Esperado**:
- Barra de progreso muestra el avance
- Mensaje de éxito: "¡Archivo cargado y procesado exitosamente!"
- El dashboard cambia a la vista de pestañas
- Se muestra información del dataset en el header

**Verificar en Backend**:
```bash
# En la terminal del backend deberías ver:
INFO:     POST /api/data/upload
INFO:     Loaded 1699 records from CubanDataset.csv
```

### Test 2: Exploración General

**Objetivo**: Verificar visualizaciones y estadísticas generales

**Pasos**:
1. Después de cargar datos, verifica que estés en la pestaña "Exploración General"
2. Observa las 3 tarjetas de métricas clave
3. Observa las 2 gráficas (distribución de diagnóstico y edad)
4. Haz clic en "Generar Insights"

**Resultado Esperado**:
- **Tarjeta 1**: Total de Registros = 1699
- **Tarjeta 2**: Edad Promedio ≈ 50-60 años
- **Tarjeta 3**: Casos Positivos (porcentaje de cáncer)
- **Gráfica 1**: Pie chart con distribución Yes/No
- **Gráfica 2**: Barras con grupos de edad (<30, 30-39, 40-49, 50-59, 60+)
- **Insights IA**: Texto generado por GPT-4 con análisis clínico

**Verificar**:
- Las gráficas son interactivas (hover muestra detalles)
- Los colores son pasteles (rosa, azul, verde)
- El texto de insights está en español

### Test 3: Factores Clínicos

**Objetivo**: Verificar análisis de variables clínicas

**Pasos**:
1. Haz clic en la pestaña "Factores Clínicos"
2. Observa la gráfica de BIRADS
3. Observa las gráficas de menopausia, lactancia, raza, clase histológica
4. Haz clic en las pestañas: Alcohol, Tabaco, Ejercicio, Estado Emocional

**Resultado Esperado**:
- **BIRADS**: Gráfica de barras con clasificaciones (1-6)
- **Menopausia**: Pie chart con estados
- **Lactancia**: Pie chart con historial
- **Raza**: Gráfica de barras
- **Clase Histológica**: Gráfica de barras
- **Factores adicionales**: Gráficas en pestañas

**Verificar**:
- Todas las gráficas se renderizan correctamente
- Los colores son consistentes con el tema
- Las gráficas son interactivas

### Test 4: Correlaciones y Patrones

**Objetivo**: Verificar análisis de correlaciones

**Pasos**:
1. Haz clic en la pestaña "Correlaciones y Patrones"
2. Observa el selector de método (Pearson por defecto)
3. Observa el heatmap de correlaciones
4. Observa la lista de correlaciones significativas
5. Cambia el método a "Spearman"
6. Haz clic en "Interpretar con IA"

**Resultado Esperado**:
- **Heatmap**: Matriz de colores (azul=negativo, blanco=cero, rosa=positivo)
- **Lista**: Pares de variables con |r| > 0.3
- **Cambio de método**: El heatmap se actualiza
- **Insights IA**: Interpretación clínica de las correlaciones

**Verificar**:
- El heatmap es interactivo (hover muestra valores)
- Las correlaciones están ordenadas por fuerza
- Los badges muestran la fuerza (strong/moderate/weak)
- El análisis de IA es relevante y en español

### Test 5: Exportar Resultados

**Objetivo**: Verificar exportación de datos y reportes

**Pasos**:
1. Haz clic en la pestaña "Exportar Resultados"
2. Haz clic en "Descargar CSV"
3. Haz clic en "Descargar JSON"
4. Haz clic en "Descargar Excel"
5. Haz clic en "Generar Reporte Clínico"
6. Espera a que se genere el reporte
7. Haz clic en "Descargar Reporte"

**Resultado Esperado**:
- **CSV**: Se descarga `breast_cancer_data.csv`
- **JSON**: Se descarga `breast_cancer_data.json`
- **Excel**: Se descarga `breast_cancer_data.xlsx`
- **Reporte**: Se muestra vista previa del reporte en Markdown
- **Descarga**: Se descarga `reporte_clinico.md`

**Verificar**:
- Los archivos se descargan correctamente
- Los datos en los archivos son correctos
- El reporte incluye: resumen ejecutivo, análisis demográfico, factores de riesgo, recomendaciones

### Test 6: Validación de Errores

**Objetivo**: Verificar manejo de errores

**Pasos**:
1. Intenta cargar un archivo que NO sea CSV
2. Intenta cargar un archivo CSV vacío
3. Desactiva la API de OpenAI (quita la clave del .env)
4. Intenta generar insights

**Resultado Esperado**:
- **Archivo no CSV**: Error "Por favor seleccione un archivo CSV válido"
- **Archivo vacío**: Error en el procesamiento
- **Sin API key**: Error "Error al generar insights con IA. Verifique la configuración de OpenAI API."

**Verificar**:
- Los mensajes de error son claros
- La aplicación no se rompe
- Se pueden recuperar de los errores

## Pruebas de API (Opcional)

### Usando la Documentación Interactiva

1. Abre `http://localhost:8000/docs`
2. Prueba cada endpoint:

**POST /api/data/upload**
- Sube `CubanDataset.csv`
- Verifica respuesta con `success: true`

**GET /api/data/summary**
- Verifica que retorna estadísticas

**GET /api/data/correlations**
- Prueba con `method=pearson`
- Prueba con `method=spearman`

**POST /api/ai/analyze-summary**
- Verifica que retorna insights

**GET /api/data/export/csv**
- Verifica que descarga CSV

### Usando cURL

```bash
# Health check
curl http://localhost:8000/

# Upload file
curl -X POST "http://localhost:8000/api/data/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@CubanDataset.csv"

# Get summary
curl http://localhost:8000/api/data/summary

# Get correlations
curl "http://localhost:8000/api/data/correlations?method=pearson"

# Export CSV
curl http://localhost:8000/api/data/export/csv -o output.csv
```

## Checklist de Pruebas

- [ ] Backend inicia sin errores
- [ ] Frontend inicia sin errores
- [ ] Carga de archivo CSV funciona
- [ ] Métricas clave se muestran correctamente
- [ ] Gráficas de distribución se renderizan
- [ ] Insights de IA se generan correctamente
- [ ] Factores clínicos se visualizan
- [ ] Heatmap de correlaciones funciona
- [ ] Cambio de método de correlación funciona
- [ ] Interpretación de correlaciones con IA funciona
- [ ] Exportación a CSV funciona
- [ ] Exportación a JSON funciona
- [ ] Exportación a Excel funciona
- [ ] Generación de reporte clínico funciona
- [ ] Descarga de reporte funciona
- [ ] Manejo de errores funciona
- [ ] Tema visual es consistente (colores pasteles)
- [ ] Interfaz es responsiva

## Problemas Comunes y Soluciones

### Error: "Cannot connect to backend"
**Solución**: Verifica que el backend esté corriendo en puerto 8000

### Error: "CORS policy"
**Solución**: Verifica que `CORS_ORIGINS` en `.env` incluya `http://localhost:3000`

### Error: "OpenAI API key not found"
**Solución**: Agrega tu clave de OpenAI en `backend/.env`

### Error: "Module not found"
**Solución**: 
- Backend: `pip install -r requirements.txt`
- Frontend: `yarn install`

### Gráficas no se muestran
**Solución**: Verifica que `react-plotly.js` y `plotly.js` estén instalados

### MongoDB connection error
**Solución**: Verifica que MongoDB esté corriendo y la URL en `.env` sea correcta

## Métricas de Éxito

✅ **Todas las pruebas pasan**
✅ **No hay errores en consola**
✅ **Las visualizaciones son claras y útiles**
✅ **Los insights de IA son relevantes**
✅ **La exportación funciona correctamente**
✅ **El tema visual es consistente**
✅ **La aplicación es responsiva**

## Siguiente Paso

Una vez que todas las pruebas pasen, el dashboard está listo para:
- Despliegue en producción
- Pruebas con usuarios reales
- Optimización de rendimiento
- Agregar nuevas funcionalidades

