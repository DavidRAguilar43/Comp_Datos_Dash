# 🔐 Guía de Despliegue con Autenticación

Esta guía explica cómo configurar el sistema de autenticación JWT en producción (Vercel + Railway).

## 📋 Resumen de Cambios

### Backend
- ✅ Sistema de autenticación JWT implementado
- ✅ Endpoints de registro y login (`/api/auth/register`, `/api/auth/login`)
- ✅ Middleware de autenticación para rutas protegidas
- ✅ Modelos de usuario con hash de contraseñas (bcrypt)

### Frontend
- ✅ Contexto de autenticación (AuthContext)
- ✅ Componentes de Login y Register
- ✅ Rutas protegidas (ProtectedRoute)
- ✅ Interceptores HTTP para tokens JWT
- ✅ Botón de logout en Dashboard

---

## 🚀 Configuración en Railway (Backend)

### 1. Variables de Entorno Requeridas

Ve a tu proyecto en Railway → Variables → Agregar las siguientes:

```env
# MongoDB (ya existente)
MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=breast_cancer_dashboard

# CORS (actualizar con tu URL de Vercel)
CORS_ORIGINS=https://tu-app.vercel.app,https://tu-app.railway.app

# OpenAI (ya existente)
OPENAI_API_KEY=sk-...

# Server (ya existente)
HOST=0.0.0.0
PORT=8000

# ⭐ NUEVA: JWT Secret Key
JWT_SECRET=tu-clave-secreta-super-segura-generada-con-openssl
```

### 2. Generar JWT_SECRET Seguro

Ejecuta este comando en tu terminal local para generar una clave segura:

```bash
openssl rand -hex 32
```

Copia el resultado y úsalo como valor de `JWT_SECRET` en Railway.

**Ejemplo de salida:**
```
f8a3b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1
```

### 3. Redeploy

Railway detectará los cambios automáticamente y redesplegará el backend.

---

## 🌐 Configuración en Vercel (Frontend)

### 1. Variables de Entorno Requeridas

Ve a tu proyecto en Vercel → Settings → Environment Variables → Agregar:

```env
# Backend URL (ya existente, verificar que esté correcta)
REACT_APP_BACKEND_URL=https://tu-app.railway.app

# ESLint (ya existente)
DISABLE_ESLINT_PLUGIN=true
ESLINT_NO_DEV_ERRORS=true
```

**IMPORTANTE:** Asegúrate de que `REACT_APP_BACKEND_URL` apunte a tu URL de Railway (sin `/` al final).

### 2. Redeploy

Vercel redesplegará automáticamente cuando hagas push a Git.

---

## 🔄 Flujo de Autenticación

### 1. Registro de Usuario
```
Usuario → /register → Backend crea usuario → Retorna JWT token → Frontend guarda token → Redirige a Dashboard
```

### 2. Login
```
Usuario → /login → Backend valida credenciales → Retorna JWT token → Frontend guarda token → Redirige a Dashboard
```

### 3. Acceso a Rutas Protegidas
```
Usuario accede a / → ProtectedRoute verifica token → Si válido: muestra Dashboard → Si inválido: redirige a /login
```

### 4. Logout
```
Usuario click en "Salir" → Frontend elimina token → Redirige a /login
```

---

## 🧪 Pruebas Locales

### 1. Instalar Dependencias Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar .env Local

El archivo `backend/.env` ya está configurado con:
```env
JWT_SECRET=dev-secret-key-change-in-production-f8a3b2c1d4e5f6a7b8c9d0e1f2a3b4c5
```

### 3. Iniciar Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 4. Iniciar Frontend

```bash
cd frontend
npm install  # o yarn install
npm start    # o yarn start
```

### 5. Probar Autenticación

1. Abre http://localhost:3000
2. Deberías ser redirigido a `/login`
3. Click en "Regístrate aquí"
4. Crea una cuenta de prueba
5. Deberías ser redirigido al Dashboard
6. Verifica que aparezca tu nombre y el botón "Salir"

---

## 📝 Endpoints de API

### Públicos (no requieren autenticación)

- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión

### Protegidos (requieren token JWT)

- `GET /api/auth/me` - Obtener información del usuario actual
- Todos los demás endpoints del dashboard

---

## 🔒 Seguridad

### Mejores Prácticas Implementadas

✅ Contraseñas hasheadas con bcrypt
✅ Tokens JWT con expiración (24 horas)
✅ HTTPS en producción (Vercel + Railway)
✅ CORS configurado correctamente
✅ Validación de email con pydantic
✅ Contraseña mínima de 8 caracteres

### Recomendaciones Adicionales

- 🔐 Cambiar `JWT_SECRET` regularmente
- 🔐 Usar contraseñas fuertes
- 🔐 Habilitar 2FA en MongoDB Atlas
- 🔐 Monitorear logs de acceso

---

## 🐛 Troubleshooting

### Error: "Could not validate credentials"

**Causa:** Token inválido o expirado
**Solución:** Hacer logout y login nuevamente

### Error: "Email already registered"

**Causa:** El email ya existe en la base de datos
**Solución:** Usar otro email o hacer login

### Error: "Database not available"

**Causa:** MongoDB no está conectado
**Solución:** Verificar `MONGO_URL` en variables de entorno

### Frontend no redirige a login

**Causa:** AuthContext no está configurado correctamente
**Solución:** Verificar que `App.js` tenga `<AuthProvider>` envolviendo las rutas

---

## ✅ Checklist de Despliegue

### Backend (Railway)
- [ ] Variable `JWT_SECRET` configurada (generada con openssl)
- [ ] Variable `CORS_ORIGINS` incluye URL de Vercel
- [ ] Dependencias actualizadas en `requirements.txt`
- [ ] Backend desplegado y funcionando

### Frontend (Vercel)
- [ ] Variable `REACT_APP_BACKEND_URL` apunta a Railway
- [ ] Código pusheado a Git
- [ ] Vercel desplegado automáticamente
- [ ] Rutas `/login` y `/register` funcionan

### Pruebas
- [ ] Registro de usuario funciona
- [ ] Login funciona
- [ ] Dashboard requiere autenticación
- [ ] Logout funciona
- [ ] Token se renueva correctamente

---

## 📞 Soporte

Si encuentras problemas, verifica:
1. Logs de Railway (Backend)
2. Logs de Vercel (Frontend)
3. Consola del navegador (Errores JS)
4. Network tab (Peticiones HTTP)

