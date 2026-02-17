"""
Gestor de parámetros TDABC configurables.

Permite configurar parámetros fundamentales del modelo sin modificar código.
"""
import json
from pathlib import Path
from typing import Dict, Any, List


class GestorParametrosTDABC:
    """
    Gestiona parámetros configurables del modelo TDABC.
    """
    
    def __init__(self, ruta_config: str = None):
        """
        Inicializa el gestor de parámetros.
        
        Args:
            ruta_config: Ruta al archivo de configuración JSON
        """
        if ruta_config is None:
            # Ruta por defecto
            base_dir = Path(__file__).parent
            ruta_config = base_dir / "config" / "parametros_tdabc.json"
        
        self.ruta_config = Path(ruta_config)
        self.parametros = self._cargar_parametros()
    
    def _cargar_parametros(self) -> Dict[str, Any]:
        """Carga parámetros desde el archivo JSON"""
        try:
            with open(self.ruta_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('parametros_tdabc', {})
        except FileNotFoundError:
            print(f"[WARN] No se encontró {self.ruta_config}, usando valores por defecto")
            return self._parametros_por_defecto()
        except Exception as e:
            print(f"[ERROR] Error al cargar parámetros: {e}")
            return self._parametros_por_defecto()
    
    def _parametros_por_defecto(self) -> Dict[str, Any]:
        """Retorna parámetros por defecto si no hay archivo de configuración"""
        return {
            "tiempo_trabajo": {
                "horas_mes": 184,
                "dias_laborales_mes": 23,
                "horas_dia": 8,
                "minutos_mes": 11040
            },
            "formatos_moneda": {
                "simbolo": "$",
                "formato_excel": "$#,##0"
            },
            "tasas_prestaciones": {
                "total_prestaciones": 0.5205
            }
        }
    
    def guardar_parametros(self):
        """Guarda los parámetros actuales al archivo JSON"""
        try:
            config = {"parametros_tdabc": self.parametros}
            with open(self.ruta_config, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"[OK] Parámetros guardados en {self.ruta_config}")
            return True
        except Exception as e:
            print(f"[ERROR] Error al guardar parámetros: {e}")
            return False
    
    # === TIEMPO DE TRABAJO ===
    
    def get_horas_mes(self) -> int:
        """Obtiene horas laborales por mes"""
        return self.parametros.get('tiempo_trabajo', {}).get('horas_mes', 184)
    
    def set_horas_mes(self, horas: int):
        """Configura horas laborales por mes"""
        if 'tiempo_trabajo' not in self.parametros:
            self.parametros['tiempo_trabajo'] = {}
        self.parametros['tiempo_trabajo']['horas_mes'] = horas
        self.parametros['tiempo_trabajo']['minutos_mes'] = horas * 60
    
    def get_minutos_mes(self) -> int:
        """Obtiene minutos laborales por mes"""
        return self.parametros.get('tiempo_trabajo', {}).get('minutos_mes', 11040)
    
    # === FORMATOS ===
    
    def get_formato_moneda(self) -> str:
        """Obtiene formato de moneda para Excel"""
        return self.parametros.get('formatos_moneda', {}).get('formato_excel', '$#,##0')
    
    def get_simbolo_moneda(self) -> str:
        """Obtiene símbolo de moneda"""
        return self.parametros.get('formatos_moneda', {}).get('simbolo', '$')
    
    def get_formato_porcentaje(self) -> str:
        """Obtiene formato de porcentaje para Excel"""
        return self.parametros.get('formatos_porcentaje', {}).get('formato_excel', '0.00%')
    
    # === PRESTACIONES SOCIALES ===
    
    def get_tasa_prestaciones(self) -> float:
        """Obtiene tasa total de prestaciones sociales"""
        return self.parametros.get('tasas_prestaciones', {}).get('total_prestaciones', 0.5205)
    
    def get_tasas_prestaciones_detalle(self) -> Dict[str, float]:
        """Obtiene detalle de todas las tasas de prestaciones"""
        return self.parametros.get('tasas_prestaciones', {})
    
    def set_tasa_prestaciones(self, tasa: float):
        """Configura tasa total de prestaciones"""
        if 'tasas_prestaciones' not in self.parametros:
            self.parametros['tasas_prestaciones'] = {}
        self.parametros['tasas_prestaciones']['total_prestaciones'] = tasa
    
    # === CONFIGURACIÓN DE HOJAS ===
    
    def get_hojas_activas(self) -> List[Dict[str, Any]]:
        """Obtiene lista de hojas activas del modelo"""
        config_hojas = self.parametros.get('configuracion_hojas', {})
        hojas = config_hojas.get('hojas_activas', [])
        return [h for h in hojas if h.get('activa', True)]
    
    def get_hojas_ordenadas(self) -> List[str]:
        """Obtiene nombres de hojas en orden"""
        hojas = self.get_hojas_activas()
        hojas_ordenadas = sorted(hojas, key=lambda x: x.get('orden', 999))
        return [h['nombre'] for h in hojas_ordenadas]
    
    def activar_hoja(self, nombre_hoja: str):
        """Activa una hoja específica"""
        config_hojas = self.parametros.get('configuracion_hojas', {})
        hojas = config_hojas.get('hojas_activas', [])
        
        for hoja in hojas:
            if hoja['nombre'] == nombre_hoja:
                hoja['activa'] = True
                return True
        return False
    
    def desactivar_hoja(self, nombre_hoja: str):
        """Desactiva una hoja específica"""
        config_hojas = self.parametros.get('configuracion_hojas', {})
        hojas = config_hojas.get('hojas_activas', [])
        
        for hoja in hojas:
            if hoja['nombre'] == nombre_hoja:
                hoja['activa'] = False
                return True
        return False
    
    def agregar_hoja(self, nombre: str, descripcion: str, orden: int = None):
        """Agrega una nueva hoja al modelo"""
        if 'configuracion_hojas' not in self.parametros:
            self.parametros['configuracion_hojas'] = {'hojas_activas': []}
        
        hojas = self.parametros['configuracion_hojas']['hojas_activas']
        
        # Verificar si ya existe
        if any(h['nombre'] == nombre for h in hojas):
            print(f"[WARN] La hoja '{nombre}' ya existe")
            return False
        
        # Determinar orden
        if orden is None:
            orden = len(hojas) + 1
        
        # Agregar hoja
        nueva_hoja = {
            'nombre': nombre,
            'activa': True,
            'orden': orden,
            'descripcion': descripcion
        }
        hojas.append(nueva_hoja)
        return True
    
    # === ESTILOS ===
    
    def get_fuente_base(self) -> str:
        """Obtiene fuente base para Excel"""
        return self.parametros.get('estilos_excel', {}).get('fuente_base', 'Calibri')
    
    def get_color_header(self) -> str:
        """Obtiene color de encabezados"""
        return self.parametros.get('estilos_excel', {}).get('color_header', '4472C4')
    
    # === VALIDACIONES ===
    
    def get_validaciones(self) -> Dict[str, Any]:
        """Obtiene rangos de validación"""
        return self.parametros.get('validaciones', {})
    
    # === UTILIDADES ===
    
    def obtener_resumen(self) -> str:
        """Genera un resumen de la configuración actual"""
        resumen = []
        resumen.append("=" * 60)
        resumen.append("CONFIGURACIÓN ACTUAL DEL MODELO TDABC")
        resumen.append("=" * 60)
        
        # Tiempo de trabajo
        resumen.append(f"\n[TIEMPO DE TRABAJO]")
        resumen.append(f"  Horas/mes: {self.get_horas_mes()}h")
        resumen.append(f"  Minutos/mes: {self.get_minutos_mes()} min")
        
        # Formatos
        resumen.append(f"\n[FORMATOS]")
        resumen.append(f"  Moneda: {self.get_simbolo_moneda()}")
        resumen.append(f"  Formato Excel: {self.get_formato_moneda()}")
        
        # Prestaciones
        resumen.append(f"\n[PRESTACIONES SOCIALES]")
        resumen.append(f"  Tasa total: {self.get_tasa_prestaciones()*100:.2f}%")
        
        # Hojas activas
        resumen.append(f"\n[HOJAS ACTIVAS]")
        hojas = self.get_hojas_activas()
        resumen.append(f"  Total: {len(hojas)} hojas")
        for hoja in hojas[:5]:  # Mostrar primeras 5
            resumen.append(f"  - {hoja['nombre']}: {hoja['descripcion']}")
        if len(hojas) > 5:
            resumen.append(f"  ... y {len(hojas) - 5} más")
        
        resumen.append("=" * 60)
        return "\n".join(resumen)


# Instancia global para uso en todo el sistema
_gestor_global = None

def get_gestor_parametros() -> GestorParametrosTDABC:
    """
    Obtiene la instancia global del gestor de parámetros.
    
    Returns:
        Instancia del gestor de parámetros
    """
    global _gestor_global
    if _gestor_global is None:
        _gestor_global = GestorParametrosTDABC()
    return _gestor_global


def ejemplo_uso():
    """Ejemplo de uso del gestor de parámetros"""
    print("\n" + "="*60)
    print("EJEMPLO: Configurar Parámetros TDABC")
    print("="*60 + "\n")
    
    # Obtener gestor
    gestor = get_gestor_parametros()
    
    # Mostrar configuración actual
    print(gestor.obtener_resumen())
    
    print("\n" + "="*60)
    print("MODIFICAR PARÁMETROS:")
    print("="*60)
    
    print("\n# Cambiar horas laborales por mes:")
    print("gestor.set_horas_mes(176)  # 22 días x 8 horas")
    
    print("\n# Cambiar tasa de prestaciones:")
    print("gestor.set_tasa_prestaciones(0.55)  # 55%")
    
    print("\n# Desactivar una hoja:")
    print("gestor.desactivar_hoja('ANALISIS_RENTABILIDAD')")
    
    print("\n# Agregar una hoja personalizada:")
    print("gestor.agregar_hoja('MI_HOJA', 'Análisis personalizado', orden=12)")
    
    print("\n# Guardar cambios:")
    print("gestor.guardar_parametros()")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    ejemplo_uso()
