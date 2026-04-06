#!/usr/bin/env python3
"""
CONVERSOR EXCEL → JSON
Sistema de Hospedajes Centinela 2026

Convierte el Excel de actualización a formato JSON compatible con el sistema web.
Incluye categorización automática según estándares Centinela.

Uso:
    python excel_to_json_converter.py <archivo_excel.xlsx> [output.json]

Ejemplo:
    python excel_to_json_converter.py Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx hospedajes.json
"""

import pandas as pd
import json
import sys
from datetime import datetime
import re

class CategorizadorHospedajes:
    """Sistema de categorización automática según estándares Centinela"""
    
    def __init__(self):
        self.pesos = {
            'habitaciones': 25,
            'wifi': 15,
            'climatizacion': 20,
            'alimentacion': 15,
            'lavanderia': 10,
            'capacidad': 10,
            'ocupacion': 5
        }
    
    def evaluar_habitaciones(self, row):
        """Evalúa estándar de habitaciones (max 2 camas + baño privado)"""
        simples_privado = pd.to_numeric(row.get('hab_simples_privado', 0), errors='coerce') or 0
        dobles_privado = pd.to_numeric(row.get('hab_dobles_privado', 0), errors='coerce') or 0
        triples_privado = pd.to_numeric(row.get('hab_triples_privado', 0), errors='coerce') or 0
        
        compartido = pd.to_numeric(row.get('hab_simples_compartido', 0), errors='coerce') or 0
        compartido += pd.to_numeric(row.get('hab_dobles_compartido', 0), errors='coerce') or 0
        compartido += pd.to_numeric(row.get('hab_triples_compartido', 0), errors='coerce') or 0
        
        total_privado = simples_privado + dobles_privado
        total_habitaciones = total_privado + triples_privado + compartido
        
        if total_habitaciones == 0:
            return 0, "NO"
        
        # Si hay triples o compartidas, es PARCIAL
        if triples_privado > 0 or compartido > 0:
            porcentaje = (total_privado / total_habitaciones) * 100
            if porcentaje >= 70:
                return 65, "PARCIAL"
            else:
                return 30, "NO"
        
        # Solo simples y dobles con baño privado
        return 100, "SI"
    
    def evaluar(self, row):
        """Evalúa un hospedaje completo y retorna categoría"""
        
        # Evaluar habitaciones
        puntaje_hab, estado_hab = self.evaluar_habitaciones(row)
        
        # Evaluar capacidad
        camas = pd.to_numeric(row.get('camas_instaladas', 0), errors='coerce') or 0
        if camas > 100:
            puntaje_cap = 100
        elif camas > 50:
            puntaje_cap = 80
        elif camas > 20:
            puntaje_cap = 60
        elif camas > 10:
            puntaje_cap = 40
        elif camas > 0:
            puntaje_cap = 20
        else:
            puntaje_cap = 0
        
        # Evaluar disponibilidad/ocupación
        disponibles = pd.to_numeric(row.get('hab_disponibles', 0), errors='coerce') or 0
        total_hab = pd.to_numeric(row.get('habitaciones_totales', 0), errors='coerce') or 0
        
        if total_hab > 0:
            ocupacion = ((total_hab - disponibles) / total_hab) * 100
            if ocupacion > 80:
                puntaje_ocup = 100
            elif ocupacion > 60:
                puntaje_ocup = 80
            elif ocupacion > 40:
                puntaje_ocup = 60
            else:
                puntaje_ocup = 40
        else:
            puntaje_ocup = 50
        
        # Por ahora, asumimos valores estándar para WiFi, clima, alimentación, lavandería
        # Estos se pueden extraer de observaciones o agregar columnas en Excel
        puntaje_wifi = 75  # Asumido
        puntaje_clima = 75  # Asumido
        puntaje_alim = 75  # Asumido
        puntaje_lav = 50  # Asumido
        
        # Cálculo ponderado
        puntuacion_total = (
            puntaje_hab * self.pesos['habitaciones'] +
            puntaje_wifi * self.pesos['wifi'] +
            puntaje_clima * self.pesos['climatizacion'] +
            puntaje_alim * self.pesos['alimentacion'] +
            puntaje_lav * self.pesos['lavanderia'] +
            puntaje_cap * self.pesos['capacidad'] +
            puntaje_ocup * self.pesos['ocupacion']
        ) / 100
        
        # Convertir a estrellas
        if puntuacion_total >= 85:
            categoria = 5
            estado = "Cumple Estándar"
        elif puntuacion_total >= 70:
            categoria = 4
            estado = "Parcialmente Cumple"
        elif puntuacion_total >= 55:
            categoria = 3
            estado = "Parcialmente Cumple"
        elif puntuacion_total >= 40:
            categoria = 2
            estado = "No Cumple"
        else:
            categoria = 1
            estado = "No Cumple"
        
        return {
            'puntuacion': round(puntuacion_total, 1),
            'categoria': categoria,
            'estado': estado,
            'estandares': {
                'habitaciones': estado_hab,
                'wifi': 'PARCIAL',
                'climatizacion': 'PARCIAL',
                'alimentacion': 'PARCIAL',
                'lavanderia': 'PARCIAL'
            }
        }


def limpiar_texto(texto):
    """Limpia y normaliza texto"""
    if pd.isna(texto) or texto == '-':
        return ""
    return str(texto).strip()


def limpiar_telefono(telefono):
    """Normaliza número telefónico"""
    if pd.isna(telefono):
        return ""
    
    tel = str(telefono).strip()
    
    # Remover espacios, guiones, paréntesis
    tel = re.sub(r'[\s\-\(\)]', '', tel)
    
    # Si empieza con 569, agregar +
    if tel.startswith('569') and len(tel) == 11:
        tel = '+' + tel
    # Si empieza con 56, agregar +
    elif tel.startswith('56') and not tel.startswith('+'):
        tel = '+' + tel
    
    return tel


def convertir_excel_a_json(excel_path, output_path='hospedajes.json'):
    """
    Convierte el Excel de actualización a JSON estructurado
    
    Args:
        excel_path: Ruta al archivo Excel
        output_path: Ruta donde guardar el JSON (default: hospedajes.json)
    
    Returns:
        dict: Datos convertidos
    """
    
    print(f"📖 Leyendo Excel: {excel_path}")
    
    # Leer Excel
    df = pd.read_excel(excel_path, sheet_name='Actualizacion 2026')
    
    # Saltar la primera fila (headers descriptivos)
    df = df.iloc[1:].reset_index(drop=True)
    
    # Renombrar columnas a nombres útiles
    df.columns = [
        'participa',
        'nombre',
        'rut',
        'encargado',
        'email_encargado',
        'telefono_encargado',
        'dueno',
        'email_dueno',
        'telefono_dueno',
        'hab_simples_privado',
        'hab_simples_compartido',
        'hab_dobles_privado',
        'hab_dobles_compartido',
        'hab_triples_privado',
        'hab_triples_compartido',
        'habitaciones_totales',
        'observaciones',
        'camas_instaladas',
        'camas_2025',
        'dif_mgi',
        'dif_centinela',
        'camas_total_centinela',
        'empresa_contratista',
        'completamente_arrendado',
        'num_trabajadores',
        'hab_disponibles',
        'al_dia_pagos',
        'col_extra'
    ]
    
    # Filtrar solo los que participan del programa
    df = df[df['participa'].str.upper() == 'SI'].copy()
    
    print(f"✅ Encontrados {len(df)} hospedajes participantes")
    
    # Inicializar categorizador
    categorizador = CategorizadorHospedajes()
    
    # Convertir a formato JSON
    hospedajes = []
    
    for idx, row in df.iterrows():
        
        # Extraer nombre limpio (quitar numeración)
        nombre_raw = limpiar_texto(row['nombre'])
        nombre_match = re.match(r'\d+\.\s*(.+)', nombre_raw)
        nombre = nombre_match.group(1) if nombre_match else nombre_raw
        
        # Extraer dirección si está en el nombre
        direccion = ""
        if ' - ' in nombre:
            partes = nombre.split(' - ')
            nombre = partes[0].strip()
            direccion = partes[1].strip() if len(partes) > 1 else ""
        
        # Crear estructura de hospedaje
        hospedaje = {
            'id': idx + 1,
            'nombre': nombre,
            'direccion': direccion,
            'localidad': 'Sierra Gorda',
            'rut': limpiar_texto(row['rut']),
            'encargado': limpiar_texto(row['encargado']),
            'telefono': limpiar_telefono(row['telefono_encargado']),
            'email': limpiar_texto(row['email_encargado']),
            'dueno': limpiar_texto(row['dueno']),
            'telefono_dueno': limpiar_telefono(row['telefono_dueno']),
            'email_dueno': limpiar_texto(row['email_dueno']),
            
            # Capacidad
            'habitaciones': {
                'simples_privado': int(pd.to_numeric(row['hab_simples_privado'], errors='coerce') or 0),
                'simples_compartido': int(pd.to_numeric(row['hab_simples_compartido'], errors='coerce') or 0),
                'dobles_privado': int(pd.to_numeric(row['hab_dobles_privado'], errors='coerce') or 0),
                'dobles_compartido': int(pd.to_numeric(row['hab_dobles_compartido'], errors='coerce') or 0),
                'triples_privado': int(pd.to_numeric(row['hab_triples_privado'], errors='coerce') or 0),
                'triples_compartido': int(pd.to_numeric(row['hab_triples_compartido'], errors='coerce') or 0),
                'total': int(pd.to_numeric(row['habitaciones_totales'], errors='coerce') or 0)
            },
            
            'camas_instaladas': int(pd.to_numeric(row['camas_instaladas'], errors='coerce') or 0),
            'camas_disponibles': int(pd.to_numeric(row['habitaciones_totales'], errors='coerce') or 0) - \
                                int(pd.to_numeric(row['hab_disponibles'], errors='coerce') or 0),
            'habitaciones_disponibles': int(pd.to_numeric(row['hab_disponibles'], errors='coerce') or 0),
            
            # Empresas y ocupación
            'empresas_alojadas': [limpiar_texto(row['empresa_contratista'])] if limpiar_texto(row['empresa_contratista']) else [],
            'num_trabajadores': int(pd.to_numeric(row['num_trabajadores'], errors='coerce') or 0),
            'completamente_arrendado': str(row['completamente_arrendado']).upper() == 'SI',
            
            # Pagos
            'al_dia_pagos': str(row['al_dia_pagos']).upper() == 'SI',
            
            # Observaciones
            'observaciones': limpiar_texto(row['observaciones']),
            
            # Servicios - valores por defecto
            'servicios': [],
            
            # Fecha
            'fecha_actualizacion': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Evaluar categoría
        evaluacion = categorizador.evaluar({
            'hab_simples_privado': hospedaje['habitaciones']['simples_privado'],
            'hab_simples_compartido': hospedaje['habitaciones']['simples_compartido'],
            'hab_dobles_privado': hospedaje['habitaciones']['dobles_privado'],
            'hab_dobles_compartido': hospedaje['habitaciones']['dobles_compartido'],
            'hab_triples_privado': hospedaje['habitaciones']['triples_privado'],
            'hab_triples_compartido': hospedaje['habitaciones']['triples_compartido'],
            'camas_instaladas': hospedaje['camas_instaladas'],
            'habitaciones_totales': hospedaje['habitaciones']['total'],
            'hab_disponibles': hospedaje['habitaciones_disponibles']
        })
        
        hospedaje['categoria'] = evaluacion['categoria']
        hospedaje['rating'] = evaluacion['categoria']
        hospedaje['puntuacion'] = evaluacion['puntuacion']
        hospedaje['estado'] = evaluacion['estado']
        hospedaje['estandares'] = evaluacion['estandares']
        
        hospedajes.append(hospedaje)
    
    # Crear estructura completa JSON
    data = {
        'hospedajes': hospedajes,
        'categorias': [
            {
                'id': 1,
                'estrellas': 1,
                'nombre': 'Básico',
                'descripcion': 'Servicios mínimos, requiere mejoras significativas',
                'requisitos_minimos': ['Habitaciones']
            },
            {
                'id': 2,
                'estrellas': 2,
                'nombre': 'Aceptable',
                'descripcion': 'Servicios básicos, algunas mejoras necesarias',
                'requisitos_minimos': ['Habitaciones', 'Algún servicio']
            },
            {
                'id': 3,
                'estrellas': 3,
                'nombre': 'Bueno',
                'descripcion': 'La mayoría de estándares cumplidos',
                'requisitos_minimos': ['Habitaciones', 'WiFi o Climatización', 'Alimentación']
            },
            {
                'id': 4,
                'estrellas': 4,
                'nombre': 'Muy Bueno',
                'descripcion': 'Casi todos los estándares cumplidos',
                'requisitos_minimos': ['Habitaciones', 'WiFi', 'Climatización', 'Alimentación']
            },
            {
                'id': 5,
                'estrellas': 5,
                'nombre': 'Premium',
                'descripcion': 'Cumple con todos los estándares Centinela',
                'requisitos_minimos': ['Habitaciones', 'WiFi', 'Climatización', 'Alimentación', 'Lavandería']
            }
        ],
        'estandares': [
            {
                'id': 1,
                'nombre': 'Habitaciones',
                'descripcion': 'Máximo 2 camas por habitación con baño privado',
                'criticidad': 'ALTA'
            },
            {
                'id': 2,
                'nombre': 'WiFi',
                'descripcion': 'WiFi de buena señal disponible en todas las habitaciones',
                'criticidad': 'MEDIA'
            },
            {
                'id': 3,
                'nombre': 'Climatización',
                'descripcion': 'Sistema de aire acondicionado en habitaciones',
                'criticidad': 'ALTA'
            },
            {
                'id': 4,
                'nombre': 'Alimentación',
                'descripcion': 'Desayuno, cena o colaciones disponibles',
                'criticidad': 'MEDIA'
            },
            {
                'id': 5,
                'nombre': 'Lavandería',
                'descripcion': 'Sistema de lavandería propio o con proveedores locales',
                'criticidad': 'BAJA'
            }
        ],
        'estados': [
            {
                'id': 1,
                'nombre': 'Cumple Estándar',
                'color': '#C8E6C9',
                'descripcion': 'Hospedaje cumple con todos o casi todos los estándares'
            },
            {
                'id': 2,
                'nombre': 'Parcialmente Cumple',
                'color': '#FFF9C4',
                'descripcion': 'Hospedaje cumple con algunos estándares, requiere mejoras'
            },
            {
                'id': 3,
                'nombre': 'No Cumple',
                'color': '#FFCDD2',
                'descripcion': 'Hospedaje no cumple con la mayoría de estándares'
            }
        ],
        'metadata': {
            'version': '2.0',
            'ultima_actualizacion': datetime.now().strftime('%Y-%m-%d'),
            'total_hospedajes': len(hospedajes),
            'total_camas': sum(h['camas_instaladas'] for h in hospedajes),
            'total_disponibles': sum(h['habitaciones_disponibles'] for h in hospedajes),
            'fuente': excel_path
        }
    }
    
    # Guardar JSON
    print(f"💾 Guardando JSON: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    print(f"\n{'='*60}")
    print(f"✅ CONVERSIÓN EXITOSA")
    print(f"{'='*60}")
    print(f"Total hospedajes: {len(hospedajes)}")
    print(f"Total camas instaladas: {data['metadata']['total_camas']}")
    print(f"Total habitaciones disponibles: {data['metadata']['total_disponibles']}")
    print(f"\nDistribución por categoría:")
    for i in range(1, 6):
        count = len([h for h in hospedajes if h['categoria'] == i])
        print(f"  {'⭐' * i} ({i} estrellas): {count} hospedajes")
    
    print(f"\nDistribución por estado:")
    for estado in set(h['estado'] for h in hospedajes):
        count = len([h for h in hospedajes if h['estado'] == estado])
        print(f"  {estado}: {count} hospedajes")
    
    print(f"\n📄 Archivo generado: {output_path}")
    print(f"{'='*60}\n")
    
    return data


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python excel_to_json_converter.py <archivo_excel.xlsx> [output.json]")
        print("\nEjemplo:")
        print("  python excel_to_json_converter.py Actualizacion_Establecimientos_Sierra_Gorda_2026_V84.xlsx hospedajes.json")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'hospedajes.json'
    
    try:
        convertir_excel_a_json(excel_file, output_file)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
