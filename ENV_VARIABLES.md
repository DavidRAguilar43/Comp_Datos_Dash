# 🔐 Variables de Entorno - Referencia Completa

Este documento lista todas las variables de entorno necesarias para cada plataforma.

---

## 🗄️ MongoDB Atlas

### Crear Connection String

1. Ve a MongoDB Atlas → Database → Connect
2. Selecciona "Connect your application"
3. Copia la connection string:
   ```
   mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   ```
4. Reemplaza `<username>` y `<password>` con tus credenciales

**Ejemplo**:
```
mongodb+srv://dashboard_user:MiPassword123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

---

## 🚂 Railway (Backend)

### Variables Requeridas

Copia y pega estas variables en Railway → Variables:

```env
# MongoDB Connection
MONGO_URL=mongodb+srv://dashboard_user:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority

# Database Name
DB_NAME=breast_cancer_dashboard

# CORS Origins (actualizar después de desplegar en Vercel)
CORS_ORIGINS=https://tu-proyecto.vercel.app

# OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Port (Railway lo asigna automáticamente)
PORT=8000

# Environment
ENVIRONMENT=production
```

### Cómo Obtener Cada Variable

| Variable | Dónde Obtenerla |
|----------|-----------------|
| `MONGO_URL` | MongoDB Atlas → Database → Connect |
| `DB_NAME` | Nombre que elijas (ej: `breast_cancer_dashboard`) |
| `CORS_ORIGINS` | URL de Vercel (actualizar después del despliegue) |
| `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) |
| `PORT` | Railway lo asigna automáticamente (dejar en 8000) |
| `ENVIRONMENT` | `production` |

### Notas Importantes

- ⚠️ **CORS_ORIGINS**: Primero puedes usar `*` para probar, luego actualiza con la URL exacta de Vercel
- ⚠️ **OPENAI_API_KEY**: Asegúrate de tener créditos en tu cuenta de OpenAI
- ⚠️ **MONGO_URL**: Verifica que la IP 0.0.0.0/0 esté en la whitelist de MongoDB Atlas

---

## ▲ Vercel (Frontend)

### Variables Requeridas

Copia y pega estas variables en Vercel → Settings → Environment Variables:

```env
# Backend API URL (actualizar con la URL de Railway)
REACT_APP_BACKEND_URL=https://tu-proyecto.up.railway.app
```

### Cómo Obtener la URL de Railway

1. Ve a tu proyecto en Railway
2. Click en el servicio desplegado
3. Ve a "Settings" → "Domains"
4. Click en "Generate Domain"
5. Copia la URL generada (ej: `https://dashboard-backend-production.up.railway.app`)
6. Pégala en Vercel como `REACT_APP_BACKEND_URL`

### Variables Opcionales

```env
# Habilitar ediciones visuales (solo para desarrollo)
REACT_APP_ENABLE_VISUAL_EDITS=false

# Deshabilitar hot reload (solo si tienes problemas)
DISABLE_HOT_RELOAD=false

# Health check (opcional)
ENABLE_HEALTH_CHECK=false
```

---

## 🔄 Flujo de Configuración Recomendado

### Paso 1: MongoDB Atlas
1. Crear cluster
2. Crear usuario de base de datos
3. Configurar Network Access (0.0.0.0/0)
4. Copiar connection string
5. ✅ Guardar `MONGO_URL`

### Paso 2: OpenAI
1. Ir a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crear nueva API key
3. ✅ Guardar `OPENAI_API_KEY`

### Paso 3: Railway (Backend)
1. Conectar repositorio de GitHub
2. Agregar variables de entorno:
   - `MONGO_URL` (de MongoDB Atlas)
   - `DB_NAME=breast_cancer_dashboard`
   - `CORS_ORIGINS=*` (temporal)
   - `OPENAI_API_KEY` (de OpenAI)
   - `PORT=8000`
   - `ENVIRONMENT=production`
3. Generar dominio
4. ✅ Guardar URL de Railway

### Paso 4: Vercel (Frontend)
1. Conectar repositorio de GitHub
2. Root Directory: `frontend`
3. Agregar variable de entorno:
   - `REACT_APP_BACKEND_URL` (URL de Railway)
4. Deploy
5. ✅ Guardar URL de Vercel

### Paso 5: Actualizar CORS
1. Volver a Railway
2. Actualizar `CORS_ORIGINS` con URL de Vercel
3. Guardar (se redespliegará automáticamente)

---

## ✅ Checklist de Verificación

Antes de desplegar, verifica que tengas:

- [ ] Connection string de MongoDB Atlas
- [ ] Usuario y contraseña de MongoDB
- [ ] IP 0.0.0.0/0 en whitelist de MongoDB
- [ ] API Key de OpenAI con créditos disponibles
- [ ] Repositorio en GitHub (privado recomendado)
- [ ] Cuenta en Railway
- [ ] Cuenta en Vercel

---

## 🆘 Solución de Problemas

### Error: "MongoServerError: bad auth"
- ✅ Verifica usuario y contraseña en `MONGO_URL`
- ✅ Asegúrate de haber reemplazado `<password>` en la connection string

### Error: "MongoNetworkError: connection timeout"
- ✅ Verifica que 0.0.0.0/0 esté en Network Access de MongoDB Atlas
- ✅ Espera 1-2 minutos después de agregar la IP

### Error: "OpenAI API key invalid"
- ✅ Verifica que la API key sea correcta
- ✅ Verifica que tengas créditos en tu cuenta de OpenAI
- ✅ Asegúrate de que la key empiece con `sk-`

### Error de CORS en el navegador
- ✅ Verifica que `CORS_ORIGINS` en Railway tenga la URL exacta de Vercel
- ✅ No incluyas `/` al final de la URL
- ✅ Usa `https://` (no `http://`)

### Frontend no se conecta al backend
- ✅ Verifica que `REACT_APP_BACKEND_URL` en Vercel sea correcta
- ✅ Verifica que la URL de Railway esté activa
- ✅ Abre DevTools (F12) y revisa la consola para errores

---

## 📝 Plantilla de Variables

### Para Railway
```
MONGO_URL=
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=
OPENAI_API_KEY=
PORT=8000
ENVIRONMENT=production
```

### Para Vercel
```
REACT_APP_BACKEND_URL=
```

---

## 🔗 Enlaces Útiles

- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Railway](https://railway.app)
- [Vercel](https://vercel.com)
- [Guía de Despliegue Completa](./DEPLOYMENT_GUIDE.md)
- [Guía Rápida](./QUICK_DEPLOY.md)

