#!/usr/bin/env python3
"""
Script para arreglar el error de Railway y subir los cambios a GitHub.
"""

import subprocess
import sys
import os

def print_header(text):
    """Imprime un encabezado."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_command(command, show_output=True):
    """Ejecuta un comando."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if show_output and result.stdout:
            print(result.stdout)
        if result.stderr and "warning" not in result.stderr.lower():
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal."""
    print_header("🔧 ARREGLAR ERROR DE RAILWAY")
    
    print("Este script va a:")
    print("1. Verificar los archivos de configuración")
    print("2. Agregar los cambios a Git")
    print("3. Hacer commit")
    print("4. Subir a GitHub")
    print()
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verificar archivos
    print("📋 Verificando archivos...")
    required_files = [
        "requirements.txt",
        "nixpacks.toml",
        "railway.json",
        "Procfile",
        "runtime.txt"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - FALTA")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Faltan archivos: {', '.join(missing)}")
        print("Por favor ejecuta primero el asistente de despliegue.")
        return 1
    
    # Git status
    print("\n📊 Estado de Git:")
    run_command("git status --short")
    
    # Add
    print("\n📦 Agregando archivos a Git...")
    if run_command("git add ."):
        print("✅ Archivos agregados")
    else:
        print("❌ Error al agregar archivos")
        return 1
    
    # Commit
    print("\n💾 Haciendo commit...")
    commit_msg = "Fix Railway deployment - Add requirements.txt and update config"
    if run_command(f'git commit -m "{commit_msg}"'):
        print("✅ Commit realizado")
    else:
        # Puede que no haya cambios
        print("⚠️  No hay cambios para hacer commit (puede que ya estén subidos)")
    
    # Push
    print("\n🚀 Subiendo a GitHub...")
    print("(Esto puede tomar un momento...)")
    
    if run_command("git push"):
        print("✅ Cambios subidos a GitHub exitosamente")
    else:
        print("❌ Error al subir a GitHub")
        print("\n💡 Posibles soluciones:")
        print("1. Verifica que tengas acceso al repositorio")
        print("2. Usa un Personal Access Token si te pide contraseña")
        print("3. Ejecuta manualmente: git push")
        return 1
    
    # Instrucciones finales
    print("\n" + "=" * 70)
    print("✅ CAMBIOS SUBIDOS EXITOSAMENTE")
    print("=" * 70)
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("\n1. Ve a Railway (https://railway.app)")
    print("2. Tu proyecto se redespliegará automáticamente")
    print("3. Espera 2-3 minutos")
    print("4. Verifica que el deployment sea exitoso")
    print("\n5. Si sigue fallando:")
    print("   - Ve a Deployments → View Logs")
    print("   - Copia el error y dímelo")
    print("\n6. Si funciona:")
    print("   - Copia la URL del backend")
    print("   - Úsala en Vercel como REACT_APP_BACKEND_URL")
    
    print("\n" + "=" * 70)
    print("🎉 ¡Listo! Ahora revisa Railway")
    print("=" * 70 + "\n")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Cancelado por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

