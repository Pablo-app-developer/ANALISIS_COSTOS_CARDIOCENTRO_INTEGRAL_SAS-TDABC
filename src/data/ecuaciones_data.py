"""
Definición de ecuaciones de tiempo TDABC por servicio
Cada servicio consume tiempo de diferentes grupos ocupacionales
"""

# Ecuaciones de tiempo: {servicio: [(grupo_ocupacional, minutos, factor_complejidad), ...]}
ECUACIONES_SERVICIOS = {
    "Ecocardiograma Transtorácico": [
        ("Cardiólogo Especialista", 15, 1.0),
        ("Técnico Radiólogo", 20, 1.0),
        ("Auxiliar de Enfermería", 10, 1.0)
    ],
    "Ecocardiograma Transesofágico": [
        ("Cardiólogo Especialista", 30, 1.2),
        ("Enfermero Especializado", 25, 1.0),
        ("Auxiliar de Enfermería", 15, 1.0)
    ],
    "Holter 24 Horas": [
        ("Cardiólogo General", 20, 1.0),
        ("Técnico Radiólogo", 30, 1.0),
        ("Auxiliar de Enfermería", 15, 1.0)
    ],
    "Holter 48 Horas": [
        ("Cardiólogo General", 25, 1.1),
        ("Técnico Radiólogo", 35, 1.0),
        ("Auxiliar de Enfermería", 20, 1.0)
    ],
    "Prueba de Esfuerzo": [
        ("Cardiólogo General", 30, 1.0),
        ("Enfermero Especializado", 25, 1.0),
        ("Técnico Radiólogo", 15, 1.0)
    ],
    "Electrocardiograma": [
        ("Técnico Radiólogo", 10, 1.0),
        ("Auxiliar de Enfermería", 5, 1.0)
    ],
    "MAPA 24 Horas": [
        ("Cardiólogo General", 20, 1.0),
        ("Enfermero", 25, 1.0),
        ("Auxiliar de Enfermería", 15, 1.0)
    ],
    "Ecocardiograma Doppler": [
        ("Cardiólogo Especialista", 20, 1.0),
        ("Técnico Radiólogo", 25, 1.0),
        ("Auxiliar de Enfermería", 10, 1.0)
    ],
    "Ecocardiograma de Estrés": [
        ("Cardiólogo Especialista", 35, 1.2),
        ("Enfermero Especializado", 30, 1.0),
        ("Técnico Radiólogo", 20, 1.0)
    ],
    "Tilt Test": [
        ("Cardiólogo General", 40, 1.0),
        ("Enfermero Especializado", 45, 1.0),
        ("Auxiliar de Enfermería", 20, 1.0)
    ],
    "Estudio Electrofisiológico": [
        ("Cardiólogo Especialista", 90, 1.5),
        ("Enfermero Especializado", 60, 1.2),
        ("Técnico Radiólogo", 45, 1.0)
    ],
    "Cardioversión Eléctrica": [
        ("Cardiólogo Especialista", 45, 1.3),
        ("Enfermero Especializado", 30, 1.0),
        ("Auxiliar de Enfermería", 20, 1.0)
    ],
    "Implante Marcapasos": [
        ("Cardiólogo Especialista", 120, 1.8),
        ("Enfermero Especializado", 90, 1.3),
        ("Técnico Radiólogo", 60, 1.0),
        ("Auxiliar de Enfermería", 30, 1.0)
    ],
    "Cateterismo Cardíaco Derecho": [
        ("Cardiólogo Especialista", 60, 1.4),
        ("Enfermero Especializado", 50, 1.2),
        ("Técnico Radiólogo", 40, 1.0)
    ],
    "Cateterismo Cardíaco Izquierdo": [
        ("Cardiólogo Especialista", 75, 1.5),
        ("Enfermero Especializado", 60, 1.2),
        ("Técnico Radiólogo", 45, 1.0)
    ],
    "Angioplastia Coronaria": [
        ("Cardiólogo Especialista", 150, 2.0),
        ("Cardiólogo General", 90, 1.5),
        ("Enfermero Especializado", 120, 1.3),
        ("Técnico Radiólogo", 90, 1.0)
    ],
    "Ablación por Radiofrecuencia": [
        ("Cardiólogo Especialista", 180, 2.2),
        ("Enfermero Especializado", 150, 1.5),
        ("Técnico Radiólogo", 120, 1.2)
    ],
    "Cierre de CIA": [
        ("Cardiólogo Especialista", 200, 2.5),
        ("Cardiólogo General", 120, 1.5),
        ("Enfermero Especializado", 180, 1.5),
        ("Técnico Radiólogo", 150, 1.3)
    ],
    "Estudio Hemodinámico Completo": [
        ("Cardiólogo Especialista", 100, 1.6),
        ("Enfermero Especializado", 80, 1.3),
        ("Técnico Radiólogo", 60, 1.0)
    ],
    "Biopsia Endomiocárdica": [
        ("Cardiólogo Especialista", 90, 1.7),
        ("Enfermero Especializado", 70, 1.3),
        ("Técnico Radiólogo", 50, 1.0),
        ("Auxiliar de Enfermería", 30, 1.0)
    ],
}
