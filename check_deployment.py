#!/usr/bin/env python3
"""
Script de verificación pre-despliegue.
Verifica que todos los archivos necesarios estén presentes y configurados correctamente.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica si un archivo existe."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NO ENCONTRADO: {filepath}")
        return False

def check_gitignore():
    """Verifica que .gitignore bloquee archivos .env."""
    gitignore_path = ".gitignore"
    if not os.path.exists(gitignore_path):
        print(f"❌ .gitignore no encontrado")
        return False

    with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    required_patterns = ['.env', '*.env', 'venv/', 'node_modules/']
    missing = []
    
    for pattern in required_patterns:
        if pattern not in content:
            missing.append(pattern)
    
    if missing:
        print(f"⚠️  .gitignore falta patrones: {', '.join(missing)}")
        return False
    else:
        print(f"✅ .gitignore configurado correctamente")
        return True

def check_env_files():
    """Verifica que existan archivos .env.example pero NO archivos .env."""
    checks = []
    
    # Verificar que existan .env.example
    checks.append(check_file_exists("backend/.env.example", "Backend .env.example"))
    checks.append(check_file_exists("frontend/.env.example", "Frontend .env.example"))
    
    # Verificar que NO existan .env en el repositorio
    env_files = [
        "backend/.env",
        "frontend/.env",
        ".env"
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"⚠️  ADVERTENCIA: {env_file} existe - NO debe estar en el repositorio")
            checks.append(False)
    
    return all(checks)

def check_deployment_files():
    """Verifica que existan los archivos de configuración de despliegue."""
    files = [
        ("vercel.json", "Configuración de Vercel"),
        ("railway.json", "Configuración de Railway"),
        ("Procfile", "Procfile para Railway"),
        ("runtime.txt", "Runtime de Python"),
        ("nixpacks.toml", "Configuración de Nixpacks"),
        ("DEPLOYMENT_GUIDE.md", "Guía de despliegue"),
        ("QUICK_DEPLOY.md", "Guía rápida de despliegue")
    ]
    
    results = []
    for filepath, description in files:
        results.append(check_file_exists(filepath, description))
    
    return all(results)

def check_backend_structure():
    """Verifica la estructura del backend."""
    files = [
        ("backend/server.py", "Servidor FastAPI"),
        ("backend/requirements.txt", "Dependencias Python"),
        ("backend/services/data_processor.py", "Procesador de datos"),
        ("backend/services/ai_analyzer.py", "Analizador IA")
    ]
    
    results = []
    for filepath, description in files:
        results.append(check_file_exists(filepath, description))
    
    return all(results)

def check_frontend_structure():
    """Verifica la estructura del frontend."""
    files = [
        ("frontend/package.json", "Package.json"),
        ("frontend/src/App.js", "App.js"),
        ("frontend/src/index.js", "Index.js"),
        ("frontend/public/index.html", "Index.html")
    ]
    
    results = []
    for filepath, description in files:
        results.append(check_file_exists(filepath, description))
    
    return all(results)

def main():
    """Función principal."""
    print("=" * 60)
    print("🔍 VERIFICACIÓN PRE-DESPLIEGUE")
    print("=" * 60)
    print()
    
    # Cambiar al directorio del proyecto
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    checks = {
        "GitIgnore": check_gitignore(),
        "Archivos de Entorno": check_env_files(),
        "Archivos de Despliegue": check_deployment_files(),
        "Estructura Backend": check_backend_structure(),
        "Estructura Frontend": check_frontend_structure()
    }
    
    print()
    print("=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if not result:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 ¡Todo listo para el despliegue!")
        print()
        print("Próximos pasos:")
        print("1. Asegúrate de tener cuentas en Vercel, Railway y MongoDB Atlas")
        print("2. Lee QUICK_DEPLOY.md para un despliegue rápido")
        print("3. O lee DEPLOYMENT_GUIDE.md para instrucciones detalladas")
        return 0
    else:
        print("⚠️  Hay problemas que deben resolverse antes del despliegue")
        print("Por favor, revisa los errores arriba")
        return 1

if __name__ == "__main__":
    sys.exit(main())

