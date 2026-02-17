"""
Configuración y constantes del Modelo TDABC
Ahora carga desde archivos JSON con fallback a valores hardcodeados
"""
from .mapper import get_mapper

# Colores corporativos (Azul médico y Gris) - NO parametrizables
COLOR_HEADER = "003366"  # Azul oscuro
COLOR_SUBHEADER = "4472C4"  # Azul medio
COLOR_TEXT = "000000"
COLOR_BG_HEADER = "D9E1F2"  # Azul claro fondo
COLOR_INPUT = "E2EFDA"   # Verde claro para inputs
COLOR_CALCULO = "F2F2F2" # Gris para cálculos
COLOR_RESULTADO = "DDEBF7" # Azul muy claro resultados
FUENTE_BASE = "Arial Narrow" # Fuente solicitada

# ========== CARGAR CONFIGURACIÓN DESDE JSON ==========
_mapper = get_mapper()

# ========== VALORES HARDCODEADOS (FALLBACK) ==========
# Estos valores se usan SOLO si no existen los archivos JSON

_SEDES_DEFAULT = ["Sede Norte - Bogotá", "Sede Sur - Medellín", "Sede Centro - Cali"]
_ASEGURADORAS_DEFAULT = ["SURA", "Sanitas", "Compensar", "Salud Total", "Nueva EPS"]

_SERVICIOS_DEFAULT = [
    "Ecocardiograma Transtorácico", "Ecocardiograma Transesofágico",
    "Holter 24 Horas", "Holter 48 Horas", "Prueba de Esfuerzo",
    "Electrocardiograma", "MAPA 24 Horas", "Ecocardiograma Doppler",
    "Ecocardiograma de Estrés", "Tilt Test",
    "Estudio Electrofisiológico", "Cardioversión Eléctrica",
    "Implante Marcapasos", "Cateterismo Cardíaco Derecho",
    "Cateterismo Cardíaco Izquierdo", "Angioplastia Coronaria",
    "Ablación por Radiofrecuencia", "Cierre de CIA",
    "Estudio Hemodinámico Completo", "Biopsia Endomiocárdica"
]

_GRUPOS_OCUPACIONALES_DEFAULT = [
    ("Cardiólogo Especialista", 12000000),
    ("Cardiólogo General", 8000000),
    ("Médico General", 5000000),
    ("Enfermero Especializado", 3500000),
    ("Enfermero", 2800000),
    ("Técnico Radiólogo", 2500000),
    ("Auxiliar de Enfermería", 1800000),
]

_PRESUPUESTO_INDIRECTOS_DEFAULT = {
    "7305 - Arrendamiento": 150000000,
    "7310 - Depreciación Equipos": 85000000,
    "7315 - Mantenimiento": 45000000,
    "7320 - Servicios Públicos": 35000000,
    "7325 - Seguros": 28000000,
    "7330 - Aseo y Limpieza": 18000000,
    "7335 - Vigilancia": 22000000,
    "7340 - Papelería": 5000000,
    "7390 - Otros": 15000000
}

_SALAS_POR_SEDE_DEFAULT = {
    "Sede Norte - Bogotá": 4,
    "Sede Sur - Medellín": 3,
    "Sede Centro - Cali": 2
}

_CATEGORIAS_SERVICIOS_DEFAULT = {
    "Ecocardiograma Transtorácico": "Diagnóstico No Invasivo",
    "Ecocardiograma Transesofágico": "Diagnóstico Invasivo",
    "Holter 24 Horas": "Diagnóstico No Invasivo",
    "Holter 48 Horas": "Diagnóstico No Invasivo",
    "Prueba de Esfuerzo": "Diagnóstico Funcional",
    "Electrocardiograma": "Diagnóstico No Invasivo",
    "MAPA 24 Horas": "Diagnóstico No Invasivo",
    "Ecocardiograma Doppler": "Diagnóstico No Invasivo",
    "Ecocardiograma de Estrés": "Diagnóstico Funcional",
    "Tilt Test": "Diagnóstico Funcional",
    "Estudio Electrofisiológico": "Diagnóstico Invasivo",
    "Cardioversión Eléctrica": "Terapéutico",
    "Implante Marcapasos": "Terapéutico",
    "Cateterismo Cardíaco Derecho": "Diagnóstico Invasivo",
    "Cateterismo Cardíaco Izquierdo": "Diagnóstico Invasivo",
    "Angioplastia Coronaria": "Terapéutico",
    "Ablación por Radiofrecuencia": "Terapéutico",
    "Cierre de CIA": "Terapéutico",
    "Estudio Hemodinámico Completo": "Diagnóstico Invasivo",
    "Biopsia Endomiocárdica": "Diagnóstico Invasivo",
}

_CATEGORIAS_DEFAULT = {
    "Diagnóstico No Invasivo": [
        "Ecocardiograma Transtorácico", "Holter 24 Horas",
        "Holter 48 Horas", "Electrocardiograma",
        "MAPA 24 Horas", "Ecocardiograma Doppler"
    ],
    "Diagnóstico Funcional": [
        "Prueba de Esfuerzo", "Ecocardiograma de Estrés",
        "Tilt Test"
    ],
    "Diagnóstico Invasivo": [
        "Ecocardiograma Transesofágico", "Estudio Electrofisiológico",
        "Cateterismo Cardíaco Derecho", "Cateterismo Cardíaco Izquierdo",
        "Estudio Hemodinámico Completo", "Biopsia Endomiocárdica"
    ],
    "Terapéutico": [
        "Cardioversión Eléctrica", "Implante Marcapasos",
        "Angioplastia Coronaria", "Ablación por Radiofrecuencia",
        "Cierre de CIA"
    ]
}

_VALORES_FACTURACION_DEFAULT = {
    "Diagnóstico No Invasivo": (120000, 350000),
    "Diagnóstico Funcional": (250000, 550000),
    "Diagnóstico Invasivo": (1500000, 3500000),
    "Terapéutico": (5500000, 35000000)
}

# ========== VALORES PÚBLICOS (CON FALLBACK) ==========
# Estos son los que usa el resto del código

# Sedes/Centros de Costo
SEDES = _mapper.get_centros_lista() or _SEDES_DEFAULT
ASEGURADORAS = _mapper.get_aseguradoras() or _ASEGURADORAS_DEFAULT

# Servicios
SERVICIOS = _mapper.get_servicios_lista() or _SERVICIOS_DEFAULT
CATEGORIAS_SERVICIOS = _mapper.get_categorias_servicios() or _CATEGORIAS_SERVICIOS_DEFAULT
VALORES_FACTURACION = _mapper.get_valores_facturacion() or _VALORES_FACTURACION_DEFAULT

# Construir CATEGORIAS desde servicios cargados
_categorias_from_json = {}
if _mapper.servicios:
    for servicio in _mapper.get_servicios_completos() or []:
        cat = servicio["categoria"]
        if cat not in _categorias_from_json:
            _categorias_from_json[cat] = []
        _categorias_from_json[cat].append(servicio["nombre"])
CATEGORIAS = _categorias_from_json if _categorias_from_json else _CATEGORIAS_DEFAULT

# Grupos Ocupacionales
GRUPOS_OCUPACIONALES = _mapper.get_grupos_ocupacionales_lista() or _GRUPOS_OCUPACIONALES_DEFAULT

# Plan Contable
PRESUPUESTO_INDIRECTOS = _mapper.get_presupuesto_indirectos_dict() or _PRESUPUESTO_INDIRECTOS_DEFAULT

# Salas por Sede
SALAS_POR_SEDE = _mapper.get_salas_por_centro() or _SALAS_POR_SEDE_DEFAULT

# Capacidad mensual en minutos (por sala)
# 176 horas al mes (Estándar Colombia)
CAPACIDAD_MENSUAL_MINUTOS = 10560

# Nombre de empresa (NUEVO - antes estaba hardcodeado en sheets)
NOMBRE_EMPRESA = _mapper.get_nombre_empresa() or "CardioCentro Diagnóstico Integral S.A.S."
