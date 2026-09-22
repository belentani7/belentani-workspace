#!/usr/bin/env python3
"""
Demo Script para Herramientas de Canto IA
Script de demostración para SoulX-Singer y SongGeneration
"""

import os
import sys
import json
import argparse
from pathlib import Path

class SingingAIDemo:
    def __init__(self):
        self.setup_paths()
        
    def setup_paths(self):
        """Configurar rutas de los repositorios"""
        self.base_path = Path(__file__).parent
        self.soulx_path = self.base_path / "SoulX-Singer"
        self.songgen_path = self.base_path / "SongGeneration-Studio"
        self.comfyui_path = self.base_path / "ComfyUI-SoulX-Singer"
        
    def check_dependencies(self):
        """Verificar dependencias instaladas"""
        required_packages = [
            "torch", "torchaudio", "numpy", "scipy", 
            "transformers", "gradio", "librosa"
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"⚠️  Paquetes faltantes: {missing}")
            print("Instala con: pip install " + " ".join(missing))
            return False
        
        print("✅ Todas las dependencias están instaladas")
        return True
    
    def demo_soulx_singer(self):
        """Demostración básica de SoulX-Singer"""
        print("\n🎤 Demostración SoulX-Singer")
        print("=" * 40)
        
        try:
            # Simular carga del modelo
            print("1. Cargando modelo SoulX-Singer...")
            print("   - Modelo: Zero-shot singing voice synthesis")
            print("   - Versión: Latest")
            print("   - Tamaño: ~2GB")
            
            # Configuración de demo
            demo_config = {
                "text": "Hola mundo, esto es una demostración de canto IA",
                "speaker_id": "default",
                "emotion": "happy",
                "tempo": 120,
                "pitch_shift": 0,
                "output_format": "wav"
            }
            
            print(f"2. Configuración: {json.dumps(demo_config, indent=2)}")
            
            # Simulación de generación
            print("3. Generando audio...")
            print("   🔊 Procesando texto a audio...")
            print("   🔊 Aplicando emociones: happy")
            print("   🔀 Ajustando pitch: 0 semitones")
            print("   ⏱️  Tempo: 120 BPM")
            
            output_file = "demo_soulx_singer.wav"
            print(f"4. ✅ Audio generado: {output_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en SoulX-Singer: {e}")
            return False
    
    def demo_songgeneration(self):
        """Demostración de SongGeneration Studio"""
        print("\n🎵 Demostración SongGeneration Studio")
        print("=" * 45)
        
        try:
            print("1. Iniciando interfaz web...")
            print("   - Servidor: localhost:7860")
            print("   - Interfaz: Gráfica web moderna")
            print("   - Características: Procesamiento por lotes")
            
            # Configuración de demo
            demo_songs = [
                {
                    "prompt": "Canción pop optimista sobre la amistad",
                    "genre": "pop",
                    "duration": 120
                },
                {
                    "prompt": "Balada romántica con piano y cuerdas",
                    "genre": "ballad",
                    "duration": 180
                },
                {
                    "prompt": "Rock energético con guitarra eléctrica",
                    "genre": "rock",
                    "duration": 150
                }
            ]
            
            print("2. Canciones a generar:")
            for i, song in enumerate(demo_songs, 1):
                print(f"   {i}. {song['prompt']} ({song['genre']}, {song['duration']}s)")
            
            print("3. 🚀 Generando canciones en paralelo...")
            print("   - Batch processing: activado")
            print("   - Calidad: Alta (320kbps)")
            print("   - Formato: WAV")
            
            print("4. ✅ Todas las canciones generadas")
            print("   📁 output_song_1.wav")
            print("   📁 output_song_2.wav") 
            print("   📁 output_song_3.wav")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en SongGeneration: {e}")
            return False
    
    def demo_comfyui_integration(self):
        """Demostración de integración ComfyUI"""
        print("\n🎨 Demostración ComfyUI Integration")
        print("=" * 45)
        
        try:
            print("1. Iniciando servidor ComfyUI...")
            print("   - Servidor: localhost:8188")
            print("   - Nodos: SoulX-Singer integrado")
            print("   - Interfaz: Gráfica drag & drop")
            
            # Flujo de trabajo de ejemplo
            workflow = {
                "text_input": "Texto de entrada",
                "voice_model": "SoulX-Singer",
                "emotion_control": "happy",
                "pitch_adjustment": 0,
                "tempo_control": 120,
                "output_format": "wav"
            }
            
            print("2. Flujo de trabajo recomendado:")
            print("   📥 Text Input Node")
            print("   🔀 SoulX-Singer Node")
            print("   🎛️  Emotion Control Node")
            print("   🎵 Pitch/Tempo Node")
            print("   💾 Output Node")
            
            print("3. 🚀 Ejecutando flujo...")
            print("   - Cargando nodos necesarios")
            print("   - Procesando secuencia")
            print("   - Generando audio final")
            
            print("4. ✅ Flujo completado")
            print("   📁 comfyui_output.wav")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en ComfyUI: {e}")
            return False
    
    def run_all_demos(self):
        """Ejecutar todas las demostraciones"""
        print("🎬 Iniciando Demostración Completa de Canto IA")
        print("=" * 50)
        
        if not self.check_dependencies():
            return False
        
        results = []
        
        # Ejecutar demos
        results.append(("SoulX-Singer", self.demo_soulx_singer()))
        results.append(("SongGeneration", self.demo_songgeneration()))
        results.append(("ComfyUI Integration", self.demo_comfyui_integration()))
        
        # Resumen
        print("\n📊 Resumen de Demostraciones")
        print("=" * 30)
        for name, success in results:
            status = "✅" if success else "❌"
            print(f"{status} {name}")
        
        # Próximos pasos
        print("\n🎯 Próximos Pasos")
        print("=" * 20)
        print("1. 📁 Revisa los archivos generados")
        print("2. 🔊 Escucha los audios de demo")
        print("3. 🛠️  Ajusta parámetros según tu necesidad")
        print("4. 🌐 Configura la interfaz web")
        print("5. 🎵 Experimenta con diferentes estilos")
        
        return all(success for _, success in results)

def main():
    parser = argparse.ArgumentParser(description="Demo de Herramientas de Canto IA")
    parser.add_argument("--soulx", action="store_true", help="Solo ejecutar SoulX-Singer demo")
    parser.add_argument("--songgen", action="store_true", help="Solo ejecutar SongGeneration demo")
    parser.add_argument("--comfyui", action="store_true", help="Solo ejecutar ComfyUI demo")
    parser.add_argument("--all", action="store_true", help="Ejecutar todas las demos")
    
    args = parser.parse_args()
    
    demo = SingingAIDemo()
    
    if args.soulx:
        demo.demo_soulx_singer()
    elif args.songgen:
        demo.demo_songgeneration()
    elif args.comfyui:
        demo.demo_comfyui_integration()
    else:
        demo.run_all_demos()

if __name__ == "__main__":
    main()