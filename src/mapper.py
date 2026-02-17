"""
Módulo de mapeo para cargar configuraciones externas
Permite adaptar el sistema TDABC a diferentes empresas del sector salud
"""
import json
from pathlib import Path
import warnings


class ConfigMapper:
    """Carga y gestiona configuraciones desde archivos JSON"""
    
    def __init__(self, config_dir="config"):
        """
        Inicializa el mapper
        
        Args:
            config_dir: Directorio donde están los archivos JSON de configuración
        """
        self.config_dir = Path(__file__).parent / config_dir
        self.empresa = None
        self.servicios = None
        self.centros_costo = None
        self.plan_contable = None
        self.grupos_ocupacionales = None
        self.mapeo_columnas = None
        self._loaded = False
        
    def cargar_configuracion(self):
        """Carga todas las configuraciones desde archivos JSON"""
        if self._loaded:
            return  # Ya cargado, no recargar
            
        self.empresa = self._cargar_json("empresa_config.json")
        self.servicios = self._cargar_json("servicios.json")
        self.centros_costo = self._cargar_json("centros_costo.json")
        self.plan_contable = self._cargar_json("plan_contable.json")
        self.grupos_ocupacionales = self._cargar_json("grupos_ocupacionales.json")
        self.mapeo_columnas = self._cargar_json("mapeo_columnas.json")
        self._loaded = True
        
    def _cargar_json(self, filename):
        """
        Carga un archivo JSON con manejo de errores
        
        Args:
            filename: Nombre del archivo JSON a cargar
            
        Returns:
            dict: Contenido del JSON o None si hay error
        """
        filepath = self.config_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            warnings.warn(
                f"⚠️ WARNING: {filename} no encontrado en {self.config_dir}. "
                f"Usando valores por defecto hardcodeados.",
                UserWarning
            )
            return None
        except json.JSONDecodeError as e:
            warnings.warn(
                f"❌ ERROR: {filename} tiene formato JSON inválido: {e}. "
                f"Usando valores por defecto hardcodeados.",
                UserWarning
            )
            return None
        except Exception as e:
            warnings.warn(
                f"❌ ERROR inesperado al cargar {filename}: {e}. "
                f"Usando valores por defecto hardcodeados.",
                UserWarning
            )
            return None

    def aplicar_mapeo(self, datos_originales, tipo_datos):
        """
        Convierte un diccionario de datos originales a un dataframe estándar interno (df_std)
        basado en el mapeo de columnas configurado.
        
        Args:
            datos_originales (dict/list): Los datos recibidos (ej: una fila o lista de filas)
            tipo_datos (str): El tipo de datos ('nomina', 'contabilidad', 'produccion', 'servicios')
            
        Returns:
            dict/list: Datos con las llaves estándar internas
        """
        if not self.mapeo_columnas or tipo_datos not in self.mapeo_columnas:
            return datos_originales
            
        mapeo = self.mapeo_columnas[tipo_datos]
        # Invertir mapeo para buscar por columna original
        # mapeo_inv = {valor: llave_estandar for llave_estandar, valor in mapeo.items()}
        
        def procesar_fila(fila):
            fila_std = {}
            for llave_std, columna_original in mapeo.items():
                if columna_original in fila:
                    fila_std[llave_std] = fila[columna_original]
                else:
                    # Fallback si no encuentra la columna (warning preventivo)
                    # print(f"⚠️ Columna '{columna_original}' no encontrada para '{llave_std}'")
                    fila_std[llave_std] = None
            return fila_std

        if isinstance(datos_originales, list):
            return [procesar_fila(f) for f in datos_originales]
        return procesar_fila(datos_originales)

    # ========== MÉTODOS DE ACCESO A COLUMNAS ==========
    
    def get_columnas_estandar(self, tipo_datos):
        """Obtiene el mapeo de columnas para un tipo de datos"""
        if self.mapeo_columnas:
            return self.mapeo_columnas.get(tipo_datos, {})
        return {}
    
    # ... (resto de métodos existentes)
    
    def get_nombre_empresa(self):
        """Obtiene nombre de empresa o valor por defecto"""
        if self.empresa:
            return self.empresa.get("nombre_empresa", "Empresa Sin Nombre")
        return None
    
    def get_sector(self):
        """Obtiene sector de la empresa"""
        if self.empresa:
            return self.empresa.get("sector", "salud")
        return None
    
    def get_pais(self):
        """Obtiene país de la empresa"""
        if self.empresa:
            return self.empresa.get("pais", "Colombia")
        return None
    
    def get_parametros_laborales(self):
        """Obtiene todos los parámetros laborales"""
        if self.empresa:
            return self.empresa.get("parametros_laborales", {})
        return None
    
    # ========== MÉTODOS DE ACCESO A SERVICIOS ==========
    
    def get_servicios_lista(self):
        """Obtiene lista de nombres de servicios"""
        if self.servicios and "servicios" in self.servicios:
            return [s["nombre"] for s in self.servicios["servicios"]]
        return None
    
    def get_servicios_completos(self):
        """Obtiene lista completa de servicios con todos sus datos"""
        if self.servicios and "servicios" in self.servicios:
            return self.servicios["servicios"]
        return None
    
    def get_categorias_servicios(self):
        """Obtiene diccionario de servicio → categoría"""
        if self.servicios and "servicios" in self.servicios:
            return {s["nombre"]: s["categoria"] for s in self.servicios["servicios"]}
        return None
    
    def get_valores_facturacion(self):
        """Obtiene diccionario de categoría → (min, max)"""
        if self.servicios and "servicios" in self.servicios:
            valores = {}
            for servicio in self.servicios["servicios"]:
                cat = servicio["categoria"]
                if cat not in valores:
                    valores[cat] = (servicio["valor_min"], servicio["valor_max"])
            return valores
        return None
    
    def get_categorias_info(self):
        """Obtiene información de categorías"""
        if self.servicios and "categorias" in self.servicios:
            return self.servicios["categorias"]
        return None
    
    # ========== MÉTODOS DE ACCESO A CENTROS DE COSTO ==========
    
    def get_centros_lista(self):
        """Obtiene lista de nombres de centros de costo/sedes"""
        if self.centros_costo and "centros" in self.centros_costo:
            return [c["nombre"] for c in self.centros_costo["centros"]]
        return None
    
    def get_centros_completos(self):
        """Obtiene lista completa de centros con todos sus datos"""
        if self.centros_costo and "centros" in self.centros_costo:
            return self.centros_costo["centros"]
        return None
    
    def get_salas_por_centro(self):
        """Obtiene diccionario de centro → número de salas"""
        if self.centros_costo and "centros" in self.centros_costo:
            return {c["nombre"]: c["salas"] for c in self.centros_costo["centros"]}
        return None
    
    def get_aseguradoras(self):
        """Obtiene lista de aseguradoras/clientes"""
        if self.centros_costo and "aseguradoras" in self.centros_costo:
            return self.centros_costo["aseguradoras"]
        return None
    
    def get_tipo_centro(self):
        """Obtiene el tipo de centro (sedes, plantas, oficinas, etc.)"""
        if self.centros_costo:
            return self.centros_costo.get("tipo", "sedes")
        return None
    
    # ========== MÉTODOS DE ACCESO A PLAN CONTABLE ==========
    
    def get_sistema_contable(self):
        """Obtiene el sistema contable usado"""
        if self.plan_contable:
            return self.plan_contable.get("sistema", "PUC_Colombia")
        return None
    
    def get_cuenta_materia_prima(self):
        """Obtiene código de cuenta de materia prima"""
        if self.plan_contable and "cuentas_directas" in self.plan_contable:
            return self.plan_contable["cuentas_directas"].get("materia_prima", {})
        return None
    
    def get_cuenta_mano_obra(self):
        """Obtiene código de cuenta de mano de obra directa"""
        if self.plan_contable and "cuentas_directas" in self.plan_contable:
            return self.plan_contable["cuentas_directas"].get("mano_obra_directa", {})
        return None
    
    def get_costos_indirectos(self):
        """Obtiene lista de costos indirectos"""
        if self.plan_contable and "costos_indirectos" in self.plan_contable:
            return self.plan_contable["costos_indirectos"]
        return None
    
    def get_presupuesto_indirectos_dict(self):
        """Obtiene diccionario de 'codigo - nombre' → presupuesto"""
        if self.plan_contable and "costos_indirectos" in self.plan_contable:
            return {
                f"{c['codigo']} - {c['nombre']}": c["presupuesto_mensual"]
                for c in self.plan_contable["costos_indirectos"]
            }
        return None
    
    # ========== MÉTODOS DE ACCESO A GRUPOS OCUPACIONALES ==========
    
    def get_grupos_ocupacionales_lista(self):
        """Obtiene lista de tuplas (nombre, salario)"""
        if self.grupos_ocupacionales and "grupos" in self.grupos_ocupacionales:
            return [(g["nombre"], g["salario_base"]) for g in self.grupos_ocupacionales["grupos"]]
        return None
    
    def get_grupos_completos(self):
        """Obtiene lista completa de grupos con todos sus datos"""
        if self.grupos_ocupacionales and "grupos" in self.grupos_ocupacionales:
            return self.grupos_ocupacionales["grupos"]
        return None


# Instancia global del mapper (singleton)
_mapper_instance = None


def get_mapper():
    """
    Obtiene la instancia global del mapper (patrón singleton)
    
    Returns:
        ConfigMapper: Instancia del mapper
    """
    global _mapper_instance
    if _mapper_instance is None:
        _mapper_instance = ConfigMapper()
        _mapper_instance.cargar_configuracion()
    return _mapper_instance
