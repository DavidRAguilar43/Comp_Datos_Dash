# ⚡ Despliegue Rápido - 5 Minutos

## 🎯 Checklist Rápido

### 1️⃣ MongoDB Atlas (2 min)
- [ ] Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
- [ ] Crear cluster gratuito M0
- [ ] Crear usuario de base de datos
- [ ] Permitir acceso desde cualquier IP (0.0.0.0/0)
- [ ] Copiar connection string

### 2️⃣ GitHub (1 min)
```bash
cd Comp_Datos_Dash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU-USUARIO/dashboard-clinico.git
git push -u origin main
```

### 3️⃣ Railway - Backend (1 min)
- [ ] Ir a [Railway](https://railway.app)
- [ ] "New Project" → "Deploy from GitHub"
- [ ] Seleccionar repositorio
- [ ] Agregar variables de entorno:
  ```
  MONGO_URL=mongodb+srv://...
  DB_NAME=breast_cancer_dashboard
  CORS_ORIGINS=*
  OPENAI_API_KEY=sk-...
  PORT=8000
  ```
- [ ] Copiar URL generada (ej: `https://xxx.up.railway.app`)

### 4️⃣ Vercel - Frontend (1 min)
- [ ] Ir a [Vercel](https://vercel.com)
- [ ] "New Project" → Importar repositorio
- [ ] Root Directory: `frontend`
- [ ] Framework: Create React App
- [ ] Variable de entorno:
  ```
  REACT_APP_BACKEND_URL=https://xxx.up.railway.app
  ```
- [ ] Deploy

### 5️⃣ Actualizar CORS (30 seg)
- [ ] Volver a Railway
- [ ] Actualizar `CORS_ORIGINS` con URL de Vercel
- [ ] Guardar

## ✅ ¡Listo!

Tu app está en línea en:
- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-proyecto.up.railway.app`
- **API Docs**: `https://tu-proyecto.up.railway.app/docs`

---

## 🆘 Problemas Comunes

| Problema | Solución |
|----------|----------|
| Error CORS | Actualiza `CORS_ORIGINS` en Railway con URL de Vercel |
| Error MongoDB | Verifica IP whitelist (0.0.0.0/0) y connection string |
| Frontend no carga | Verifica `REACT_APP_BACKEND_URL` en Vercel |
| Error 500 | Revisa logs en Railway → Deployments → View Logs |

---

## 📝 Variables de Entorno Requeridas

### Railway (Backend)
```env
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=https://tu-frontend.vercel.app
OPENAI_API_KEY=sk-...
PORT=8000
ENVIRONMENT=production
```

### Vercel (Frontend)
```env
REACT_APP_BACKEND_URL=https://tu-backend.railway.app
```

---

## 🔗 Enlaces Útiles

- [Guía Completa de Despliegue](./DEPLOYMENT_GUIDE.md)
- [Documentación del Proyecto](./README.md)
- [Estructura del Proyecto](./ProjectStructure.md)

