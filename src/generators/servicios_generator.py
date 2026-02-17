"""
Generador de datos para servicios.

Funciones puras que generan datos de servicios sin conocer Excel.
"""
from typing import List, Dict, Any


def generar_datos_servicios(servicios_completos: List[Dict], categorias_info: Dict) -> List[Dict[str, Any]]:
    """
    Genera una lista de servicios con todos sus atributos calculados.
    
    Args:
        servicios_completos: Lista de servicios desde servicios.json
        categorias_info: Información de categorías desde servicios.json
        
    Returns:
        Lista de diccionarios con estructura:
        {
            'codigo': str,
            'nombre': str,
            'categoria': str,
            'complejidad': str,
            'requiere_insumos': bool,
            'estado': str
        }
    """
    servicios_procesados = []
    
    for servicio_data in servicios_completos:
        servicio = servicio_data.get("nombre", "")
        categoria = servicio_data.get("categoria", "")
        
        # Obtener complejidad del servicio o default de categoría
        complejidad = servicio_data.get("complejidad")
        if not complejidad:
            cat_info = categorias_info.get(categoria, {})
            complejidad = cat_info.get("complejidad_base", "Media")
        
        # Obtener requiere_insumos del servicio o default de categoría
        requiere_insumos = servicio_data.get("requiere_insumos")
        if requiere_insumos is None:
            cat_info = categorias_info.get(categoria, {})
            requiere_insumos = cat_info.get("requiere_insumos_default", False)
        
        servicios_procesados.append({
            'codigo': servicio_data.get("codigo", f"SV{len(servicios_procesados)+1:03d}"),
            'nombre': servicio,
            'categoria': categoria,
            'complejidad': complejidad,
            'requiere_insumos': requiere_insumos,
            'estado': 'Activo'
        })
    
    return servicios_procesados
