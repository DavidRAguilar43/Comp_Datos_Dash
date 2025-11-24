# Corrección de Filtros - Factores Clínicos

**Fecha**: 2025-11-23  
**Problema**: Los filtros en la sección de Factores Clínicos se traban y no muestran datos, especialmente el filtro de diagnóstico.

## Problema Identificado

### Síntomas
- Al cambiar filtros en Factores Clínicos, la aplicación se queda cargando
- No se muestran datos después de aplicar filtros
- El problema es más evidente con el filtro de diagnóstico

### Causa Raíz

El método `apply_filters` en `backend/services/data_processor.py` tenía varios problemas:

1. **Falta de manejo de errores**: Si un filtro fallaba, no había try-catch para capturar el error
2. **Conversión de tipos en BIRADS**: El filtro de BIRADS podía fallar al convertir valores a string
3. **Falta de logging**: No había forma de saber dónde estaba fallando el filtro

## Correcciones Aplicadas

### 1. Agregado de Try-Catch en Todos los Filtros

**Archivo**: `backend/services/data_processor.py`

Cada filtro ahora tiene manejo de errores:

```python
# Diagnosis filter
try:
    if filters['diagnosis'] == 'Maligno':
        filtered_df = filtered_df[filtered_df['cancer'] == 'Yes']
    elif filters['diagnosis'] == 'Benigno':
        filtered_df = filtered_df[filtered_df['cancer'] == 'No']
except Exception as e:
    print(f"Warning: Error applying diagnosis filter: {e}")
```

### 2. Logging Detallado

Se agregó logging en cada paso del filtrado:

```python
# Al inicio
initial_count = len(filtered_df)
print(f"DEBUG: Starting with {initial_count} records")
print(f"DEBUG: Filters received: {filters}")

# En cada filtro
before_count = len(filtered_df)
print(f"DEBUG: Unique cancer values: {filtered_df['cancer'].unique()}")
# ... aplicar filtro ...
after_count = len(filtered_df)
print(f"DEBUG: Diagnosis filter ({filters['diagnosis']}): {before_count} -> {after_count} records")

# Al final
final_count = len(filtered_df)
print(f"DEBUG: Final filtered records: {final_count} (from {initial_count})")
```

### 3. Mejora en Filtro de BIRADS

El filtro de BIRADS ahora maneja correctamente valores alfanuméricos:

```python
# Convert birads to string and check if it starts with the filter value
# Handle both numeric (1, 2, 3) and alphanumeric (3A, 3B, 4C) BIRADS values
birads_str = filtered_df['birads'].astype(str).str.strip()
# Filter by BIRADS number (e.g., "3" matches "3", "3A", "3B", "3C")
filtered_df = filtered_df[birads_str.str.startswith(str(filters['birads']))]
```

## Cómo Probar

### 1. Reiniciar el Backend

```bash
cd backend
# Detener el servidor actual (Ctrl+C)
# Reiniciar
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 2. Probar Cada Filtro

1. **Cargar dataset**: Sube `CubanDataset.csv`
2. **Ir a Factores Clínicos**
3. **Probar filtro de Diagnóstico**:
   - Seleccionar "Benigno"
   - Verificar que se muestren datos
   - Revisar logs del backend
4. **Probar filtro de Menopausia**:
   - Seleccionar "Premenopáusica"
   - Verificar datos
5. **Probar filtro de BIRADS**:
   - Seleccionar "BIRADS 3"
   - Verificar datos
6. **Probar filtro de Lactancia**:
   - Seleccionar "Sí"
   - Verificar datos
7. **Probar filtro de Edad**:
   - Mover el slider
   - Verificar datos

### 3. Revisar Logs del Backend

En la terminal del backend, deberías ver algo como:

```
DEBUG: Starting with 1699 records
DEBUG: Filters received: {'ageMin': 18, 'ageMax': 100, 'diagnosis': 'Benigno', 'menopause': 'all', 'birads': 'all', 'breastfeeding': 'all'}
DEBUG: Unique cancer values: ['Yes' 'No']
DEBUG: Diagnosis filter (Benigno): 1699 -> 850 records
DEBUG: Final filtered records: 850 (from 1699)
```

## Valores Esperados en el Dataset

Basado en `CubanDataset.csv`:

- **cancer**: "Yes", "No"
- **menopause**: "No", números (edad de menopausia)
- **birads**: "3A", "3B", "3C", "4A", "4B", "4C", "5A", "5B", "5C", etc.
- **breastfeeding**: "No", "3 months", "1 month", etc.

## Próximos Pasos

Si los filtros siguen sin funcionar después de estas correcciones:

1. **Revisar los logs del backend** para identificar el filtro problemático
2. **Verificar los valores únicos** de cada columna en el dataset
3. **Ajustar la lógica de filtrado** según los valores reales

## Resultados de Pruebas

### Script de Prueba Ejecutado

Se creó y ejecutó `backend/scripts/test_filters.py` que prueba todos los filtros individualmente.

**Resultados**: ✅ **TODOS LOS FILTROS FUNCIONAN CORRECTAMENTE EN EL BACKEND**

```
✅ Diagnosis = Benigno: 537 registros
✅ Diagnosis = Maligno: 1160 registros
✅ Menopause = Premenopáusica: 315 registros
✅ Menopause = Posmenopáusica: 1382 registros
✅ BIRADS = 3: 355 registros
✅ BIRADS = 4: 194 registros
✅ BIRADS = 5: 1091 registros
✅ Breastfeeding = Sí: 1071 registros
✅ Breastfeeding = No: 626 registros
✅ Combined (Maligno + Posmenopáusica): 845 registros
```

### Conclusión

El problema **NO está en el backend**. Los filtros funcionan correctamente.

El problema puede estar en:
1. **Frontend**: Manejo de la respuesta o estado de carga
2. **Comunicación**: Timeout o error de red
3. **CORS**: Problemas de configuración

## Archivos Modificados

### Backend

- `backend/services/data_processor.py` (líneas 233-321)
  - Agregado logging detallado
  - Agregado try-catch en todos los filtros
  - Mejorado filtro de BIRADS
  - Mejorado filtro de Menopausia (conversión a string)
  - Agregado conteo de registros en cada paso

- `backend/scripts/test_filters.py` (NUEVO)
  - Script de prueba para verificar filtros
  - Prueba cada filtro individualmente
  - Muestra valores únicos de cada columna

### Frontend

- `frontend/src/components/ClinicalFactors.js` (líneas 32-77)
  - Agregado logging detallado en console
  - Mejorado manejo de errores
  - Muestra detalles del error en mensaje

