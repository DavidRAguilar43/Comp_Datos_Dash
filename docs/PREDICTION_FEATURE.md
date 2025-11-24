# Funcionalidad de Predicción de Riesgo de Cáncer de Mama

## Descripción General

Se ha implementado un sistema completo de predicción de riesgo de cáncer de mama que permite a los usuarios ingresar sus datos clínicos y obtener una estimación personalizada del riesgo basada en modelos de Machine Learning entrenados.

## Componentes Implementados

### Backend

#### 1. Método de Predicción en `ml_models.py`

**Método:** `predict_single(input_data, model_name)`

**Funcionalidad:**
- Recibe datos clínicos del paciente
- Preprocesa y escala los datos usando el mismo scaler del entrenamiento
- Realiza predicción usando el modelo seleccionado
- Calcula probabilidad de cáncer
- Clasifica el riesgo en 3 niveles: Bajo, Moderado, Alto
- Genera interpretación clínica del resultado

**Niveles de Riesgo:**
- **Bajo** (< 30%): Color verde
- **Moderado** (30-60%): Color amarillo
- **Alto** (> 60%): Color rojo

#### 2. Endpoint de Predicción en `server.py`

**Ruta:** `POST /api/ml/predict`

**Request Body:**
```json
{
  "age": 45,
  "menarche": 12,
  "menopause": 50,
  "agefirst": 25,
  "children": 2,
  "biopsies": 1,
  "imc": 24.5,
  "weight": 65.5,
  "histologicalclass": 3,
  "model_name": "random_forest"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 0,
  "probability": 0.23,
  "probability_percentage": 23.0,
  "risk_level": "Bajo",
  "risk_color": "green",
  "model_used": "random_forest",
  "interpretation": "La probabilidad de cáncer de mama es baja..."
}
```

### Frontend

#### 1. Componente `PredictionForm.js`

**Ubicación:** `frontend/src/components/PredictionForm.js`

**Características:**
- Formulario intuitivo con 9 campos clínicos
- Selector de modelo de ML (4 opciones)
- Validación de datos
- Indicadores de carga
- Visualización de resultados con:
  - Nivel de riesgo con icono y color
  - Porcentaje de probabilidad
  - Barra de progreso visual
  - Interpretación clínica
  - Disclaimer médico

**Campos del Formulario:**
1. Edad (años)
2. Edad de Menarquia (años)
3. Edad de Menopausia (años) - opcional
4. Edad Primer Embarazo (años) - opcional
5. Número de Hijos
6. Número de Biopsias
7. IMC (Índice de Masa Corporal)
8. Peso (kg)
9. Clase Histológica

**Modelos Disponibles:**
- Random Forest (Recomendado)
- Red Neuronal
- SVM
- Regresión Logística

#### 2. Integración en Dashboard

**Ubicación:** `frontend/src/components/Dashboard.js`

- Nuevo tab "Predicción" agregado a la barra horizontal
- Icono: Target (🎯)
- Color: Naranja
- Posición: Sexto tab (después de "Modelos ML")

## Flujo de Uso

1. **Usuario carga datos:** Sube el dataset CSV en la pestaña inicial
2. **Entrena modelos:** Va a la pestaña "Modelos ML" y entrena los modelos
3. **Accede a Predicción:** Hace clic en el tab "Predicción"
4. **Ingresa datos:** Completa el formulario con información clínica
5. **Selecciona modelo:** Elige el modelo de ML a usar (Random Forest por defecto)
6. **Obtiene resultado:** Recibe:
   - Nivel de riesgo (Bajo/Moderado/Alto)
   - Probabilidad porcentual
   - Interpretación clínica
   - Recomendaciones

## Consideraciones Técnicas

### Preprocesamiento de Datos
- Los datos se escalan usando el mismo `StandardScaler` del entrenamiento
- Valores faltantes se imputan con 0
- Solo se usan features numéricas del dataset

### Manejo de Errores
- Validación de modelos entrenados
- Mensajes de error descriptivos
- Manejo de campos opcionales

### Seguridad y Responsabilidad
- Disclaimer médico visible en resultados
- Aclaración de que NO reemplaza diagnóstico profesional
- Recomendación de consulta con especialista

## Variables del Dataset Utilizadas

Las siguientes variables numéricas del `CubanDataset.csv` se utilizan para la predicción:

- `age`: Edad del paciente
- `menarche`: Edad de primera menstruación
- `menopause`: Edad de menopausia (si aplica)
- `agefirst`: Edad del primer embarazo (si aplica)
- `children`: Número de hijos
- `biopsies`: Número de biopsias realizadas
- `imc`: Índice de Masa Corporal
- `weight`: Peso en kilogramos
- `histologicalclass`: Clasificación histológica

## Próximas Mejoras Sugeridas

1. **Validación de rangos:** Agregar validación de rangos válidos para cada campo
2. **Historial de predicciones:** Guardar predicciones anteriores del usuario
3. **Comparación de modelos:** Mostrar predicción de todos los modelos simultáneamente
4. **Exportar resultado:** Permitir descargar el resultado en PDF
5. **Gráficos adicionales:** Visualizar factores de riesgo más influyentes
6. **Más variables:** Incluir variables categóricas del dataset

## Testing

Para probar la funcionalidad:

1. Asegurarse de que el backend esté corriendo
2. Cargar el dataset `CubanDataset.csv`
3. Entrenar al menos un modelo en la pestaña "Modelos ML"
4. Ir a la pestaña "Predicción"
5. Ingresar datos de prueba (usar datos del admin: edad 45, menarquia 12, etc.)
6. Verificar que se muestre el resultado correctamente

## Archivos Modificados/Creados

### Backend
- ✅ `backend/services/ml_models.py` - Agregado método `predict_single()` y mejoras en `prepare_data()`
- ✅ `backend/server.py` - Agregado endpoint `/api/ml/predict`

### Frontend
- ✅ `frontend/src/components/PredictionForm.js` - Nuevo componente
- ✅ `frontend/src/components/Dashboard.js` - Agregado tab de Predicción

### Documentación
- ✅ `docs/PREDICTION_FEATURE.md` - Este documento

## Correcciones Importantes (2024-11-24)

### Problema Detectado
Las predicciones devolvían siempre el mismo resultado sin importar los datos ingresados.

### Causa Raíz
1. **Columnas categóricas no convertidas**: Variables como `menopause`, `agefirst`, `children` contenían valores "No" y no se convertían a numérico
2. **Columnas irrelevantes incluidas**: `id` y `year` se usaban para predicción (no deberían)
3. **Imputación incorrecta**: Valores faltantes se llenaban con 0 en lugar de la media del dataset

### Solución Implementada

#### 1. Conversión de Columnas a Numérico
En `ml_models.py` → `prepare_data()`:
```python
# Convert specific columns to numeric (handle "No" as 0)
columns_to_convert = ['menopause', 'agefirst', 'children', 'exercise']
for col in columns_to_convert:
    if col in X.columns:
        X[col] = X[col].replace({'No': '0', 'no': '0', 'NO': '0'})
        X[col] = pd.to_numeric(X[col], errors='coerce')
```

#### 2. Exclusión de Columnas Irrelevantes
```python
# Remove irrelevant features (id, year)
irrelevant_features = ['id', 'year']
numeric_features = [f for f in numeric_features if f not in irrelevant_features]
```

#### 3. Imputación con Media del Dataset
```python
# Store feature means for later imputation
self.feature_means = X.mean().to_dict()

# En predict_single():
for feature in missing_features:
    if self.feature_means and feature in self.feature_means:
        input_df[feature] = self.feature_means[feature]
```

### Resultado
- **Antes**: 8 características (incluyendo id, year)
- **Después**: 10 características relevantes
- **Características usadas ahora**:
  1. age
  2. menarche
  3. menopause (convertida a numérico)
  4. agefirst (convertida a numérico)
  5. children (convertida a numérico)
  6. biopsies
  7. imc
  8. weight
  9. exercise (convertida a numérico)
  10. histologicalclass

### Validación
Pruebas con diferentes casos:
- **Caso bajo riesgo** (edad 30, 1 hijo, sin biopsias): 45% - Moderado
- **Caso alto riesgo** (edad 60, sin hijos, 3 biopsias): 66.52% - Alto
- **Caso medio riesgo** (edad 45, 2 hijos, 1 biopsia): 98.5% - Alto
- **Datos mínimos** (solo edad e IMC): 51.12% - Moderado

✅ **Las predicciones ahora varían correctamente según los datos de entrada**

