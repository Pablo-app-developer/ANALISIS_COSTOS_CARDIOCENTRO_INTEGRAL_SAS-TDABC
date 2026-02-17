"""
Clase principal del Modelo TDABC
"""
from openpyxl import Workbook
from .data_initializer import DataInitializer
from .sheets import (
    parametros, nomina, capacidad, costo_por_minuto,
    servicios, ecuaciones_tiempo, insumos, produccion,
    costos_indirectos, costeo_servicios, resumen_ejecutivo
)


class ModeloTDABC:
    """Generador del Modelo TDABC para CardioCentro Diagnóstico Integral S.A.S."""
    
    def __init__(self):
        self.wb = Workbook()
        self.wb.remove(self.wb.active)  # Remover hoja por defecto
        self.data_init = DataInitializer()
    
    def generar_archivo(self, nombre_archivo="Modelo_TDABC_CardioCentro.xlsx"):
        """Genera el archivo Excel completo"""
        print("Iniciando generación del modelo TDABC...")
        print("="*60)
        
        # Crear todas las hojas en orden
        print("[OK] Creando hoja PARAMETROS...")
        parametros.crear_hoja_parametros(self.wb)
        
        print("[OK] Creando hoja NOMINA...")
        nomina.crear_hoja_nomina(self.wb)
        
        print("[OK] Creando hoja CAPACIDAD...")
        capacidad.crear_hoja_capacidad(self.wb)
        
        print("[OK] Creando hoja COSTO_POR_MINUTO...")
        costo_por_minuto.crear_hoja_costo_por_minuto(self.wb)
        
        print("[OK] Creando hoja SERVICIOS...")
        servicios.crear_hoja_servicios(self.wb)
        
        print("[OK] Creando hoja ECUACIONES_TIEMPO...")
        ecuaciones_tiempo.crear_hoja_ecuaciones_tiempo(self.wb)
        
        print("[OK] Creando hoja INSUMOS...")
        insumos.crear_hoja_insumos(self.wb)
        
        print("[OK] Creando hoja PRODUCCION...")
        produccion.crear_hoja_produccion(self.wb)
        
        print("[OK] Creando hoja COSTEO_SERVICIOS...")
        costeo_servicios.crear_hoja_costeo_servicios(self.wb, self.data_init)
        
        print("[OK] Creando hoja COSTOS_INDIRECTOS...")
        costos_indirectos.crear_hoja_costos_indirectos(self.wb, self.data_init)
        
        print("[OK] Creando hoja RESUMEN_EJECUTIVO...")
        resumen_ejecutivo.crear_hoja_resumen_ejecutivo(self.wb)
        
        print("="*60)
        print(f"Guardando archivo {nombre_archivo}...")
        self.wb.save(nombre_archivo)
        print(f"[SUCCESS] Archivo generado exitosamente: {nombre_archivo}")
        print("="*60)
        print("\nESTRUCTURA DEL MODELO:")
        print("  1. PARAMETROS - Configuración general")
        print("  2. NOMINA - Estructura salarial")
        print("  3. CAPACIDAD - Capacidad práctica (184h/mes)")
        print("  4. COSTO_POR_MINUTO - Núcleo TDABC")
        print("  5. SERVICIOS - Catálogo de servicios")
        print("  6. ECUACIONES_TIEMPO - Ecuaciones TDABC por servicio")
        print("  7. INSUMOS - Costos de materiales")
        print("  8. COSTOS_INDIRECTOS - Costos administrativos")
        print("  9. PRODUCCION - Volúmenes y facturación")
        print(" 10. COSTEO_SERVICIOS - Costo total por servicio")
        print(" 11. RESUMEN_EJECUTIVO - Dashboard de rentabilidad")
        print("="*60)
