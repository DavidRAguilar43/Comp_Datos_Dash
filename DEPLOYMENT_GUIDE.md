# 🚀 Guía de Despliegue - Dashboard Clínico

Esta guía te ayudará a desplegar tu aplicación de forma **GRATUITA** usando:
- **Vercel** para el Frontend (React)
- **Railway** para el Backend (FastAPI)
- **MongoDB Atlas** para la base de datos (opcional, gratis hasta 512MB)

---

## 📋 Pre-requisitos

1. Cuenta en [GitHub](https://github.com) (gratis)
2. Cuenta en [Vercel](https://vercel.com) (gratis)
3. Cuenta en [Railway](https://railway.app) (gratis - $5 de crédito inicial)
4. Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (opcional, gratis)
5. API Key de [OpenAI](https://platform.openai.com/api-keys)

---

## 🗄️ PASO 1: Configurar MongoDB Atlas (Base de Datos)

### 1.1 Crear Cluster Gratuito

1. Ve a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto: "Dashboard-Clinico"
4. Crea un cluster gratuito (M0 Sandbox - FREE)
   - Provider: AWS, Google Cloud o Azure
   - Region: Elige la más cercana a ti
   - Cluster Name: `dashboard-cluster`

### 1.2 Configurar Acceso

1. **Database Access** (Usuarios):
   - Click en "Database Access" en el menú lateral
   - Add New Database User
   - Username: `dashboard_user`
   - Password: Genera una contraseña segura (guárdala)
   - Database User Privileges: "Read and write to any database"
   - Add User

2. **Network Access** (IP Whitelist):
   - Click en "Network Access"
   - Add IP Address
   - **IMPORTANTE**: Click en "Allow Access from Anywhere" (0.0.0.0/0)
   - Confirm

### 1.3 Obtener Connection String

1. Ve a "Database" → "Connect"
2. Selecciona "Connect your application"
3. Driver: Python, Version: 3.11 or later
4. Copia la connection string:
   ```
   mongodb+srv://dashboard_user:<password>@dashboard-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. **Reemplaza** `<password>` con la contraseña que creaste
6. Guarda esta URL, la necesitarás para Railway

---

## 🚂 PASO 2: Desplegar Backend en Railway

### 2.1 Preparar Repositorio

1. **Inicializar Git** (si no lo has hecho):
   ```bash
   cd Comp_Datos_Dash
   git init
   git add .
   git commit -m "Initial commit - Dashboard Clínico"
   ```

2. **Crear repositorio en GitHub**:
   - Ve a [GitHub](https://github.com/new)
   - Nombre: `dashboard-clinico`
   - Visibilidad: Private (recomendado por seguridad)
   - NO inicialices con README
   - Create repository

3. **Subir código a GitHub**:
   ```bash
   git remote add origin https://github.com/TU-USUARIO/dashboard-clinico.git
   git branch -M main
   git push -u origin main
   ```

### 2.2 Desplegar en Railway

1. Ve a [Railway](https://railway.app)
2. Click en "Start a New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway a acceder a tu GitHub
5. Selecciona el repositorio `dashboard-clinico`
6. Railway detectará automáticamente el proyecto Python

### 2.3 Configurar Variables de Entorno en Railway

1. En tu proyecto de Railway, click en el servicio desplegado
2. Ve a la pestaña "Variables"
3. Agrega las siguientes variables:

   ```
   MONGO_URL=mongodb+srv://dashboard_user:TU_PASSWORD@dashboard-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   DB_NAME=breast_cancer_dashboard
   CORS_ORIGINS=https://tu-dominio-frontend.vercel.app
   OPENAI_API_KEY=sk-tu-clave-de-openai
   PORT=8000
   ENVIRONMENT=production
   ```

   **IMPORTANTE**: 
   - Reemplaza `MONGO_URL` con tu connection string de MongoDB Atlas
   - Reemplaza `OPENAI_API_KEY` con tu clave de OpenAI
   - `CORS_ORIGINS` lo actualizaremos después de desplegar el frontend

4. Click en "Deploy" o espera a que se redespliegue automáticamente

### 2.4 Obtener URL del Backend

1. En Railway, ve a "Settings" → "Domains"
2. Click en "Generate Domain"
3. Railway generará una URL como: `https://tu-proyecto.up.railway.app`
4. **Guarda esta URL**, la necesitarás para el frontend

---

## ▲ PASO 3: Desplegar Frontend en Vercel

### 3.1 Desplegar desde GitHub

1. Ve a [Vercel](https://vercel.com)
2. Click en "Add New..." → "Project"
3. Import Git Repository
4. Selecciona tu repositorio `dashboard-clinico`
5. Configure Project:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 3.2 Configurar Variables de Entorno

1. En "Environment Variables", agrega:
   ```
   REACT_APP_BACKEND_URL=https://tu-proyecto.up.railway.app
   ```
   (Usa la URL que obtuviste de Railway)

2. Click en "Deploy"

### 3.3 Obtener URL del Frontend

1. Vercel desplegará tu aplicación
2. Te dará una URL como: `https://dashboard-clinico.vercel.app`
3. **Guarda esta URL**

---

## 🔄 PASO 4: Actualizar CORS en Railway

1. Vuelve a Railway
2. Ve a "Variables"
3. Actualiza `CORS_ORIGINS` con la URL de Vercel:
   ```
   CORS_ORIGINS=https://dashboard-clinico.vercel.app
   ```
4. Guarda y espera a que se redespliegue

---

## ✅ PASO 5: Verificar Despliegue

1. Abre tu aplicación en Vercel: `https://dashboard-clinico.vercel.app`
2. Deberías ver el dashboard
3. Prueba subir un archivo CSV
4. Verifica que las visualizaciones funcionen
5. Prueba el análisis con IA

---

## 🔧 Solución de Problemas

### Error de CORS
- Verifica que `CORS_ORIGINS` en Railway tenga la URL correcta de Vercel
- Asegúrate de que NO haya espacios ni comas extras

### Error de Conexión a MongoDB
- Verifica que la IP 0.0.0.0/0 esté en la whitelist de MongoDB Atlas
- Verifica que el usuario y contraseña sean correctos
- Verifica que hayas reemplazado `<password>` en la connection string

### Error 500 en el Backend
- Ve a Railway → Logs para ver los errores
- Verifica que todas las variables de entorno estén configuradas
- Verifica que `OPENAI_API_KEY` sea válida

### Frontend no se conecta al Backend
- Verifica que `REACT_APP_BACKEND_URL` en Vercel apunte a Railway
- Verifica que la URL de Railway esté activa
- Abre las DevTools del navegador (F12) y revisa la consola

---

## 📊 Límites del Plan Gratuito

### Vercel (Frontend)
- ✅ Despliegues ilimitados
- ✅ 100 GB de ancho de banda/mes
- ✅ Dominio personalizado gratis
- ✅ SSL automático

### Railway (Backend)
- ✅ $5 de crédito inicial
- ✅ ~500 horas de ejecución/mes
- ⚠️ Después del crédito inicial, necesitarás agregar una tarjeta (pero sigue siendo gratis si no excedes el uso)

### MongoDB Atlas
- ✅ 512 MB de almacenamiento
- ✅ Conexiones compartidas
- ✅ Suficiente para desarrollo y proyectos pequeños

---

## 🔄 Actualizaciones Futuras

Cada vez que hagas cambios en tu código:

1. **Commit y push a GitHub**:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push
   ```

2. **Vercel y Railway se redesplegarán automáticamente** 🎉

---

## 🎉 ¡Listo!

Tu aplicación ahora está en producción y accesible desde cualquier lugar del mundo.

**URLs importantes**:
- Frontend: `https://tu-proyecto.vercel.app`
- Backend: `https://tu-proyecto.up.railway.app`
- API Docs: `https://tu-proyecto.up.railway.app/docs`

