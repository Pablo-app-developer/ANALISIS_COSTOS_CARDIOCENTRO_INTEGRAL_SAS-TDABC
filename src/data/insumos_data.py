"""
Definición de insumos directos por servicio
"""

# Insumos por servicio: {servicio: [(tipo_insumo, cantidad, costo_unitario), ...]}
INSUMOS_POR_SERVICIO = {
    "Ecocardiograma Transesofágico": [
        ("Gel conductor", 1, 5000),
        ("Sonda transesofágica (uso)", 1, 80000),
        ("Material descartable", 1, 15000)
    ],
    "Estudio Electrofisiológico": [
        ("Catéter diagnóstico", 2, 450000),
        ("Electrodos", 6, 25000),
        ("Material quirúrgico", 1, 120000)
    ],
    "Cardioversión Eléctrica": [
        ("Electrodos adhesivos", 2, 35000),
        ("Medicamentos sedación", 1, 80000),
        ("Material descartable", 1, 20000)
    ],
    "Implante Marcapasos": [
        ("Marcapasos (dispositivo)", 1, 8500000),
        ("Cables de estimulación", 2, 650000),
        ("Material quirúrgico", 1, 180000),
        ("Medicamentos", 1, 120000)
    ],
    "Cateterismo Cardíaco Derecho": [
        ("Catéter Swan-Ganz", 1, 380000),
        ("Introductor", 1, 85000),
        ("Medio de contraste", 50, 1200),
        ("Material descartable", 1, 95000)
    ],
    "Cateterismo Cardíaco Izquierdo": [
        ("Catéter diagnóstico", 2, 420000),
        ("Introductor arterial", 1, 95000),
        ("Medio de contraste", 100, 1200),
        ("Material descartable", 1, 110000)
    ],
    "Angioplastia Coronaria": [
        ("Stent coronario", 1.5, 3500000),
        ("Catéter guía", 1, 580000),
        ("Balón de angioplastia", 2, 450000),
        ("Medio de contraste", 150, 1200),
        ("Medicamentos anticoagulantes", 1, 280000),
        ("Material descartable", 1, 250000)
    ],
    "Ablación por Radiofrecuencia": [
        ("Catéter de ablación", 1, 4500000),
        ("Catéteres diagnósticos", 3, 380000),
        ("Electrodos", 8, 25000),
        ("Material descartable", 1, 320000)
    ],
    "Cierre de CIA": [
        ("Dispositivo oclusor", 1, 12000000),
        ("Catéter delivery", 1, 850000),
        ("Catéter diagnóstico", 2, 380000),
        ("Medio de contraste", 80, 1200),
        ("Material descartable", 1, 280000)
    ],
    "Estudio Hemodinámico Completo": [
        ("Catéteres", 3, 420000),
        ("Introductor", 2, 85000),
        ("Medio de contraste", 120, 1200),
        ("Material descartable", 1, 150000)
    ],
    "Biopsia Endomiocárdica": [
        ("Pinza de biopsia", 1, 680000),
        ("Catéter guía", 1, 350000),
        ("Material histológico", 1, 95000),
        ("Material descartable", 1, 120000)
    ],
}
