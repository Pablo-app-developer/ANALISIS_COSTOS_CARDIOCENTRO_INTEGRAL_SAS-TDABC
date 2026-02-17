"""
Adaptador genérico para crear modelos TDABC para diferentes empresas.

Este módulo permite generar un modelo TDABC completo a partir de un archivo
de configuración JSON, sin necesidad de modificar código Python.
"""
import json
from pathlib import Path
from typing import Dict, Any, List
import warnings


class AdaptadorEmpresa:
    """
    Adaptador que valida y procesa configuraciones de empresa para TDABC.
    """
    
    CAMPOS_REQUERIDOS_EMPRESA = {
        'nombre_empresa': str,
        'nit': str,
        'sector': str,
        'pais': str
    }
    
    CAMPOS_REQUERIDOS_SERVICIO = {
        'codigo': str,
        'nombre': str,
        'categoria': str
    }
    
    CAMPOS_OPCIONALES_SERVICIO = {
        'complejidad': str,
        'requiere_insumos': bool,
        'volumen_min': int,
        'volumen_max': int,
        'valor_min': (int, float),
        'valor_max': (int, float)
    }
    
    def __init__(self, config_path: str = None):
        """
        Inicializa el adaptador.
        
        Args:
            config_path: Ruta al archivo de configuración JSON
        """
        self.config_path = config_path
        self.config_data = None
        self.errores = []
        self.advertencias = []
    
    def cargar_configuracion(self, config_path: str = None) -> bool:
        """
        Carga y valida un archivo de configuración.
        
        Args:
            config_path: Ruta al archivo JSON de configuración
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        path = config_path or self.config_path
        if not path:
            self.errores.append("No se especificó ruta de configuración")
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
            
            return self.validar_configuracion()
        
        except FileNotFoundError:
            self.errores.append(f"Archivo no encontrado: {path}")
            return False
        except json.JSONDecodeError as e:
            self.errores.append(f"Error al parsear JSON: {e}")
            return False
        except Exception as e:
            self.errores.append(f"Error inesperado: {e}")
            return False
    
    def validar_configuracion(self) -> bool:
        """
        Valida que la configuración tenga todos los campos requeridos.
        
        Returns:
            True si la configuración es válida, False en caso contrario
        """
        if not self.config_data:
            self.errores.append("No hay datos de configuración cargados")
            return False
        
        # Validar información de empresa
        if 'empresa' not in self.config_data:
            self.errores.append("Falta sección 'empresa' en configuración")
            return False
        
        empresa = self.config_data['empresa']
        for campo, tipo in self.CAMPOS_REQUERIDOS_EMPRESA.items():
            if campo not in empresa:
                self.errores.append(f"Campo requerido faltante en empresa: {campo}")
            elif not isinstance(empresa[campo], tipo):
                self.errores.append(f"Campo '{campo}' debe ser de tipo {tipo.__name__}")
        
        # Validar servicios
        if 'servicios' not in self.config_data:
            self.errores.append("Falta sección 'servicios' en configuración")
            return False
        
        servicios = self.config_data['servicios']
        if not isinstance(servicios, list):
            self.errores.append("'servicios' debe ser una lista")
            return False
        
        if len(servicios) == 0:
            self.advertencias.append("No hay servicios definidos")
        
        # Validar cada servicio
        for idx, servicio in enumerate(servicios):
            for campo, tipo in self.CAMPOS_REQUERIDOS_SERVICIO.items():
                if campo not in servicio:
                    self.errores.append(f"Servicio {idx}: falta campo requerido '{campo}'")
                elif not isinstance(servicio[campo], tipo):
                    self.errores.append(f"Servicio {idx}: campo '{campo}' debe ser {tipo.__name__}")
        
        # Validar categorías
        if 'categorias' in self.config_data:
            categorias = self.config_data['categorias']
            if not isinstance(categorias, dict):
                self.errores.append("'categorias' debe ser un diccionario")
        else:
            self.advertencias.append("No hay categorías definidas, se usarán defaults")
        
        # Validar centros de costo
        if 'centros' not in self.config_data:
            self.advertencias.append("No hay centros de costo definidos")
        
        return len(self.errores) == 0
    
    def generar_plantilla(self, output_path: str, sector: str = "salud"):
        """
        Genera una plantilla de configuración para un sector específico.
        
        Args:
            output_path: Ruta donde guardar la plantilla
            sector: Sector de la empresa (salud, educacion, manufactura, etc.)
        """
        plantillas = {
            "salud": self._plantilla_salud(),
            "educacion": self._plantilla_educacion(),
            "manufactura": self._plantilla_manufactura()
        }
        
        plantilla = plantillas.get(sector, plantillas["salud"])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plantilla, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Plantilla generada: {output_path}")
        print(f"  Sector: {sector}")
        print(f"  Edita este archivo y luego usa adaptar_empresa('{output_path}')")
    
    def _plantilla_salud(self) -> Dict:
        """Genera plantilla para sector salud"""
        return {
            "empresa": {
                "nombre_empresa": "Mi Clínica S.A.S.",
                "nit": "900123456-7",
                "sector": "salud",
                "pais": "Colombia",
                "ciudad": "Bogotá"
            },
            "servicios": [
                {
                    "codigo": "SV001",
                    "nombre": "Consulta General",
                    "categoria": "Consulta Externa",
                    "complejidad": "Baja",
                    "requiere_insumos": False,
                    "volumen_min": 50,
                    "volumen_max": 100,
                    "valor_min": 50000,
                    "valor_max": 80000
                },
                {
                    "codigo": "SV002",
                    "nombre": "Procedimiento Quirúrgico Menor",
                    "categoria": "Quirúrgico",
                    "complejidad": "Media",
                    "requiere_insumos": True,
                    "volumen_min": 5,
                    "volumen_max": 15,
                    "valor_min": 500000,
                    "valor_max": 1500000
                }
            ],
            "categorias": {
                "Consulta Externa": {
                    "descripcion": "Consultas médicas ambulatorias",
                    "complejidad_base": "Baja",
                    "requiere_insumos_default": False,
                    "volumen_min_default": 40,
                    "volumen_max_default": 100
                },
                "Quirúrgico": {
                    "descripcion": "Procedimientos quirúrgicos",
                    "complejidad_base": "Alta",
                    "requiere_insumos_default": True,
                    "volumen_min_default": 2,
                    "volumen_max_default": 10
                }
            },
            "centros": [
                {
                    "nombre": "Sede Principal",
                    "ciudad": "Bogotá",
                    "salas": 3
                }
            ],
            "grupos_ocupacionales": [
                ["Médico General", 8000000],
                ["Enfermera", 3000000],
                ["Auxiliar", 1500000]
            ]
        }
    
    def _plantilla_educacion(self) -> Dict:
        """Genera plantilla para sector educación"""
        return {
            "empresa": {
                "nombre_empresa": "Instituto Educativo XYZ",
                "nit": "900234567-8",
                "sector": "educacion",
                "pais": "Colombia",
                "ciudad": "Medellín"
            },
            "servicios": [
                {
                    "codigo": "CU001",
                    "nombre": "Curso Básico",
                    "categoria": "Formación Básica",
                    "complejidad": "Baja",
                    "requiere_insumos": False,
                    "volumen_min": 20,
                    "volumen_max": 50,
                    "valor_min": 200000,
                    "valor_max": 400000
                }
            ],
            "categorias": {
                "Formación Básica": {
                    "descripcion": "Cursos de nivel básico",
                    "complejidad_base": "Baja",
                    "requiere_insumos_default": False,
                    "volumen_min_default": 15,
                    "volumen_max_default": 40
                }
            },
            "centros": [
                {
                    "nombre": "Campus Principal",
                    "ciudad": "Medellín",
                    "salas": 10
                }
            ],
            "grupos_ocupacionales": [
                ["Docente Senior", 6000000],
                ["Docente Junior", 3000000],
                ["Administrativo", 2000000]
            ]
        }
    
    def _plantilla_manufactura(self) -> Dict:
        """Genera plantilla para sector manufactura"""
        return {
            "empresa": {
                "nombre_empresa": "Manufactura ABC S.A.",
                "nit": "900345678-9",
                "sector": "manufactura",
                "pais": "Colombia",
                "ciudad": "Cali"
            },
            "servicios": [
                {
                    "codigo": "PR001",
                    "nombre": "Producto Estándar",
                    "categoria": "Producción Estándar",
                    "complejidad": "Media",
                    "requiere_insumos": True,
                    "volumen_min": 100,
                    "volumen_max": 500,
                    "valor_min": 50000,
                    "valor_max": 100000
                }
            ],
            "categorias": {
                "Producción Estándar": {
                    "descripcion": "Productos de línea estándar",
                    "complejidad_base": "Media",
                    "requiere_insumos_default": True,
                    "volumen_min_default": 50,
                    "volumen_max_default": 300
                }
            },
            "centros": [
                {
                    "nombre": "Planta Principal",
                    "ciudad": "Cali",
                    "salas": 5
                }
            ],
            "grupos_ocupacionales": [
                ["Operario Calificado", 2500000],
                ["Operario", 1500000],
                ["Supervisor", 4000000]
            ]
        }
    
    def obtener_reporte_validacion(self) -> str:
        """
        Genera un reporte de validación con errores y advertencias.
        
        Returns:
            String con el reporte formateado
        """
        reporte = []
        reporte.append("=" * 60)
        reporte.append("REPORTE DE VALIDACIÓN DE CONFIGURACIÓN")
        reporte.append("=" * 60)
        
        if self.errores:
            reporte.append(f"\n❌ ERRORES ({len(self.errores)}):")
            for error in self.errores:
                reporte.append(f"  • {error}")
        
        if self.advertencias:
            reporte.append(f"\n⚠️  ADVERTENCIAS ({len(self.advertencias)}):")
            for adv in self.advertencias:
                reporte.append(f"  • {adv}")
        
        if not self.errores and not self.advertencias:
            reporte.append("\n✅ Configuración válida - Sin errores ni advertencias")
        
        reporte.append("=" * 60)
        return "\n".join(reporte)


def adaptar_empresa(config_path: str) -> bool:
    """
    Función principal para adaptar el sistema TDABC a una nueva empresa.
    
    Args:
        config_path: Ruta al archivo JSON de configuración de la empresa
        
    Returns:
        True si la adaptación fue exitosa, False en caso contrario
        
    Ejemplo:
        >>> adaptar_empresa("config/mi_clinica.json")
        ✓ Configuración cargada correctamente
        ✓ Validación exitosa
        ✓ Archivos de configuración generados en src/config/
        True
    """
    adaptador = AdaptadorEmpresa(config_path)
    
    print(f"\n{'='*60}")
    print("ADAPTADOR GENÉRICO DE EMPRESA - TDABC")
    print(f"{'='*60}\n")
    print(f"Cargando configuración: {config_path}")
    
    if not adaptador.cargar_configuracion():
        print("\n❌ Error al cargar configuración\n")
        print(adaptador.obtener_reporte_validacion())
        return False
    
    print("✓ Configuración cargada correctamente")
    print(adaptador.obtener_reporte_validacion())
    
    if adaptador.errores:
        return False
    
    # Copiar configuración a src/config/
    _copiar_configuracion_a_sistema(adaptador.config_data)
    
    print("\n✅ Adaptación completada exitosamente")
    print("Ahora puedes ejecutar: python main.py")
    print(f"{'='*60}\n")
    
    return True


def _copiar_configuracion_a_sistema(config_data: Dict):
    """
    Copia la configuración validada a los archivos del sistema.
    
    Args:
        config_data: Datos de configuración validados
    """
    config_dir = Path("src/config")
    
    # Guardar empresa_config.json
    empresa_config = {
        "nombre_empresa": config_data['empresa']['nombre_empresa'],
        "nit": config_data['empresa']['nit'],
        "sector": config_data['empresa']['sector'],
        "pais": config_data['empresa']['pais']
    }
    
    with open(config_dir / "empresa_config.json", 'w', encoding='utf-8') as f:
        json.dump(empresa_config, f, indent=4, ensure_ascii=False)
    print(f"  ✓ Generado: empresa_config.json")
    
    # Guardar servicios.json
    servicios_config = {
        "servicios": config_data.get('servicios', []),
        "categorias": config_data.get('categorias', {})
    }
    
    with open(config_dir / "servicios.json", 'w', encoding='utf-8') as f:
        json.dump(servicios_config, f, indent=4, ensure_ascii=False)
    print(f"  ✓ Generado: servicios.json")
    
    # Guardar centros_costo.json si existe
    if 'centros' in config_data:
        centros_config = {
            "centros": config_data['centros'],
            "aseguradoras": config_data.get('aseguradoras', ["Cliente General"])
        }
        
        with open(config_dir / "centros_costo.json", 'w', encoding='utf-8') as f:
            json.dump(centros_config, f, indent=4, ensure_ascii=False)
        print(f"  ✓ Generado: centros_costo.json")
    
    # Guardar grupos_ocupacionales.json si existe
    if 'grupos_ocupacionales' in config_data:
        grupos_config = {
            "grupos": config_data['grupos_ocupacionales']
        }
        
        with open(config_dir / "grupos_ocupacionales.json", 'w', encoding='utf-8') as f:
            json.dump(grupos_config, f, indent=4, ensure_ascii=False)
        print(f"  ✓ Generado: grupos_ocupacionales.json")
