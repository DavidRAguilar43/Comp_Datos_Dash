# 💳 Fix: OpenRouter Credits Exhausted

## 🐛 Problema Real

El error 500 **NO es por falta de configuración**, sino por **créditos insuficientes en OpenRouter**:

```
Error code: 402 - This request requires more credits, or fewer max_tokens. 
You requested up to 600 tokens, but can only afford 469.
```

## ✅ Soluciones

### Opción 1: Agregar Créditos (Recomendado para producción)

1. Ve a: https://openrouter.ai/settings/credits
2. Agrega créditos (mínimo $5)
3. Los insights funcionarán inmediatamente

**Costos estimados:**
- ~$0.001 por insight generado
- $5 = ~5,000 insights
- Suficiente para uso normal del dashboard

### Opción 2: Reducir Uso de Tokens (Temporal - YA APLICADO)

He reducido el `max_tokens` en todos los endpoints de IA:

| Endpoint | Antes | Ahora | Ahorro |
|----------|-------|-------|--------|
| `analyze_ml_model` | 500 | 350 | 30% |
| `analyze_summary_statistics` | 600 | 400 | 33% |
| `analyze_correlations` | 500 | 350 | 30% |
| `generate_clinical_report` | 800 | 400 | 50% |

**Esto te permitirá:**
- ✅ Usar los créditos gratis restantes (469 tokens)
- ✅ Generar al menos 1-2 insights más
- ⚠️ Respuestas más cortas pero funcionales

### Opción 3: Cambiar a OpenAI (Alternativa)

Si prefieres usar OpenAI en lugar de OpenRouter:

1. Obtén una API key de OpenAI: https://platform.openai.com/api-keys
2. Agrega créditos a tu cuenta de OpenAI (mínimo $5)
3. Actualiza la variable en Railway:
   - Railway → Variables → `OPENAI_API_KEY`
   - Reemplaza con tu nueva key de OpenAI (empieza con `sk-...`)

**Nota:** OpenAI tiene precios similares a OpenRouter.

## 🚀 Desplegar los Cambios (Opción 2)

Si elegiste la Opción 2 (reducir tokens), despliega los cambios:

```bash
cd Comp_Datos_Dash

# Commit los cambios
git add backend/services/ai_analyzer.py
git commit -m "Reduce max_tokens to fit within free OpenRouter credits"
git push

# Railway redesplegará automáticamente
```

## 🧪 Verificar

1. Espera 1-2 minutos después del push
2. Ve a Railway → Deployments → Verifica que esté "Success"
3. Prueba en tu app: https://comp-datos-dash.vercel.app
4. Click en "Generar Insights"

## 📊 Monitorear Uso de Créditos

Para ver cuántos créditos te quedan:

1. Ve a: https://openrouter.ai/settings/credits
2. Verás:
   - Créditos disponibles
   - Historial de uso
   - Costo por request

## 💡 Recomendaciones

### Para Desarrollo/Testing:
- ✅ Usa los créditos gratis con tokens reducidos
- ✅ Limita las pruebas de IA a lo necesario
- ✅ Considera agregar $5 para desarrollo continuo

### Para Producción:
- ✅ Agrega créditos suficientes ($10-20)
- ✅ Configura alertas de créditos bajos
- ✅ Monitorea el uso regularmente

### Para Ahorrar Créditos:
- ✅ Cachea los insights generados (implementación futura)
- ✅ Limita la frecuencia de generación
- ✅ Usa modelos más baratos para testing

## 🔍 Logs de Referencia

**Error original:**
```
2025-11-27 17:27:56,378 - httpx - INFO - HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 402 Payment Required"
2025-11-27 17:27:56,379 - server - ERROR - Error generating AI insights: Error code: 402 - {'error': {'message': 'This request requires more credits, or fewer max_tokens. You requested up to 600 tokens, but can only afford 469.'}}
```

**Después del fix (esperado):**
```
2025-11-27 XX:XX:XX,XXX - server - INFO - Generating AI insights for summary statistics
2025-11-27 XX:XX:XX,XXX - httpx - INFO - HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-27 XX:XX:XX,XXX - server - INFO - AI insights generated successfully
```

## 🆘 Troubleshooting

### Sigo viendo error 402 después de reducir tokens

- Verifica que Railway haya redesplegado con los cambios
- Revisa que el nuevo código esté en producción
- Puede que necesites agregar créditos de todas formas

### ¿Cuántos créditos necesito?

Para uso normal del dashboard:
- **Desarrollo/Testing**: $5 (suficiente para 1-2 meses)
- **Producción ligera**: $10/mes (100-200 insights)
- **Producción media**: $20/mes (500+ insights)

### ¿Cómo evito quedarme sin créditos?

1. Configura alertas en OpenRouter
2. Monitorea el uso semanalmente
3. Implementa caché de insights (futuro)
4. Limita la generación a usuarios autenticados

---

**Resumen:** El problema es falta de créditos en OpenRouter. Puedes agregar créditos ($5) o usar la versión reducida que acabo de implementar.

