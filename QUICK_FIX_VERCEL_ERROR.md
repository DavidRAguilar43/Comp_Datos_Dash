# ⚡ Quick Fix: Error 500 en Vercel

## 🎯 Problema Actualizado
Al hacer clic en "Generar Insights" aparece error 500.

**Causa real:** Te quedaste sin créditos en OpenRouter (Error 402).

```
Error: You requested up to 600 tokens, but can only afford 469.
```

## 🔧 Soluciones (elige una)

### Opción 1: Agregar Créditos a OpenRouter (Recomendado)

1. Ve a: https://openrouter.ai/settings/credits
2. Agrega créditos (mínimo $5)
3. ✅ Funcionará inmediatamente, sin cambios de código

**Costo:** ~$0.001 por insight = $5 para ~5,000 insights

### Opción 2: Usar Versión Reducida (GRATIS - Ya aplicado)

He reducido el uso de tokens para que funcione con tus créditos gratis:

```bash
cd Comp_Datos_Dash
git pull  # Descarga los cambios
git add backend/services/ai_analyzer.py
git commit -m "Reduce tokens for free credits"
git push  # Railway redesplegará automáticamente
```

**Limitaciones:**
- ✅ Gratis con créditos restantes
- ⚠️ Respuestas más cortas
- ⚠️ Solo 1-2 insights más disponibles

### Opción 3: Cambiar a OpenAI

1. Ve a: https://platform.openai.com/api-keys
2. Crea una API key
3. Agrega créditos ($5 mínimo)
4. Actualiza en Railway:
   - Railway → Variables → `OPENAI_API_KEY`
   - Reemplaza con tu nueva key de OpenAI

## 🧪 Verificar Configuración Local

```bash
# Activa el entorno virtual
cd Comp_Datos_Dash/backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Instala requests si no lo tienes
pip install requests

# Ejecuta el script de verificación
python scripts/verify_railway_config.py
```

## 📚 Documentación Completa

Ver: `backend/docs/VERCEL_ERROR_500_FIX.md`

## 🆘 ¿Sigue sin funcionar?

1. **Revisa logs de Railway:**
   - Railway → Tu proyecto → Backend → Pestaña "Logs"
   - Busca errores relacionados con OpenAI

2. **Verifica la key:**
   ```bash
   # OpenRouter
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer TU_KEY_AQUI"
   
   # OpenAI
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer TU_KEY_AQUI"
   ```

3. **Fuerza redespliegue:**
   - Railway → Deployments → Click último deployment → "Redeploy"

## 💡 Sobre el Error de PostHog

El error `ERR_BLOCKED_BY_CLIENT` es solo analytics bloqueado por tu navegador.
- ⚠️ No es crítico
- ✅ Puedes ignorarlo
- 🔧 O desactiva el bloqueador de anuncios para este sitio

## 📊 Costos

- OpenRouter: ~$0.001 por insight (~$5 créditos gratis)
- OpenAI: ~$0.001 por insight (requiere agregar créditos)

---

**¿Necesitas ayuda?** Revisa `backend/docs/VERCEL_ERROR_500_FIX.md` para más detalles.

