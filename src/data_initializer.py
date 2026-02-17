"""
Inicializador de datos financieros
"""
from . import config


class DataInitializer:
    """Clase para inicializar y calcular datos financieros"""
    
    def __init__(self):
        self.presupuesto_indirectos = config.PRESUPUESTO_INDIRECTOS.copy()
        self.total_indirectos_global = sum(self.presupuesto_indirectos.values())
        self.indirectos_por_sede = {}
        self.tasas_cif_por_sede = {}
        self.salas_por_sede = config.SALAS_POR_SEDE.copy()
        self.capacidad_mensual_minutos = config.CAPACIDAD_MENSUAL_MINUTOS
        
        self._calcular_distribuciones()
    
    def _calcular_distribuciones(self):
        """Pre-calcula costos indirectos y tasas para consistencia total."""
        total_salas = sum(self.salas_por_sede.values())
        
        for sede, salas in self.salas_por_sede.items():
            factor = salas / total_salas
            costo_sede = self.total_indirectos_global * factor
            self.indirectos_por_sede[sede] = costo_sede
            capacidad_sede = salas * self.capacidad_mensual_minutos
            tasa = costo_sede / capacidad_sede
            self.tasas_cif_por_sede[sede] = tasa
