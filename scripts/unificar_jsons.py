import json
import os
from typing import List, Dict, Any

def unificar_logos_concurso():
    """
    Unifica todos los archivos JSON del concurso de logos en un solo archivo consolidado
    con metadatos adicionales y validación de datos.
    """
    
    # Rutas de los archivos JSON (ajusta según tu estructura)
    archivos_json = [
        "ai_studio_code.txt",           # Tanda 1
        "ai_studio_code (1).txt",       # Tanda 2  
        "ai_studio_code (2).txt",       # Tanda 3
        "ai_studio_code (3).txt"        # Tanda 4
    ]
    
    logos_unificados = []
    estadisticas = {
        "total_logos": 0,
        "tandas_procesadas": 0,
        "mejor_puntuacion": 0,
        "peor_puntuacion": 100,
        "promedio_puntuacion": 0,
        "logos_por_tanda": {},
        "criterios_promedio": {
            "originalidad": 0,
            "adecuacion_marca": 0,
            "legibilidad_escalabilidad": 0,
            "impacto_visual": 0,
            "versatilidad_cromatica": 0,
            "innovacion_tecnologica": 0
        }
    }
    
    suma_total_puntuaciones = 0
    suma_criterios = {criterio: 0 for criterio in estadisticas["criterios_promedio"].keys()}
    
    for idx, archivo in enumerate(archivos_json, 1):
        if not os.path.exists(archivo):
            print(f"⚠️  Archivo no encontrado: {archivo}")
            continue
            
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                
            # Parsear JSON
            datos_tanda = json.loads(contenido)
            
            # Validar que sea una lista
            if not isinstance(datos_tanda, list):
                print(f"❌ Error: {archivo} no contiene una lista válida")
                continue
                
            # Procesar cada logo de la tanda
            logos_tanda_procesados = 0
            for logo in datos_tanda:
                # Validar estructura del logo
                if not isinstance(logo, dict) or 'logo_id' not in logo:
                    print(f"⚠️  Logo inválido encontrado en {archivo}")
                    continue
                
                # Enriquecer datos del logo
                logo_enriquecido = {
                    **logo,
                    "tanda": idx,
                    "nombre_archivo": archivo,
                    "posicion_en_tanda": logos_tanda_procesados + 1,
                    "id_global": len(logos_unificados) + 1,
                    "clasificado": True,  # Todos los logos en esta fase están clasificados
                    "fase": "Clasificatoria",
                    "fecha_evaluacion": "2025-01-01",  # Puedes ajustar esto
                    "puntuacion_normalizada": round((logo.get('total', 0) / 60) * 100, 2) if logo.get('total') else 0
                }
                
                logos_unificados.append(logo_enriquecido)
                logos_tanda_procesados += 1
                
                # Actualizar estadísticas
                puntuacion = logo.get('total', 0)
                suma_total_puntuaciones += puntuacion
                
                if puntuacion > estadisticas["mejor_puntuacion"]:
                    estadisticas["mejor_puntuacion"] = puntuacion
                if puntuacion < estadisticas["peor_puntuacion"]:
                    estadisticas["peor_puntuacion"] = puntuacion
                
                # Sumar criterios para promedio
                scores = logo.get('scores', {})
                for criterio in suma_criterios.keys():
                    suma_criterios[criterio] += scores.get(criterio, 0)
            
            estadisticas["logos_por_tanda"][f"Tanda {idx}"] = logos_tanda_procesados
            estadisticas["tandas_procesadas"] += 1
            print(f"✅ Procesada {archivo}: {logos_tanda_procesados} logos")
            
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear JSON en {archivo}: {e}")
        except Exception as e:
            print(f"❌ Error procesando {archivo}: {e}")
    
    # Calcular estadísticas finales
    estadisticas["total_logos"] = len(logos_unificados)
    if estadisticas["total_logos"] > 0:
        estadisticas["promedio_puntuacion"] = round(suma_total_puntuaciones / estadisticas["total_logos"], 2)
        
        for criterio in estadisticas["criterios_promedio"].keys():
            estadisticas["criterios_promedio"][criterio] = round(
                suma_criterios[criterio] / estadisticas["total_logos"], 2
            )
    
    # Ordenar logos por puntuación (de mayor a menor)
    logos_unificados.sort(key=lambda x: x.get('total', 0), reverse=True)
    
    # Agregar ranking
    for idx, logo in enumerate(logos_unificados, 1):
        logo["ranking_global"] = idx
    
    # Estructura final del archivo unificado
    datos_finales = {
        "metadata": {
            "concurso": "fAIcing Logo Rebranding 2025",
            "fase": "Clasificatoria - 32 Finalistas",
            "fecha_generacion": "2025-01-01",
            "version": "1.0",
            "descripcion": "Evaluación completa de 32 propuestas de logo para el rebranding de la aplicación fAIcing"
        },
        "estadisticas": estadisticas,
        "criterios_evaluacion": {
            "originalidad": "Nivel de innovación y diferenciación del diseño",
            "adecuacion_marca": "Coherencia con los valores y propósito de fAIcing",
            "legibilidad_escalabilidad": "Claridad y funcionalidad en diferentes tamaños",
            "impacto_visual": "Capacidad de generar recordación y atracción",
            "versatilidad_cromatica": "Adaptabilidad a diferentes contextos y medios",
            "innovacion_tecnologica": "Representación efectiva de la tecnología AI"
        },
        "logos": logos_unificados
    }
    
    # Guardar archivo unificado
    nombre_archivo_salida = "concurso_logos_faicing_unificado.json"
    with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(datos_finales, f, ensure_ascii=False, indent=2)
    
    # Reporte final
    print("\n" + "="*60)
    print("🎯 CONCURSO DE LOGOS fAIcing - UNIFICACIÓN COMPLETADA")
    print("="*60)
    print(f"📊 Total de logos procesados: {estadisticas['total_logos']}")
    print(f"📁 Tandas procesadas: {estadisticas['tandas_procesadas']}")
    print(f"🥇 Mejor puntuación: {estadisticas['mejor_puntuacion']}/60")
    print(f"🥉 Peor puntuación: {estadisticas['peor_puntuacion']}/60")
    print(f"📈 Puntuación promedio: {estadisticas['promedio_puntuacion']}/60")
    print(f"💾 Archivo generado: {nombre_archivo_salida}")
    
    print("\n📋 Distribución por tanda:")
    for tanda, cantidad in estadisticas["logos_por_tanda"].items():
        print(f"   {tanda}: {cantidad} logos")
    
    print("\n🎨 Promedios por criterio:")
    for criterio, promedio in estadisticas["criterios_promedio"].items():
        print(f"   {criterio.replace('_', ' ').title()}: {promedio}/10")
    
    return datos_finales

if __name__ == "__main__":
    resultado = unificar_logos_concurso()