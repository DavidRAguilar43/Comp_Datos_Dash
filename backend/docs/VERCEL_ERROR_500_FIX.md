# 🔧 Fix: Error 500 en AI Insights (Vercel/Railway)

## 🐛 Problema

Al hacer clic en "Generar Insights" en la aplicación desplegada en Vercel, aparecen estos errores:

```
us-assets.i.posthog.com/static/array.js:1  Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
compdatosdash-production-01c5.up.railway.app/api/ai/analyze-summary:1  Failed to load resource: the server responded with a status of 500 ()
emergent-main.js:39 Error fetching AI insights: fi
```

## 🔍 Diagnóstico

### Error 1: PostHog bloqueado (ERR_BLOCKED_BY_CLIENT)
- **Causa**: Bloqueador de anuncios o extensión del navegador
- **Impacto**: ⚠️ No crítico - solo afecta analytics
- **Solución**: Opcional - desactivar bloqueador o ignorar

### Error 2: Error 500 en `/api/ai/analyze-summary` ⚠️ CRÍTICO
- **Causa**: Variable de entorno `OPENAI_API_KEY` no configurada en Railway
- **Impacto**: 🚨 Los insights de IA no funcionan
- **Solución**: Configurar API key en Railway

## ✅ Solución: Configurar OPENAI_API_KEY en Railway

### Paso 1: Obtener una API Key

Tienes dos opciones:

#### Opción A: OpenRouter (Recomendado - más económico)

1. Ve a: https://openrouter.ai/keys
2. Crea una cuenta (puedes usar GitHub)
3. Click en **"Create Key"**
4. Dale un nombre (ej: "Breast Cancer Dashboard")
5. Copia la key (empieza con `sk-or-v1-...`)

**Ventajas de OpenRouter:**
- ✅ Más barato que OpenAI directo
- ✅ Acceso a múltiples modelos (GPT-4, Claude, etc.)
- ✅ Créditos gratis para empezar
- ✅ Compatible con la API de OpenAI

#### Opción B: OpenAI Directo

1. Ve a: https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Click en **"Create new secret key"**
4. Dale un nombre (ej: "Breast Cancer Dashboard")
5. Copia la key (empieza con `sk-...`)

**Nota:** OpenAI requiere agregar créditos a tu cuenta.

### Paso 2: Configurar en Railway

1. Ve a https://railway.app
2. Inicia sesión
3. Selecciona tu proyecto **compdatosdash-production**
4. Click en el servicio **backend** (el que tiene el código Python)
5. Ve a la pestaña **"Variables"**
6. Busca la variable `OPENAI_API_KEY`:
   - **Si existe**: Click en el valor y pégalo nuevo
   - **Si NO existe**: Click en **"+ New Variable"**
     - Name: `OPENAI_API_KEY`
     - Value: Pega tu API key
7. Click en **"Add"** o **"Save"**

### Paso 3: Verificar el Redespliegue

1. Railway redesplegará automáticamente (verás un nuevo deployment en la pestaña "Deployments")
2. Espera 1-2 minutos hasta que el deployment esté en estado **"Success"**
3. Ve a la pestaña **"Logs"** y verifica que no haya errores

### Paso 4: Probar en Vercel

1. Ve a tu aplicación en Vercel: https://comp-datos-dash.vercel.app
2. Navega a la sección **"Resumen General"**
3. Click en **"Generar Insights"**
4. Deberías ver el análisis de IA generado correctamente

## 🧪 Verificación Adicional

### Probar el endpoint directamente

Puedes probar el endpoint de AI directamente:

```bash
curl -X POST https://compdatosdash-production.up.railway.app/api/ai/analyze-summary
```

**Respuesta esperada (si funciona):**
```json
{
  "success": true,
  "insights": "...",
  "model_used": "openai/gpt-4o-mini",
  "tokens_used": 450
}
```

**Respuesta de error (si falta la key):**
```json
{
  "detail": "OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file."
}
```

## 🔐 Seguridad

**⚠️ IMPORTANTE:**
- ✅ **NUNCA** incluyas la API key en el código
- ✅ **NUNCA** hagas commit de archivos `.env` con keys reales
- ✅ Configura las keys **SOLO** en Railway Dashboard (Variables tab)
- ✅ Las variables de entorno en Railway NO se sincronizan con Git
- ✅ Revoca keys antiguas si las expusiste accidentalmente

## 📊 Costos Estimados

### OpenRouter (Recomendado)
- GPT-4o-mini: ~$0.15 por 1M tokens de entrada
- Estimado: ~$0.001 por insight generado
- Créditos gratis: $5 para empezar

### OpenAI Directo
- GPT-4o-mini: ~$0.15 por 1M tokens de entrada
- Estimado: ~$0.001 por insight generado
- Requiere agregar créditos (mínimo $5)

## 🆘 Troubleshooting

### Error persiste después de configurar la key

1. **Verifica que la key sea válida:**
   ```bash
   # Para OpenRouter
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer sk-or-v1-YOUR_KEY_HERE"
   
   # Para OpenAI
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer sk-YOUR_KEY_HERE"
   ```

2. **Revisa los logs de Railway:**
   - Ve a la pestaña "Logs"
   - Busca errores relacionados con OpenAI
   - Verifica que la variable esté cargada

3. **Fuerza un redespliegue:**
   - Ve a "Deployments"
   - Click en el último deployment
   - Click en "Redeploy"

### Error: "Insufficient credits"

- Agrega créditos a tu cuenta de OpenRouter u OpenAI
- OpenRouter: https://openrouter.ai/credits
- OpenAI: https://platform.openai.com/account/billing

## 📚 Referencias

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Railway Environment Variables](https://docs.railway.app/develop/variables)

