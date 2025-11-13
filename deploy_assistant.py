#!/usr/bin/env python3
"""
Asistente de Despliegue Interactivo
Este script te guiará paso a paso en el despliegue del proyecto.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(number, text):
    """Imprime un paso numerado."""
    print(f"\n{'🔹' * 35}")
    print(f"  PASO {number}: {text}")
    print(f"{'🔹' * 35}\n")

def ask_yes_no(question):
    """Pregunta sí/no al usuario."""
    while True:
        response = input(f"{question} (s/n): ").lower().strip()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Por favor responde 's' o 'n'")

def run_command(command, cwd=None):
    """Ejecuta un comando y muestra el resultado."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """Verifica el estado de Git."""
    print_step(1, "Verificando Git")
    
    # Verificar si Git está instalado
    success, stdout, stderr = run_command("git --version")
    if not success:
        print("❌ Git no está instalado. Por favor instala Git primero.")
        print("   Descarga: https://git-scm.com/download/win")
        return False
    
    print(f"✅ Git instalado: {stdout.strip()}")
    
    # Verificar si ya es un repositorio Git
    if os.path.exists(".git"):
        print("✅ Ya es un repositorio Git")
        return True
    else:
        print("⚠️  No es un repositorio Git todavía")
        if ask_yes_no("¿Quieres inicializar Git ahora?"):
            success, stdout, stderr = run_command("git init")
            if success:
                print("✅ Repositorio Git inicializado")
                return True
            else:
                print(f"❌ Error al inicializar Git: {stderr}")
                return False
        return False

def setup_github():
    """Configura GitHub."""
    print_step(2, "Configurar GitHub")
    
    print("Para subir tu código a GitHub, necesitas:")
    print("1. Una cuenta en GitHub (https://github.com)")
    print("2. Crear un nuevo repositorio")
    print()
    
    if not ask_yes_no("¿Ya creaste un repositorio en GitHub?"):
        print("\n📝 Instrucciones:")
        print("1. Ve a https://github.com/new")
        print("2. Nombre del repositorio: dashboard-clinico")
        print("3. Visibilidad: Private (recomendado)")
        print("4. NO marques 'Initialize with README'")
        print("5. Click en 'Create repository'")
        print()
        input("Presiona ENTER cuando hayas creado el repositorio...")
    
    repo_url = input("\n📎 Pega la URL de tu repositorio (ej: https://github.com/usuario/repo.git): ").strip()
    
    if not repo_url:
        print("❌ URL no proporcionada")
        return False, None
    
    # Configurar remote
    print("\n🔗 Configurando remote...")
    run_command("git remote remove origin")  # Remover si existe
    success, stdout, stderr = run_command(f'git remote add origin "{repo_url}"')
    
    if success or "already exists" in stderr:
        print("✅ Remote configurado")
        return True, repo_url
    else:
        print(f"❌ Error: {stderr}")
        return False, None

def commit_and_push():
    """Hace commit y push del código."""
    print_step(3, "Subir código a GitHub")
    
    print("📦 Preparando archivos...")
    
    # Add all files
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"⚠️  Advertencia al agregar archivos: {stderr}")
    
    # Commit
    print("💾 Haciendo commit...")
    success, stdout, stderr = run_command('git commit -m "Initial commit - Dashboard Clinico"')
    if not success and "nothing to commit" not in stderr:
        print(f"⚠️  {stderr}")
    
    # Check branch
    success, stdout, stderr = run_command("git branch -M main")
    
    # Push
    print("🚀 Subiendo a GitHub...")
    print("(Esto puede tomar un momento...)")
    success, stdout, stderr = run_command("git push -u origin main")
    
    if success or "up-to-date" in stderr:
        print("✅ Código subido exitosamente a GitHub")
        return True
    else:
        print(f"❌ Error al subir: {stderr}")
        print("\n💡 Si te pide autenticación:")
        print("   - Usuario: tu nombre de usuario de GitHub")
        print("   - Contraseña: usa un Personal Access Token")
        print("   - Cómo crear token: https://github.com/settings/tokens")
        return False

def collect_env_variables():
    """Recolecta las variables de entorno."""
    print_step(4, "Recolectar Variables de Entorno")
    
    env_vars = {}
    
    print("Necesitamos configurar las variables de entorno.")
    print("Puedes dejar algunas en blanco y configurarlas después.\n")
    
    # MongoDB
    print("🗄️  MONGODB")
    print("Si no tienes MongoDB Atlas:")
    print("   1. Ve a https://www.mongodb.com/cloud/atlas/register")
    print("   2. Crea un cluster gratuito (M0)")
    print("   3. Crea un usuario de base de datos")
    print("   4. Permite acceso desde cualquier IP (0.0.0.0/0)")
    print("   5. Obtén la connection string\n")
    
    mongo_url = input("MONGO_URL (connection string) [Enter para omitir]: ").strip()
    if mongo_url:
        env_vars['MONGO_URL'] = mongo_url
    
    # OpenAI
    print("\n🤖 OPENAI")
    print("Si no tienes API Key de OpenAI:")
    print("   1. Ve a https://platform.openai.com/api-keys")
    print("   2. Crea una nueva API key")
    print("   3. Copia la key (empieza con 'sk-')\n")
    
    openai_key = input("OPENAI_API_KEY [Enter para omitir]: ").strip()
    if openai_key:
        env_vars['OPENAI_API_KEY'] = openai_key
    
    return env_vars

def save_env_config(env_vars):
    """Guarda la configuración de variables de entorno."""
    config_file = "deployment_config.json"
    
    config = {
        "backend_env": {
            "MONGO_URL": env_vars.get('MONGO_URL', ''),
            "DB_NAME": "breast_cancer_dashboard",
            "CORS_ORIGINS": "*",
            "OPENAI_API_KEY": env_vars.get('OPENAI_API_KEY', ''),
            "PORT": "8000",
            "ENVIRONMENT": "production"
        },
        "frontend_env": {
            "REACT_APP_BACKEND_URL": "https://TU-PROYECTO.up.railway.app"
        }
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuración guardada en {config_file}")
    return config

def show_deployment_instructions(config):
    """Muestra las instrucciones finales de despliegue."""
    print_step(5, "Desplegar en Railway y Vercel")
    
    print("📋 INSTRUCCIONES FINALES:\n")
    
    print("=" * 70)
    print("🚂 RAILWAY (Backend)")
    print("=" * 70)
    print("1. Ve a https://railway.app")
    print("2. Click en 'Start a New Project'")
    print("3. Selecciona 'Deploy from GitHub repo'")
    print("4. Autoriza Railway y selecciona tu repositorio")
    print("5. En 'Variables', agrega estas variables:\n")
    
    for key, value in config['backend_env'].items():
        if value:
            print(f"   {key}={value}")
        else:
            print(f"   {key}=<PENDIENTE>")
    
    print("\n6. Railway generará una URL como: https://xxx.up.railway.app")
    print("7. COPIA ESA URL (la necesitarás para Vercel)\n")
    
    print("=" * 70)
    print("▲ VERCEL (Frontend)")
    print("=" * 70)
    print("1. Ve a https://vercel.com")
    print("2. Click en 'Add New...' → 'Project'")
    print("3. Import tu repositorio de GitHub")
    print("4. Configuración:")
    print("   - Framework Preset: Create React App")
    print("   - Root Directory: frontend")
    print("   - Build Command: npm run build")
    print("   - Output Directory: build")
    print("5. En 'Environment Variables', agrega:")
    print(f"   REACT_APP_BACKEND_URL=<URL_DE_RAILWAY>")
    print("6. Click en 'Deploy'")
    print("7. Vercel te dará una URL como: https://xxx.vercel.app\n")
    
    print("=" * 70)
    print("🔄 ACTUALIZAR CORS")
    print("=" * 70)
    print("1. Vuelve a Railway")
    print("2. Actualiza la variable CORS_ORIGINS con la URL de Vercel")
    print("3. Guarda (se redespliegará automáticamente)\n")

def main():
    """Función principal."""
    print_header("🚀 ASISTENTE DE DESPLIEGUE - DASHBOARD CLÍNICO")
    
    print("Este asistente te ayudará a desplegar tu proyecto paso a paso.")
    print("Puedes detenerlo en cualquier momento con Ctrl+C\n")
    
    if not ask_yes_no("¿Quieres continuar?"):
        print("👋 ¡Hasta luego!")
        return 0
    
    # Cambiar al directorio del proyecto
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Paso 1: Git
    if not check_git_status():
        print("\n❌ No se pudo configurar Git. Por favor revisa los errores.")
        return 1
    
    # Paso 2: GitHub
    success, repo_url = setup_github()
    if not success:
        print("\n⚠️  No se configuró GitHub. Puedes hacerlo manualmente después.")
    
    # Paso 3: Push
    if success and ask_yes_no("¿Quieres subir el código a GitHub ahora?"):
        commit_and_push()
    
    # Paso 4: Variables de entorno
    env_vars = collect_env_variables()
    config = save_env_config(env_vars)
    
    # Paso 5: Instrucciones finales
    show_deployment_instructions(config)
    
    print("\n" + "=" * 70)
    print("✅ ASISTENTE COMPLETADO")
    print("=" * 70)
    print("\n📚 Recursos adicionales:")
    print("   - Guía rápida: QUICK_DEPLOY.md")
    print("   - Guía completa: DEPLOYMENT_GUIDE.md")
    print("   - Variables de entorno: ENV_VARIABLES.md")
    print("   - Configuración guardada: deployment_config.json")
    print("\n🎉 ¡Buena suerte con tu despliegue!\n")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Asistente cancelado por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

