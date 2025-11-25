# 🔐 Guía de Seguridad - Manejo de Secrets y API Keys

## ⚠️ REGLAS CRÍTICAS DE SEGURIDAD

### 🚫 NUNCA HACER:

1. **NUNCA** incluir API keys, passwords o secrets en archivos que se suban a Git
2. **NUNCA** hacer commit de archivos `.env` con valores reales
3. **NUNCA** incluir secrets en documentación (README, guías, etc.)
4. **NUNCA** compartir API keys en issues, pull requests o comentarios de código
5. **NUNCA** hacer hardcode de credentials en el código fuente

### ✅ SIEMPRE HACER:

1. **SIEMPRE** usar variables de entorno para secrets
2. **SIEMPRE** usar placeholders en documentación (ej: `tu_api_key_aqui`)
3. **SIEMPRE** verificar que `.gitignore` bloquee archivos `.env`
4. **SIEMPRE** rotar API keys si fueron expuestas accidentalmente
5. **SIEMPRE** usar archivos `.env.example` con valores de ejemplo

---

## 📋 Configuración Correcta de Secrets en Railway

### Paso 1: Obtener tu API Key de OpenRouter

1. Ve a [OpenRouter](https://openrouter.ai/keys)
2. Inicia sesión o crea una cuenta
3. Genera una nueva API key
4. **Copia la key** (empieza con `sk-or-v1-...`)
5. **NO la pegues en ningún archivo de código**

### Paso 2: Configurar Variables de Entorno en Railway

1. Ve a [Railway Dashboard](https://railway.app)
2. Selecciona tu proyecto
3. Haz clic en el servicio **backend**
4. Ve a la pestaña **"Variables"**
5. Haz clic en **"New Variable"**
6. Agrega las siguientes variables:

```
OPENAI_API_KEY=<pega_tu_api_key_aqui>
CORS_ORIGINS=https://comp-datos-dash.vercel.app,http://localhost:3000
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard
JWT_SECRET=<genera_un_secret_seguro>
```

7. Haz clic en **"Add"** para cada variable
8. Railway redesplegará automáticamente

### Paso 3: Generar JWT Secret Seguro

```bash
# En PowerShell (Windows)
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})

# En Linux/Mac
openssl rand -hex 32
```

---

## 🔧 Configuración Local (Desarrollo)

### Archivo `.env` Local

Crea un archivo `backend/.env` con:

```env
# OpenRouter API Key
OPENAI_API_KEY=tu_openrouter_api_key_aqui

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Database
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard

# JWT Secret (genera uno único)
JWT_SECRET=tu_jwt_secret_seguro_aqui
```

**⚠️ IMPORTANTE:**
- Este archivo **NO** debe subirse a Git
- Está bloqueado por `.gitignore`
- Cada desarrollador debe crear su propio `.env`

### Archivo `.env.example` (Template)

Crea `backend/.env.example` con placeholders:

```env
# OpenRouter API Key - Obtén la tuya en https://openrouter.ai/keys
OPENAI_API_KEY=sk-or-v1-your_api_key_here

# CORS Origins (separados por comas)
CORS_ORIGINS=http://localhost:3000

# MongoDB Connection
MONGO_URL=mongodb://localhost:27017
DB_NAME=breast_cancer_dashboard

# JWT Secret (genera con: openssl rand -hex 32)
JWT_SECRET=your_secure_jwt_secret_here
```

Este archivo **SÍ** se sube a Git como referencia.

---

## 🚨 Qué Hacer Si Expones una API Key

### Acción Inmediata (Primeros 5 minutos):

1. **Deshabilitar la API key expuesta:**
   - Ve a [OpenRouter Keys](https://openrouter.ai/keys)
   - Revoca/elimina la key comprometida
   - Genera una nueva key

2. **Actualizar Railway:**
   - Ve a Railway → Variables
   - Actualiza `OPENAI_API_KEY` con la nueva key
   - Railway redesplegará automáticamente

### Limpieza del Historial de Git:

Si la key fue commiteada a Git:

1. **Remover del archivo actual:**
   ```bash
   # Edita el archivo y reemplaza la key con placeholder
   git add archivo_modificado.md
   git commit -m "security: remove exposed API key"
   ```

2. **Limpiar historial (PELIGROSO - hace force push):**
   ```bash
   # Crear backup primero
   git clone --mirror <repo_url> backup-repo
   
   # Limpiar historial
   git filter-branch --force --tree-filter \
     'if [ -f "archivo.md" ]; then \
        sed -i "s/sk-or-v1-EXPOSED_KEY/tu_api_key_aqui/g" "archivo.md"; \
      fi' \
     --tag-name-filter cat -- --all
   
   # Force push (CUIDADO: reescribe historial)
   git push --force origin main
   ```

3. **Notificar al equipo:**
   - Todos deben hacer `git pull --rebase`
   - Eliminar sus copias locales antiguas

---

## ✅ Checklist de Seguridad

Antes de cada commit, verifica:

- [ ] No hay API keys en archivos modificados
- [ ] Archivos `.env` no están en staging (`git status`)
- [ ] Documentación usa placeholders, no valores reales
- [ ] Secrets están solo en Railway/Vercel, no en código
- [ ] `.gitignore` está actualizado

Antes de cada push:

- [ ] Revisar diff: `git diff origin/main`
- [ ] Buscar patterns: `git grep -i "sk-or-v1-[a-f0-9]\{64\}"`
- [ ] Verificar que no hay secrets expuestos

---

## 📚 Referencias

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Railway Environment Variables](https://docs.railway.app/develop/variables)
- [Git Secrets Prevention](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Última actualización:** 2025-11-25  
**Mantenido por:** Equipo de Desarrollo

