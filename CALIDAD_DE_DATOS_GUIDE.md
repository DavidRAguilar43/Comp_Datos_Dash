# Guía de Usuario - Sección "Calidad de Datos"

## Descripción General

La nueva sección **"Calidad de Datos"** proporciona un informe completo y automático de todas las operaciones de preparación de datos realizadas en su conjunto de datos.

---

## Cómo Acceder

1. **Inicie la aplicación**:
   - Backend: `cd backend && ./venv/Scripts/activate && python -m uvicorn server:app --reload`
   - Frontend: `cd frontend && npm start`

2. **Abra el navegador**: http://localhost:3000

3. **Cargue un archivo CSV** con datos de pacientes

4. **Haga clic en la pestaña "Calidad de Datos"** (segunda pestaña, icono de escudo)

---

## Secciones del Informe

### 1. Tarjetas de Resumen (Superior)

Cuatro tarjetas con métricas clave:

- **🟢 Transformaciones**: Total de operaciones aplicadas
- **🔵 Imputación**: Número de columnas con valores imputados
- **🟠 Valores Atípicos**: Columnas con outliers detectados
- **🟣 Duplicados**: Registros duplicados eliminados

### 2. Resumen de Datos Faltantes

**Comparación Antes/Después del Procesamiento**

- **Antes**: Muestra todas las columnas con valores nulos
  - Cantidad de valores faltantes
  - Porcentaje del total
  - Indicador visual rojo

- **Después**: Estado post-procesamiento
  - Valores faltantes restantes (si los hay)
  - Indicador verde si todos fueron imputados

### 3. Reporte de Imputación

**Tabla detallada** que muestra:

| Columna | Valores Imputados | Método | Valor de Relleno |
|---------|-------------------|--------|------------------|
| age     | 15                | Media  | 52.34            |
| cancer  | 8                 | Moda   | No               |

**Métodos de Imputación**:
- **Media**: Para columnas numéricas (edad, mediciones, etc.)
- **Moda**: Para columnas categóricas (diagnóstico, estado, etc.)

### 4. Eliminación de Duplicados

**Tres métricas principales**:
- Total de duplicados detectados
- Número de duplicados eliminados
- Método utilizado (drop_duplicates)

### 5. Detección de Valores Atípicos

**Tabla con análisis IQR** (Rango Intercuartílico):

| Columna | Cantidad | % | Límite Inferior | Límite Superior | Tratamiento |
|---------|----------|---|-----------------|-----------------|-------------|
| age     | 12       | 2.5% | 18.5         | 85.5            | flagged     |

**Interpretación**:
- **Límite Inferior/Superior**: Valores fuera de estos rangos son considerados atípicos
- **Tratamiento**: Actualmente solo se marcan (flagged), no se eliminan

### 6. Correcciones de Tipo de Datos

**Tarjetas individuales** para cada columna corregida:

```
📊 income
Tipo Original: object (texto)
Nuevo Tipo: float64 (número)
Razón: Valores numéricos almacenados como texto con símbolos
```

**Correcciones Automáticas**:
- Números con símbolos ($1,234 → 1234)
- Fechas en formato texto → datetime
- Conversiones de tipo apropiadas

### 7. Registro de Transformaciones

**Lista cronológica** de todas las operaciones:

1. **Text Standardization**
   - Descripción: Espacios eliminados y valores Yes/No normalizados
   - Columnas afectadas: cancer, menopause, breastfeeding

2. **Type Correction**
   - Descripción: Tipos de datos corregidos para mejor análisis
   - Columnas afectadas: income, date_of_birth

### 8. Renombrado de Columnas

**Comparación lado a lado**:

```
Anterior: Patient ID        →  Nuevo: patient_id
Anterior: Date of Birth     →  Nuevo: date_of_birth
Anterior: Cancer Diagnosis  →  Nuevo: cancer_diagnosis
```

**Mejoras**:
- Minúsculas consistentes
- Espacios reemplazados por guiones bajos
- Mayor claridad y consistencia

### 9. Formato de Fechas

**Estandarización de fechas**:

```
📅 date_of_birth
Formato Aplicado: %Y-%m-%d (YYYY-MM-DD)
Ejemplo Antes: 15/03/1975
Ejemplo Después: 1975-03-15
```

---

## Interpretación de Resultados

### ✅ Indicadores Positivos

- **Valores faltantes = 0 después**: Todos los datos fueron imputados correctamente
- **Duplicados eliminados > 0**: Se mejoró la calidad eliminando redundancias
- **Transformaciones aplicadas**: El dataset está estandarizado

### ⚠️ Puntos de Atención

- **Muchos valores atípicos**: Puede indicar problemas de calidad o casos especiales
- **Muchas imputaciones**: Revisar si los valores imputados son razonables
- **Correcciones de tipo**: Verificar que las conversiones sean correctas

---

## Beneficios

### 1. **Transparencia Total**
- Visibilidad completa de todas las operaciones realizadas
- Trazabilidad de cambios en los datos

### 2. **Calidad Asegurada**
- Detección automática de problemas
- Corrección sistemática de inconsistencias

### 3. **Documentación Automática**
- Registro completo para auditorías
- Reproducibilidad de resultados

### 4. **Toma de Decisiones Informada**
- Conocimiento del estado de los datos
- Confianza en los análisis posteriores

---

## Preguntas Frecuentes

**P: ¿Los datos originales se modifican?**
R: No, se mantiene una copia del dataset original. Las transformaciones se aplican a una copia de trabajo.

**P: ¿Puedo deshacer las transformaciones?**
R: Actualmente no, pero el dataset original se conserva en memoria durante la sesión.

**P: ¿Qué pasa si no quiero que se imputen ciertos valores?**
R: La imputación es automática. Para control manual, deberá modificar el código del backend.

**P: ¿Los outliers se eliminan?**
R: No, solo se detectan y marcan. No se eliminan automáticamente para preservar datos potencialmente importantes.

**P: ¿Puedo exportar este informe?**
R: Actualmente el informe solo está disponible en la interfaz web. Puede tomar capturas de pantalla o implementar una función de exportación.

---

## Soporte Técnico

Para problemas o preguntas:
1. Revise la consola del navegador (F12) para errores
2. Verifique que ambos servidores estén corriendo
3. Consulte `DATA_PREPARATION_IMPLEMENTATION.md` para detalles técnicos

---

**¡Disfrute de su análisis de datos con mayor confianza y transparencia!**

