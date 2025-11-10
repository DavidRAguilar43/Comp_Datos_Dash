# 🚀 Inicio Rápido - Dashboard Clínico

## ⚡ Configuración en 5 Minutos

### 1️⃣ Configurar Backend (2 minutos)

```bash
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de configuración
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

**Editar `backend/.env`** (abrir con notepad/nano/vim):
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard
CORS_ORIGINS=http://localhost:3000
OPENAI_API_KEY=sk-tu_clave_aqui  # ⚠️ IMPORTANTE: Agregar tu clave de OpenAI
```

### 2️⃣ Configurar Frontend (2 minutos)

```bash
# Navegar a la carpeta frontend (desde la raíz del proyecto)
cd frontend

# Instalar dependencias
yarn install

# Crear archivo de configuración
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

**Editar `frontend/.env`**:
```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

### 3️⃣ Iniciar Aplicación (1 minuto)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Activar entorno virtual
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

### 4️⃣ Usar el Dashboard

1. El navegador se abrirá automáticamente en `http://localhost:3000`
2. Arrastra el archivo `CubanDataset.csv` al área de carga
3. Haz clic en "Cargar y Analizar Datos"
4. ¡Explora las visualizaciones y genera insights con IA! 🎉

## 📋 Requisitos Previos

- ✅ Python 3.10 o superior
- ✅ Node.js 16 o superior
- ✅ Yarn (instalar con `npm install -g yarn`)
- ✅ MongoDB (local o en la nube)
- ✅ Clave API de OpenAI (obtener en https://platform.openai.com/api-keys)

## 🔍 Verificar Instalación

### Backend
```bash
# Debería mostrar: {"message": "Breast Cancer Risk Factors Dashboard API"}
curl http://localhost:8000/

# O abrir en navegador:
http://localhost:8000/docs  # Documentación interactiva de la API
```

### Frontend
```bash
# Debería abrir el dashboard en el navegador
http://localhost:3000
```

## ❓ Problemas Comunes

### "Python no reconocido"
**Solución**: Instalar Python desde https://www.python.org/downloads/

### "Yarn no reconocido"
**Solución**: 
```bash
npm install -g yarn
```

### "MongoDB connection error"
**Solución**: 
- Instalar MongoDB: https://www.mongodb.com/try/download/community
- O usar MongoDB Atlas (gratis): https://www.mongodb.com/cloud/atlas

### "OpenAI API error"
**Solución**: 
- Obtener clave API en: https://platform.openai.com/api-keys
- Agregar al archivo `backend/.env`

### "CORS error"
**Solución**: 
- Verificar que `CORS_ORIGINS` en `backend/.env` incluya `http://localhost:3000`

## 📚 Documentación Completa

- **README.md** - Guía completa del proyecto
- **TESTING.md** - Guía de pruebas detallada
- **ProjectStructure.md** - Arquitectura y estructura
- **IMPLEMENTATION_SUMMARY.md** - Resumen de implementación

## 🎯 Próximos Pasos

1. ✅ Cargar datos y explorar visualizaciones
2. ✅ Generar insights con IA
3. ✅ Analizar correlaciones
4. ✅ Exportar resultados
5. ✅ Leer la documentación completa
6. ✅ Personalizar según tus necesidades

## 💡 Tips

- **Datos de Prueba**: Usa `CubanDataset.csv` incluido en el proyecto
- **API Docs**: Explora `http://localhost:8000/docs` para ver todos los endpoints
- **Tema Visual**: Los colores pasteles son personalizables en `frontend/src/index.css`
- **Análisis IA**: Requiere créditos de OpenAI (muy económico para uso académico)

## 🆘 Soporte

Si tienes problemas:
1. Revisa **TESTING.md** para soluciones detalladas
2. Verifica que todos los requisitos estén instalados
3. Asegúrate de que MongoDB esté corriendo
4. Verifica las variables de entorno en `.env`

---

**¡Listo para analizar datos clínicos! 🎗️**

