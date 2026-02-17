"""
Generador de datos para producción.

Funciones puras que generan datos de producción sin conocer Excel.
"""
import random
from typing import List, Dict, Any


def generar_datos_produccion(
    servicios_lista: List[str],
    servicios_dict: Dict[str, Dict],
    categorias_info: Dict,
    sedes: List[str],
    aseguradoras: List[str]
) -> List[Dict[str, Any]]:
    """
    Genera datos de producción (volúmenes y facturación) para todos los servicios.
    
    Args:
        servicios_lista: Lista de nombres de servicios
        servicios_dict: Diccionario {nombre_servicio: datos_completos}
        categorias_info: Información de categorías
        sedes: Lista de sedes
        aseguradoras: Lista de aseguradoras
        
    Returns:
        Lista de diccionarios con estructura:
        {
            'codigo': str,
            'servicio': str,
            'sede': str,
            'aseguradora': str,
            'cantidad': int,
            'valor_unitario': int,
            'categoria': str
        }
    """
    datos_produccion = []
    
    for servicio in servicios_lista:
        servicio_data = servicios_dict.get(servicio, {})
        codigo = servicio_data.get("codigo", f"SV{servicios_lista.index(servicio)+1:03d}")
        categoria = servicio_data.get("categoria", "Diagnóstico No Invasivo")

        for sede in sedes:
            for aseguradora in aseguradoras:
                # Obtener rangos de volumen del servicio o default de categoría
                volumen_min = servicio_data.get("volumen_min")
                volumen_max = servicio_data.get("volumen_max")
                
                if volumen_min is None or volumen_max is None:
                    cat_info = categorias_info.get(categoria, {})
                    volumen_min = cat_info.get("volumen_min_default", 10)
                    volumen_max = cat_info.get("volumen_max_default", 30)
                
                cantidad = random.randint(volumen_min, volumen_max)

                # Obtener rangos de valor del servicio
                valor_min = servicio_data.get("valor_min", 100000)
                valor_max = servicio_data.get("valor_max", 500000)
                valor = random.randint(int(valor_min), int(valor_max))

                datos_produccion.append({
                    'codigo': codigo,
                    'servicio': servicio,
                    'sede': sede,
                    'aseguradora': aseguradora,
                    'cantidad': cantidad,
                    'valor_unitario': valor,
                    'categoria': categoria
                })
    
    return datos_produccion
