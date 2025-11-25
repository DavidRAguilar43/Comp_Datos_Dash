# 🚂 Solución Error 500 en Railway - AI Insights

## 📋 Problema Identificado

**Error en logs de Railway:**
```
ERROR - Error initializing AI analyzer: Client.__init__() got an unexpected keyword argument 'proxies'
```

**Causa raíz:**
- Conflicto de versiones entre `openai==1.12.0` (antigua) y `httpx>=0.28.0` (reciente)
- La versión antigua de OpenAI usa el parámetro `proxies` que fue eliminado en httpx 0.28.0

---

## ✅ Solución Implementada

### 1. Actualización de Dependencias

**Archivo modificado:** `backend/requirements.txt`

**Cambio realizado:**
```diff
# AI/ML
- openai==1.12.0
+ openai>=1.50.0,<1.56.0
scikit-learn>=1.5.0
```

**Razón:** 
- Versiones 1.50.x - 1.55.x son compatibles con httpx moderno
- Evitamos 1.56.0+ que tiene otros problemas conocidos

---

## 🚀 Pasos para Desplegar en Railway

### Opción A: Redespliegue Automático (Recomendado)

1. **Commit y push de los cambios:**
   ```bash
   cd "C:\Users\David\Downloads\Patrones de Comportamiento de Datos\ProyectoFinal"
   git add Comp_Datos_Dash/backend/requirements.txt
   git commit -m "fix: actualizar openai a versión compatible con httpx"
   git push origin main
   ```

2. **Railway detectará el cambio automáticamente** y redesplegará

3. **Verificar en Railway Dashboard:**
   - Ve a [railway.app](https://railway.app)
   - Selecciona tu proyecto
   - Ve a "Deployments" → espera que termine el build
   - Revisa los logs para confirmar que no hay errores

### Opción B: Redespliegue Manual

Si Railway no detecta el cambio automáticamente:

1. Ve a [railway.app](https://railway.app)
2. Selecciona tu proyecto **compdatosdash-production**
3. Haz clic en el servicio del **backend**
4. Ve a la pestaña **"Deployments"**
5. Haz clic en **"Redeploy"** en el último deployment

---

## 🔐 Configurar Variables de Entorno (IMPORTANTE)

Asegúrate de que Railway tenga configuradas estas variables:

1. Ve a tu proyecto en Railway
2. Selecciona el servicio backend
3. Ve a la pestaña **"Variables"**
4. Agrega/verifica estas variables:

```env
OPENAI_API_KEY=tu_openrouter_api_key_aqui
CORS_ORIGINS=https://comp-datos-dash.vercel.app,http://localhost:3000
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard
JWT_SECRET=genera_un_secret_seguro_con_openssl_rand_hex_32
```

**⚠️ IMPORTANTE - SEGURIDAD:**
- **NUNCA** incluyas API keys reales en archivos que se suban a Git
- Obtén tu API key de OpenRouter desde: https://openrouter.ai/keys
- Configura las variables SOLO en Railway Dashboard (Variables tab)
- Las variables de entorno en Railway NO se sincronizan con Git

**⚠️ Nota:** Si falta `OPENAI_API_KEY`, el endpoint de AI fallará con error 500.

---

## 🧪 Verificación Post-Despliegue

### 1. Revisar Logs en Railway

```
✅ Buscar: "Generating AI insights for summary statistics"
❌ NO debe aparecer: "Error initializing AI analyzer"
```

### 2. Probar desde el Frontend

1. Abre tu app en Vercel: https://comp-datos-dash.vercel.app
2. Carga un archivo CSV
3. Ve a la sección de **Resumen de Datos**
4. Haz clic en **"Generar Insights con IA"**
5. Deberías ver insights generados sin errores

### 3. Verificar con cURL (Opcional)

```bash
curl -X POST https://compdatosdash-production-01c5.up.railway.app/api/ai/analyze-summary \
  -H "Content-Type: application/json"
```

**Respuesta esperada:**
- Status: 200 OK (si hay datos cargados)
- Status: 400 (si no hay datos - esto es normal)
- ❌ NO debe ser 500

---

## 📊 Resumen de Cambios

| Componente | Antes | Después |
|------------|-------|---------|
| openai | 1.12.0 (fija) | >=1.50.0,<1.56.0 (rango compatible) |
| Compatibilidad httpx | ❌ Rota | ✅ Funcional |
| Error 500 | ✅ Presente | ❌ Resuelto |

---

## 🔍 Troubleshooting

### Si sigue fallando después del redespliegue:

1. **Verificar que se instaló la nueva versión:**
   - Revisa los logs de build en Railway
   - Busca: `Installing openai-1.5x.x`

2. **Limpiar caché de Railway:**
   - En Railway Dashboard → Settings → "Clear Build Cache"
   - Redeploy nuevamente

3. **Verificar variables de entorno:**
   - Asegúrate que `OPENAI_API_KEY` esté configurada
   - Verifica que no tenga espacios extra

4. **Revisar logs completos:**
   - Railway Dashboard → Logs
   - Busca cualquier otro error relacionado

---

## 📝 Notas Adicionales

- **Versión local vs Railway:** El archivo `.env` es local y NO se sube a Railway
- **OpenRouter:** La API key `sk-or-v1-*` indica que usas OpenRouter, no OpenAI directo
- **Modelo:** El código usa `gpt-4o` - asegúrate que tu cuenta de OpenRouter lo soporte

---

**Fecha de creación:** 2025-11-25  
**Última actualización:** 2025-11-25

