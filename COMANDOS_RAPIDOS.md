# ⚡ Comandos Rápidos - Copiar y Pegar

## 🐙 Subir a GitHub

```bash
# 1. Inicializar Git
git init

# 2. Agregar archivos
git add .

# 3. Commit
git commit -m "Initial commit - Dashboard Clinico"

# 4. Conectar con GitHub (REEMPLAZA TU-USUARIO)
git remote add origin https://github.com/TU-USUARIO/dashboard-clinico.git

# 5. Cambiar a main
git branch -M main

# 6. Push
git push -u origin main
```

---

## 🚂 Variables de Entorno para RAILWAY

Copia y pega estas variables en Railway → Variables:

```
MONGO_URL=mongodb+srv://dashboard_user:TU_PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=*
OPENAI_API_KEY=sk-tu-clave-aqui
PORT=8000
ENVIRONMENT=production
```

**Después de desplegar en Vercel, actualiza**:
```
CORS_ORIGINS=https://tu-proyecto.vercel.app
```

---

## ▲ Variables de Entorno para VERCEL

En Vercel → Settings → Environment Variables:

```
REACT_APP_BACKEND_URL=https://tu-proyecto.up.railway.app
```

---

## 🔄 Actualizar Código (después del primer despliegue)

```bash
# 1. Agregar cambios
git add .

# 2. Commit con mensaje descriptivo
git commit -m "Descripción de tus cambios"

# 3. Push (se redespliegará automáticamente)
git push
```

---

## 🧪 Probar Localmente Antes de Desplegar

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

---

## 📋 URLs Importantes

Después del despliegue, guarda estas URLs:

```
Frontend (Vercel):     https://_____________________.vercel.app
Backend (Railway):     https://_____________________.up.railway.app
API Docs:              https://_____________________.up.railway.app/docs
MongoDB Atlas:         https://cloud.mongodb.com
GitHub Repo:           https://github.com/___________/dashboard-clinico
```

---

## 🔍 Verificar Despliegue

### Verificar Backend
```bash
# En tu navegador, abre:
https://tu-proyecto.up.railway.app/docs

# Deberías ver la documentación de la API
```

### Verificar Frontend
```bash
# En tu navegador, abre:
https://tu-proyecto.vercel.app

# Deberías ver el dashboard
```

---

## 🆘 Comandos de Diagnóstico

### Ver logs de Git
```bash
git log --oneline
```

### Ver estado de Git
```bash
git status
```

### Ver remotes configurados
```bash
git remote -v
```

### Verificar archivos ignorados
```bash
git check-ignore -v *
```

---

## 🔧 Solucionar Problemas Comunes

### Si Git dice "nothing to commit"
```bash
git status
# Verifica qué archivos están siendo ignorados
```

### Si falla el push por autenticación
```bash
# Usa un Personal Access Token en lugar de tu contraseña
# Créalo en: https://github.com/settings/tokens
```

### Si Railway no detecta Python
```bash
# Verifica que runtime.txt exista en la raíz
cat runtime.txt
# Debería decir: python-3.11.9
```

### Si Vercel no encuentra el frontend
```bash
# Verifica que la Root Directory sea: frontend
# Verifica que package.json exista en frontend/
```

---

## 📦 Reinstalar Dependencias

### Backend
```bash
cd backend
pip install -r requirements.txt --upgrade
```

### Frontend
```bash
cd frontend
npm install
# o
npm ci  # Instalación limpia
```

---

## 🗑️ Limpiar y Empezar de Nuevo

### Limpiar Git
```bash
# CUIDADO: Esto borra el historial de Git
rm -rf .git
git init
```

### Limpiar dependencias de Frontend
```bash
cd frontend
rm -rf node_modules
rm package-lock.json
npm install
```

### Limpiar entorno virtual de Backend
```bash
cd backend
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ✅ Checklist Final

Antes de considerar el despliegue completo:

- [ ] Código subido a GitHub
- [ ] Backend desplegado en Railway
- [ ] Frontend desplegado en Vercel
- [ ] Variables de entorno configuradas en Railway
- [ ] Variables de entorno configuradas en Vercel
- [ ] CORS actualizado con URL de Vercel
- [ ] Backend responde en /docs
- [ ] Frontend carga correctamente
- [ ] Puedes subir un CSV y ver visualizaciones
- [ ] El análisis con IA funciona

---

## 🎯 Comandos de Emergencia

### Si todo falla, ejecuta el asistente:
```bash
python deploy_assistant.py
```

### O sigue la guía manual:
```bash
# Abre en tu navegador:
MANUAL_DEPLOY.md
```

---

## 📞 Recursos de Ayuda

- **Guía Manual Completa**: `MANUAL_DEPLOY.md`
- **Guía Rápida**: `QUICK_DEPLOY.md`
- **Variables de Entorno**: `ENV_VARIABLES.md`
- **Guía Detallada**: `DEPLOYMENT_GUIDE.md`
- **Asistente Interactivo**: `python deploy_assistant.py`

