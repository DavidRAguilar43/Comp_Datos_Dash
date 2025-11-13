# 📖 Guía Manual de Despliegue - Paso a Paso

Esta guía te llevará de la mano en cada paso del despliegue.

---

## ✅ CHECKLIST PREVIO

Antes de empezar, asegúrate de tener:

- [ ] Cuenta en [GitHub](https://github.com)
- [ ] Cuenta en [Railway](https://railway.app)
- [ ] Cuenta en [Vercel](https://vercel.com)
- [ ] Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (opcional)
- [ ] API Key de [OpenAI](https://platform.openai.com/api-keys)

---

## 📝 PARTE 1: PREPARAR MONGODB ATLAS (10 minutos)

### 1.1 Crear Cuenta y Cluster

1. Ve a https://www.mongodb.com/cloud/atlas/register
2. Crea una cuenta (puedes usar Google/GitHub)
3. Selecciona "Create a deployment"
4. Elige **M0 FREE** (gratis para siempre)
5. Provider: AWS, Google Cloud o Azure (el que prefieras)
6. Region: Elige la más cercana a ti
7. Cluster Name: `dashboard-cluster`
8. Click en **"Create Deployment"**

### 1.2 Crear Usuario de Base de Datos

1. Te aparecerá un modal "Security Quickstart"
2. En "How would you like to authenticate your connection?":
   - Username: `dashboard_user`
   - Password: Click en "Autogenerate Secure Password" y **COPIA LA CONTRASEÑA**
   - O crea tu propia contraseña (guárdala bien)
3. Click en **"Create Database User"**

### 1.3 Configurar Acceso de Red

1. En "Where would you like to connect from?":
   - Click en **"My Local Environment"**
   - En "IP Access List", click en **"Add My Current IP Address"**
   - Luego click en **"Add Entry"**
2. **IMPORTANTE**: Agrega también acceso desde cualquier IP:
   - IP Address: `0.0.0.0/0`
   - Description: `Allow all`
   - Click en **"Add Entry"**
3. Click en **"Finish and Close"**

### 1.4 Obtener Connection String

1. Click en **"Go to Database"**
2. En tu cluster, click en **"Connect"**
3. Selecciona **"Drivers"**
4. Driver: Python, Version: 3.11 or later
5. Copia la connection string (se ve así):
   ```
   mongodb+srv://dashboard_user:<password>@dashboard-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **REEMPLAZA** `<password>` con la contraseña que copiaste antes
7. **GUARDA** esta URL completa en un lugar seguro (la necesitarás para Railway)

**Ejemplo de URL completa**:
```
mongodb+srv://dashboard_user:MiPassword123@dashboard-cluster.abc123.mongodb.net/?retryWrites=true&w=majority
```

---

## 🐙 PARTE 2: SUBIR A GITHUB (5 minutos)

### 2.1 Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Repository name: `dashboard-clinico`
3. Description: "Dashboard de análisis de cáncer de mama"
4. Visibilidad: **Private** (recomendado por seguridad)
5. **NO** marques "Add a README file"
6. **NO** marques "Add .gitignore"
7. **NO** marques "Choose a license"
8. Click en **"Create repository"**

### 2.2 Subir el Código

Abre una terminal en la carpeta `Comp_Datos_Dash` y ejecuta:

```bash
# Inicializar Git (si no lo has hecho)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit - Dashboard Clinico"

# Conectar con GitHub (reemplaza TU-USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU-USUARIO/dashboard-clinico.git

# Cambiar a rama main
git branch -M main

# Subir el código
git push -u origin main
```

**Si te pide autenticación**:
- Usuario: Tu nombre de usuario de GitHub
- Contraseña: Usa un **Personal Access Token** (no tu contraseña normal)
- Cómo crear token: https://github.com/settings/tokens → "Generate new token (classic)" → Marca "repo" → Generate

---

## 🚂 PARTE 3: DESPLEGAR BACKEND EN RAILWAY (5 minutos)

### 3.1 Crear Proyecto en Railway

1. Ve a https://railway.app
2. Click en **"Login"** y usa tu cuenta de GitHub
3. Click en **"New Project"**
4. Selecciona **"Deploy from GitHub repo"**
5. Si es la primera vez, autoriza Railway a acceder a tu GitHub
6. Busca y selecciona tu repositorio `dashboard-clinico`
7. Railway comenzará a desplegar automáticamente

### 3.2 Configurar Variables de Entorno

1. En tu proyecto de Railway, verás el servicio desplegándose
2. Click en el servicio (aparece como "dashboard-clinico" o similar)
3. Ve a la pestaña **"Variables"**
4. Click en **"New Variable"** y agrega cada una de estas:

```
MONGO_URL=mongodb+srv://dashboard_user:TU_PASSWORD@dashboard-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=*
OPENAI_API_KEY=sk-tu-clave-de-openai-aqui
PORT=8000
ENVIRONMENT=production
```

**IMPORTANTE**:
- Reemplaza `MONGO_URL` con tu connection string completa de MongoDB Atlas
- Reemplaza `OPENAI_API_KEY` con tu clave de OpenAI
- Deja `CORS_ORIGINS=*` por ahora (lo actualizaremos después)

5. Después de agregar todas las variables, Railway se redespliegará automáticamente

### 3.3 Obtener URL del Backend

1. Ve a la pestaña **"Settings"**
2. Scroll down hasta **"Domains"**
3. Click en **"Generate Domain"**
4. Railway generará una URL como: `https://dashboard-clinico-production.up.railway.app`
5. **COPIA Y GUARDA** esta URL (la necesitarás para Vercel)

### 3.4 Verificar que Funciona

1. Abre la URL en tu navegador
2. Agrega `/docs` al final: `https://tu-proyecto.up.railway.app/docs`
3. Deberías ver la documentación de la API (Swagger UI)
4. Si ves la documentación, ¡el backend está funcionando! ✅

---

## ▲ PARTE 4: DESPLEGAR FRONTEND EN VERCEL (5 minutos)

### 4.1 Crear Proyecto en Vercel

1. Ve a https://vercel.com
2. Click en **"Login"** y usa tu cuenta de GitHub
3. Click en **"Add New..."** → **"Project"**
4. Busca y selecciona tu repositorio `dashboard-clinico`
5. Click en **"Import"**

### 4.2 Configurar el Proyecto

En la pantalla de configuración:

1. **Framework Preset**: Selecciona **"Create React App"**
2. **Root Directory**: Click en **"Edit"** y escribe `frontend`
3. **Build Command**: Debería decir `npm run build` (déjalo así)
4. **Output Directory**: Debería decir `build` (déjalo así)

### 4.3 Agregar Variable de Entorno

1. Scroll down hasta **"Environment Variables"**
2. Agrega:
   - **Name**: `REACT_APP_BACKEND_URL`
   - **Value**: La URL de Railway que copiaste (ej: `https://dashboard-clinico-production.up.railway.app`)
3. **NO** agregues `/` al final de la URL
4. Click en **"Add"**

### 4.4 Desplegar

1. Click en **"Deploy"**
2. Vercel comenzará a construir y desplegar tu aplicación
3. Esto tomará 2-3 minutos
4. Cuando termine, verás "Congratulations!" 🎉

### 4.5 Obtener URL del Frontend

1. Vercel te mostrará la URL de tu aplicación
2. Se verá como: `https://dashboard-clinico.vercel.app`
3. **COPIA Y GUARDA** esta URL

---

## 🔄 PARTE 5: ACTUALIZAR CORS (2 minutos)

Ahora que tienes la URL de Vercel, necesitas actualizar el backend:

1. Vuelve a **Railway**
2. Ve a tu proyecto → Servicio → **"Variables"**
3. Busca la variable `CORS_ORIGINS`
4. Click en ella para editarla
5. Cambia el valor de `*` a la URL de Vercel:
   ```
   https://dashboard-clinico.vercel.app
   ```
6. **NO** agregues `/` al final
7. Click fuera para guardar
8. Railway se redespliegará automáticamente (toma ~1 minuto)

---

## ✅ PARTE 6: VERIFICAR QUE TODO FUNCIONA

### 6.1 Probar el Frontend

1. Abre tu aplicación en Vercel: `https://tu-proyecto.vercel.app`
2. Deberías ver el dashboard
3. Intenta subir el archivo `CubanDataset.csv` que está en la raíz del proyecto
4. Si se carga y ves las visualizaciones, ¡funciona! 🎉

### 6.2 Probar el Backend

1. Abre: `https://tu-proyecto.up.railway.app/docs`
2. Deberías ver la documentación de la API
3. Prueba el endpoint `/api/health` para verificar que está funcionando

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Failed to fetch" en el frontend

**Causa**: El frontend no puede conectarse al backend

**Solución**:
1. Verifica que `REACT_APP_BACKEND_URL` en Vercel sea correcta
2. Verifica que la URL de Railway esté activa
3. Abre DevTools (F12) en el navegador y revisa la consola

### Error: CORS en el navegador

**Causa**: El backend no permite peticiones desde el frontend

**Solución**:
1. Verifica que `CORS_ORIGINS` en Railway tenga la URL exacta de Vercel
2. NO incluyas `/` al final
3. Usa `https://` (no `http://`)

### Error: "MongoServerError: bad auth"

**Causa**: Usuario o contraseña incorrectos de MongoDB

**Solución**:
1. Verifica que hayas reemplazado `<password>` en la connection string
2. Verifica que la contraseña sea correcta
3. Intenta crear un nuevo usuario en MongoDB Atlas

### Error: "MongoNetworkError"

**Causa**: MongoDB no permite la conexión

**Solución**:
1. Ve a MongoDB Atlas → Network Access
2. Verifica que `0.0.0.0/0` esté en la lista
3. Espera 1-2 minutos después de agregarlo

---

## 🎉 ¡LISTO!

Tu aplicación ahora está desplegada y funcionando en:

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-proyecto.up.railway.app`
- **API Docs**: `https://tu-proyecto.up.railway.app/docs`

### Próximos Pasos

- Comparte la URL con tus compañeros o profesores
- Cada vez que hagas cambios, solo haz `git push` y se redespliegará automáticamente
- Monitorea el uso en Railway para no exceder el plan gratuito

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa los logs en Railway (Deployments → View Logs)
2. Revisa la consola del navegador (F12)
3. Consulta `ENV_VARIABLES.md` para verificar las variables
4. Consulta `DEPLOYMENT_GUIDE.md` para más detalles

