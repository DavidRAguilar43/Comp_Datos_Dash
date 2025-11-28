#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la conexión con OpenRouter.
Uso: python test_openrouter.py
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_api_key():
    """Verificar que la API key esté configurada."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY no está configurada")
        print("   Configúrala en Railway Dashboard → Variables")
        return False
    
    if not api_key.startswith('sk-or-v1-'):
        print(f"⚠️  WARNING: La API key no parece ser de OpenRouter")
        print(f"   Formato esperado: sk-or-v1-...")
        print(f"   Formato actual: {api_key[:10]}...")
        return False
    
    # Verificar si es una de las keys deshabilitadas
    disabled_keys = [
        "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",
        "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"
    ]
    
    if api_key in disabled_keys:
        print("❌ ERROR: Esta API key fue deshabilitada por seguridad")
        print("   Necesitas obtener una nueva key de: https://openrouter.ai/keys")
        print("   Y configurarla en Railway Dashboard → Variables")
        return False
    
    print(f"✅ API key configurada: {api_key[:15]}...{api_key[-4:]}")
    return True

def test_openai_client():
    """Verificar que el cliente de OpenAI se pueda inicializar."""
    try:
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No se puede crear cliente: API key no configurada")
            return False
        
        # Intentar crear el cliente
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        print("✅ Cliente OpenAI creado exitosamente")
        print(f"   Base URL: https://openrouter.ai/api/v1")
        return True
        
    except Exception as e:
        print(f"❌ Error creando cliente OpenAI: {e}")
        return False

def test_simple_request():
    """Hacer una petición simple a OpenRouter."""
    try:
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No se puede hacer petición: API key no configurada")
            return False
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        print("🔄 Haciendo petición de prueba a OpenRouter...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Di 'OK' si funciono correctamente"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ Respuesta recibida: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error en petición: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        
        # Verificar si es un error de autenticación
        if "401" in str(e) or "Unauthorized" in str(e):
            print("   → La API key es inválida o fue deshabilitada")
            print("   → Obtén una nueva en: https://openrouter.ai/keys")
        elif "429" in str(e):
            print("   → Límite de rate excedido")
        elif "500" in str(e):
            print("   → Error del servidor de OpenRouter")
        
        return False

def main():
    """Ejecutar todos los tests."""
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE OPENROUTER")
    print("=" * 60)
    print()
    
    print("1️⃣ Verificando API Key...")
    if not test_api_key():
        print("\n❌ FALLO: Configura una API key válida primero")
        sys.exit(1)
    print()
    
    print("2️⃣ Verificando Cliente OpenAI...")
    if not test_openai_client():
        print("\n❌ FALLO: No se pudo crear el cliente")
        sys.exit(1)
    print()
    
    print("3️⃣ Probando Conexión con OpenRouter...")
    if not test_simple_request():
        print("\n❌ FALLO: No se pudo conectar con OpenRouter")
        sys.exit(1)
    print()
    
    print("=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
    print("\nLa configuración de OpenRouter está correcta.")
    print("Si aún tienes errores 500, revisa los logs de Railway.")

if __name__ == "__main__":
    main()

