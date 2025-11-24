# 🔐 Crear Usuario Administrador

## Credenciales del Usuario Admin

He creado las credenciales para tu usuario administrador:

```
📧 Email:    admin@uabc.edu.mx
🔑 Password: 12345678
👤 Nombre:   Administrador
```

---

## 🚀 Cómo Crear el Usuario

### Opción 1: Usar el Formulario de Registro (MÁS FÁCIL) ✅

1. **Abre tu aplicación en Vercel:**
   ```
   https://comp-datos-dash.vercel.app
   ```
   (O la URL que te haya dado Vercel)

2. **Serás redirigido a `/login`**

3. **Click en "Regístrate aquí"**

4. **Completa el formulario con estas credenciales:**
   - Email: `admin@uabc.edu.mx`
   - Nombre completo: `Administrador`
   - Contraseña: `12345678`
   - Confirmar contraseña: `12345678`

5. **Click en "Crear Cuenta"**

6. **¡Listo!** Deberías ver el Dashboard

---

### Opción 2: Usar cURL (Si el frontend no funciona)

Si por alguna razón el frontend no está funcionando, puedes crear el usuario directamente con la API:

```bash
curl -X POST https://compdatosdash-production.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@uabc.edu.mx",
    "password": "12345678",
    "full_name": "Administrador"
  }'
```

**En PowerShell (Windows):**
```powershell
$body = @{
    email = "admin@uabc.edu.mx"
    password = "12345678"
    full_name = "Administrador"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://compdatosdash-production.up.railway.app/api/auth/register" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

### Opción 3: Usar Postman o Insomnia

1. **Abre Postman o Insomnia**

2. **Crea una nueva petición POST:**
   ```
   URL: https://compdatosdash-production.up.railway.app/api/auth/register
   Method: POST
   Headers: Content-Type: application/json
   ```

3. **Body (JSON):**
   ```json
   {
     "email": "admin@uabc.edu.mx",
     "password": "12345678",
     "full_name": "Administrador"
   }
   ```

4. **Envía la petición**

5. **Deberías recibir:**
   ```json
   {
     "access_token": "eyJ...",
     "token_type": "bearer",
     "user": {
       "email": "admin@uabc.edu.mx",
       "full_name": "Administrador"
     }
   }
   ```

---

## 🔐 Iniciar Sesión

Una vez creado el usuario, puedes iniciar sesión:

### En la Aplicación Web:
1. Ve a `https://comp-datos-dash.vercel.app/login`
2. Email: `admin@uabc.edu.mx`
3. Password: `12345678`
4. Click en "Iniciar Sesión"

### Con la API:
```bash
curl -X POST https://compdatosdash-production.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@uabc.edu.mx",
    "password": "12345678"
  }'
```

---

## ⚠️ IMPORTANTE: Cambiar Contraseña

**Esta es una contraseña temporal de prueba.** 

Después de iniciar sesión por primera vez, deberías cambiarla por una más segura.

(Nota: La funcionalidad de cambio de contraseña aún no está implementada. Si quieres que la agregue, avísame)

---

## 🔒 Deshabilitar Registro Público (Opcional)

Si quieres que **solo tú puedas crear nuevos usuarios** y deshabilitar el registro público:

1. Avísame y modificaré el código para:
   - Deshabilitar el endpoint `/api/auth/register` para usuarios no autenticados
   - Agregar un formulario en el Dashboard para que crees nuevos usuarios
   - Solo usuarios autenticados podrán crear cuentas

2. Haré commit y push de los cambios

3. Vercel y Railway redesplegarán automáticamente

---

## 📊 Verificar que el Usuario Existe

Puedes verificar que el usuario se creó correctamente:

```bash
# Primero, haz login para obtener el token
curl -X POST https://compdatosdash-production.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@uabc.edu.mx",
    "password": "12345678"
  }'

# Copia el access_token de la respuesta

# Luego, verifica tu información de usuario
curl -X GET https://compdatosdash-production.up.railway.app/api/auth/me \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## ✅ Resumen

**Credenciales:**
- Email: `admin@uabc.edu.mx`
- Password: `12345678`

**Método más fácil:**
1. Ve a tu app en Vercel
2. Click en "Regístrate aquí"
3. Usa las credenciales de arriba
4. ¡Listo!

**URLs:**
- Frontend: https://comp-datos-dash.vercel.app
- Backend: https://compdatosdash-production.up.railway.app
- API Docs: https://compdatosdash-production.up.railway.app/docs

