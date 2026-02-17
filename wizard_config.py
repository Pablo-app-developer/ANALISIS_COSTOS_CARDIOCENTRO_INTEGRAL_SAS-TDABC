"""
Wizard interactivo para configurar el sistema TDABC.

Asistente CLI que guía al usuario paso a paso para crear configuraciones.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import re


class WizardTDABC:
    """
    Wizard interactivo para configurar el sistema TDABC.
    """
    
    def __init__(self):
        self.config = {}
        self.errores = []
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / "src" / "config"
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_banner(self, titulo: str):
        """Muestra un banner decorativo"""
        print("\n" + "=" * 70)
        print(f"  {titulo}")
        print("=" * 70 + "\n")
    
    def mostrar_progreso(self, paso: int, total: int, descripcion: str):
        """Muestra barra de progreso"""
        porcentaje = (paso / total) * 100
        barra = "█" * int(porcentaje / 5) + "░" * (20 - int(porcentaje / 5))
        print(f"\n[{barra}] {porcentaje:.0f}% - Paso {paso}/{total}: {descripcion}\n")
    
    def validar_texto(self, texto: str, min_len: int = 1, max_len: int = 100) -> bool:
        """Valida que el texto esté en el rango permitido"""
        return min_len <= len(texto.strip()) <= max_len
    
    def validar_numero(self, valor: str, min_val: float = 0, max_val: float = float('inf')) -> Optional[float]:
        """Valida y convierte un número"""
        try:
            num = float(valor.replace(',', '.'))
            if min_val <= num <= max_val:
                return num
            return None
        except ValueError:
            return None
    
    def validar_email(self, email: str) -> bool:
        """Valida formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def preguntar(self, pregunta: str, valor_defecto: str = "", validador=None, tipo: str = "texto") -> str:
        """
        Hace una pregunta al usuario con validación.
        
        Args:
            pregunta: Texto de la pregunta
            valor_defecto: Valor por defecto
            validador: Función de validación
            tipo: Tipo de dato esperado
        """
        while True:
            if valor_defecto:
                respuesta = input(f"{pregunta} [{valor_defecto}]: ").strip()
                if not respuesta:
                    respuesta = valor_defecto
            else:
                respuesta = input(f"{pregunta}: ").strip()
            
            # Validar
            if validador:
                if validador(respuesta):
                    return respuesta
                else:
                    print(f"  ❌ Valor inválido. Intenta de nuevo.")
            else:
                if respuesta:
                    return respuesta
                else:
                    print(f"  ❌ Este campo es obligatorio.")
    
    def preguntar_si_no(self, pregunta: str, defecto: bool = True) -> bool:
        """Pregunta Sí/No"""
        defecto_texto = "S" if defecto else "N"
        while True:
            respuesta = input(f"{pregunta} (S/N) [{defecto_texto}]: ").strip().upper()
            if not respuesta:
                return defecto
            if respuesta in ['S', 'SI', 'Y', 'YES']:
                return True
            elif respuesta in ['N', 'NO']:
                return False
            else:
                print("  ❌ Responde S (Sí) o N (No)")
    
    def seleccionar_opcion(self, pregunta: str, opciones: List[str], permitir_multiple: bool = False) -> Any:
        """
        Muestra un menú de opciones.
        
        Args:
            pregunta: Texto de la pregunta
            opciones: Lista de opciones
            permitir_multiple: Si permite selección múltiple
        """
        print(f"\n{pregunta}")
        for i, opcion in enumerate(opciones, 1):
            print(f"  {i}. {opcion}")
        
        if permitir_multiple:
            print("\n  (Ingresa números separados por comas, ej: 1,3,5)")
            while True:
                respuesta = input("\nSelección: ").strip()
                try:
                    indices = [int(x.strip()) for x in respuesta.split(',')]
                    if all(1 <= i <= len(opciones) for i in indices):
                        return [opciones[i-1] for i in indices]
                    else:
                        print(f"  ❌ Números deben estar entre 1 y {len(opciones)}")
                except ValueError:
                    print("  ❌ Formato inválido. Usa números separados por comas.")
        else:
            while True:
                respuesta = input("\nSelección: ").strip()
                try:
                    indice = int(respuesta)
                    if 1 <= indice <= len(opciones):
                        return opciones[indice - 1]
                    else:
                        print(f"  ❌ Número debe estar entre 1 y {len(opciones)}")
                except ValueError:
                    print("  ❌ Ingresa un número válido")
    
    # === PASOS DEL WIZARD ===
    
    def paso_1_informacion_empresa(self):
        """Paso 1: Información básica de la empresa"""
        self.mostrar_progreso(1, 7, "Información de la Empresa")
        
        print("📋 Información Básica de la Empresa\n")
        
        self.config['empresa'] = {
            'nombre': self.preguntar(
                "Nombre de la empresa",
                validador=lambda x: self.validar_texto(x, 3, 100)
            ),
            'nit': self.preguntar("NIT/RUC/RFC"),
            'sector': self.seleccionar_opcion(
                "Sector de la empresa",
                ["Salud", "Educación", "Manufactura", "Servicios", "Otro"]
            ),
            'pais': self.preguntar("País", "Colombia"),
            'ciudad': self.preguntar("Ciudad"),
            'contacto': self.preguntar("Email de contacto", validador=self.validar_email)
        }
        
        print("\n✅ Información de empresa guardada")
    
    def paso_2_parametros_tdabc(self):
        """Paso 2: Parámetros TDABC"""
        self.mostrar_progreso(2, 7, "Parámetros TDABC")
        
        print("⚙️ Configuración de Parámetros TDABC\n")
        
        # Horas laborales
        print("📅 Tiempo de Trabajo:")
        dias_mes = self.validar_numero(
            self.preguntar("Días laborales por mes", "23"),
            min_val=20, max_val=31
        )
        horas_dia = self.validar_numero(
            self.preguntar("Horas por día", "8"),
            min_val=4, max_val=12
        )
        
        horas_mes = int(dias_mes * horas_dia)
        
        self.config['parametros_tdabc'] = {
            'tiempo_trabajo': {
                'horas_mes': horas_mes,
                'dias_laborales_mes': int(dias_mes),
                'horas_dia': int(horas_dia),
                'minutos_mes': horas_mes * 60
            }
        }
        
        print(f"\n  ✓ Total: {horas_mes} horas/mes ({horas_mes * 60} minutos)")
        
        # Prestaciones sociales
        print("\n💰 Prestaciones Sociales:")
        if self.preguntar_si_no("¿Usar tasas de Colombia (52.05%)?", True):
            tasa_prestaciones = 0.5205
        else:
            tasa_prestaciones = self.validar_numero(
                self.preguntar("Tasa total de prestaciones (ej: 0.45 para 45%)"),
                min_val=0, max_val=1
            )
        
        self.config['parametros_tdabc']['tasas_prestaciones'] = {
            'total_prestaciones': tasa_prestaciones
        }
        
        print(f"\n  ✓ Tasa de prestaciones: {tasa_prestaciones * 100:.2f}%")
        
        # Moneda
        print("\n💵 Formato de Moneda:")
        simbolo = self.preguntar("Símbolo de moneda", "$")
        
        self.config['parametros_tdabc']['formatos_moneda'] = {
            'simbolo': simbolo,
            'formato_excel': f'{simbolo}#,##0'
        }
        
        print("\n✅ Parámetros TDABC configurados")
    
    def paso_3_centros_costo(self):
        """Paso 3: Centros de costo"""
        self.mostrar_progreso(3, 7, "Centros de Costo")
        
        print("🏢 Configuración de Centros de Costo\n")
        
        centros = []
        
        print("Ingresa los centros de costo de tu empresa.")
        print("(Presiona Enter sin texto para terminar)\n")
        
        while True:
            nombre = input(f"Centro de costo #{len(centros) + 1}: ").strip()
            if not nombre:
                if len(centros) == 0:
                    print("  ❌ Debes ingresar al menos un centro de costo")
                    continue
                break
            
            codigo = f"CC{len(centros) + 1:03d}"
            centros.append({
                'codigo': codigo,
                'nombre': nombre,
                'tipo': 'Productivo'
            })
            print(f"  ✓ Agregado: {codigo} - {nombre}")
        
        self.config['centros_costo'] = centros
        print(f"\n✅ {len(centros)} centros de costo configurados")
    
    def paso_4_servicios(self):
        """Paso 4: Servicios"""
        self.mostrar_progreso(4, 7, "Servicios")
        
        print("🔧 Configuración de Servicios\n")
        
        if self.preguntar_si_no("¿Importar servicios desde un archivo Excel?", False):
            print("\n  ℹ️  Después del wizard, usa:")
            print("     python -m src.importador_produccion")
            self.config['servicios'] = []
        else:
            servicios = []
            
            print("Ingresa los servicios que ofreces.")
            print("(Presiona Enter sin texto para terminar)\n")
            
            while True:
                nombre = input(f"Servicio #{len(servicios) + 1}: ").strip()
                if not nombre:
                    if len(servicios) == 0:
                        print("  ❌ Debes ingresar al menos un servicio")
                        continue
                    break
                
                codigo = f"SV{len(servicios) + 1:03d}"
                
                # Categoría
                categoria = self.seleccionar_opcion(
                    f"Categoría de '{nombre}'",
                    ["Diagnóstico", "Terapéutico", "Quirúrgico", "Consulta", "Otro"]
                )
                
                servicios.append({
                    'codigo': codigo,
                    'nombre': nombre,
                    'categoria': categoria,
                    'complejidad': 'Media',
                    'requiere_insumos': True
                })
                print(f"  ✓ Agregado: {codigo} - {nombre} ({categoria})")
            
            self.config['servicios'] = servicios
            print(f"\n✅ {len(servicios)} servicios configurados")
    
    def paso_5_sedes(self):
        """Paso 5: Sedes"""
        self.mostrar_progreso(5, 7, "Sedes")
        
        print("📍 Configuración de Sedes\n")
        
        sedes = []
        
        print("Ingresa las sedes/sucursales de tu empresa.")
        print("(Presiona Enter sin texto para terminar)\n")
        
        while True:
            nombre = input(f"Sede #{len(sedes) + 1}: ").strip()
            if not nombre:
                if len(sedes) == 0:
                    print("  ❌ Debes ingresar al menos una sede")
                    continue
                break
            
            sedes.append(nombre)
            print(f"  ✓ Agregado: {nombre}")
        
        self.config['sedes'] = sedes
        print(f"\n✅ {len(sedes)} sedes configuradas")
    
    def paso_6_clientes(self):
        """Paso 6: Clientes/Aseguradoras"""
        self.mostrar_progreso(6, 7, "Clientes/Aseguradoras")
        
        print("👥 Configuración de Clientes/Aseguradoras\n")
        
        clientes = []
        
        print("Ingresa tus principales clientes o aseguradoras.")
        print("(Presiona Enter sin texto para terminar)\n")
        
        while True:
            nombre = input(f"Cliente #{len(clientes) + 1}: ").strip()
            if not nombre:
                if len(clientes) == 0:
                    print("  ❌ Debes ingresar al menos un cliente")
                    continue
                break
            
            clientes.append(nombre)
            print(f"  ✓ Agregado: {nombre}")
        
        self.config['aseguradoras'] = clientes
        print(f"\n✅ {len(clientes)} clientes configurados")
    
    def paso_7_hojas_excel(self):
        """Paso 7: Configuración de hojas Excel"""
        self.mostrar_progreso(7, 7, "Hojas del Modelo Excel")
        
        print("📊 Configuración de Hojas del Modelo\n")
        
        hojas_disponibles = [
            ("SERVICIOS", "Catálogo de servicios", True),
            ("PRODUCCION", "Volúmenes y facturación", True),
            ("CENTROS_COSTO", "Centros de costo", True),
            ("GRUPOS_OCUPACIONALES", "Grupos ocupacionales", True),
            ("NOMINA", "Nómina y costos de personal", True),
            ("COSTOS_INDIRECTOS", "Costos indirectos", True),
            ("DISTRIBUCION_TIEMPO", "Distribución de tiempo", False),
            ("ECUACIONES_TIEMPO", "Ecuaciones de tiempo", False),
            ("COSTO_CAPACIDAD", "Costo de capacidad", False),
            ("ASIGNACION_COSTOS", "Asignación de costos", False),
            ("ANALISIS_RENTABILIDAD", "Análisis de rentabilidad", True)
        ]
        
        tipo_modelo = self.seleccionar_opcion(
            "¿Qué tipo de modelo deseas?",
            [
                "Completo (11 hojas - análisis detallado)",
                "Simplificado (6 hojas - análisis básico)",
                "Personalizado (seleccionar hojas manualmente)"
            ]
        )
        
        if "Completo" in tipo_modelo:
            hojas_activas = [(h[0], h[1], True) for h in hojas_disponibles]
        elif "Simplificado" in tipo_modelo:
            hojas_activas = [(h[0], h[1], h[2]) for h in hojas_disponibles]
        else:
            print("\nSelecciona las hojas que deseas incluir:")
            hojas_activas = []
            for nombre, desc, _ in hojas_disponibles:
                incluir = self.preguntar_si_no(f"  ¿Incluir {nombre}? ({desc})", True)
                hojas_activas.append((nombre, desc, incluir))
        
        self.config['hojas_activas'] = [
            {
                'nombre': nombre,
                'descripcion': desc,
                'activa': activa,
                'orden': i + 1
            }
            for i, (nombre, desc, activa) in enumerate(hojas_activas)
        ]
        
        total_activas = sum(1 for h in hojas_activas if h[2])
        print(f"\n✅ Modelo configurado con {total_activas} hojas activas")
    
    def resumen_configuracion(self):
        """Muestra resumen de la configuración"""
        self.limpiar_pantalla()
        self.mostrar_banner("RESUMEN DE CONFIGURACIÓN")
        
        print(f"🏢 Empresa: {self.config['empresa']['nombre']}")
        print(f"   NIT: {self.config['empresa']['nit']}")
        print(f"   Sector: {self.config['empresa']['sector']}")
        print(f"   País: {self.config['empresa']['pais']}")
        
        print(f"\n⚙️  Parámetros TDABC:")
        print(f"   Horas/mes: {self.config['parametros_tdabc']['tiempo_trabajo']['horas_mes']}")
        print(f"   Prestaciones: {self.config['parametros_tdabc']['tasas_prestaciones']['total_prestaciones'] * 100:.2f}%")
        
        print(f"\n📊 Elementos Configurados:")
        print(f"   Centros de costo: {len(self.config.get('centros_costo', []))}")
        print(f"   Servicios: {len(self.config.get('servicios', []))}")
        print(f"   Sedes: {len(self.config.get('sedes', []))}")
        print(f"   Clientes: {len(self.config.get('aseguradoras', []))}")
        
        hojas_activas = sum(1 for h in self.config.get('hojas_activas', []) if h['activa'])
        print(f"   Hojas activas: {hojas_activas}")
        
        print("\n" + "=" * 70)
    
    def guardar_configuracion(self):
        """Guarda la configuración en archivos JSON"""
        print("\n💾 Guardando configuración...\n")
        
        try:
            # Crear directorio si no existe
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Guardar empresa_config.json
            empresa_config = {
                'empresa': self.config['empresa'],
                'sedes': self.config.get('sedes', []),
                'aseguradoras': self.config.get('aseguradoras', [])
            }
            
            ruta_empresa = self.config_dir / "empresa_config.json"
            with open(ruta_empresa, 'w', encoding='utf-8') as f:
                json.dump(empresa_config, f, indent=2, ensure_ascii=False)
            print(f"  ✓ {ruta_empresa}")
            
            # Guardar parametros_tdabc.json
            ruta_parametros = self.config_dir / "parametros_tdabc.json"
            with open(ruta_parametros, 'w', encoding='utf-8') as f:
                json.dump({'parametros_tdabc': self.config['parametros_tdabc']}, f, indent=2, ensure_ascii=False)
            print(f"  ✓ {ruta_parametros}")
            
            # Guardar centros_costo.json
            if self.config.get('centros_costo'):
                ruta_centros = self.config_dir / "centros_costo.json"
                with open(ruta_centros, 'w', encoding='utf-8') as f:
                    json.dump({'centros': self.config['centros_costo']}, f, indent=2, ensure_ascii=False)
                print(f"  ✓ {ruta_centros}")
            
            # Guardar servicios.json
            if self.config.get('servicios'):
                ruta_servicios = self.config_dir / "servicios.json"
                with open(ruta_servicios, 'w', encoding='utf-8') as f:
                    json.dump({'servicios': self.config['servicios']}, f, indent=2, ensure_ascii=False)
                print(f"  ✓ {ruta_servicios}")
            
            print("\n✅ Configuración guardada exitosamente!")
            return True
            
        except Exception as e:
            print(f"\n❌ Error al guardar configuración: {e}")
            return False
    
    def ejecutar(self):
        """Ejecuta el wizard completo"""
        self.limpiar_pantalla()
        self.mostrar_banner("🧙 WIZARD DE CONFIGURACIÓN TDABC")
        
        print("Bienvenido al asistente de configuración del sistema TDABC.")
        print("Este wizard te guiará paso a paso para configurar tu empresa.\n")
        
        if not self.preguntar_si_no("¿Deseas continuar?", True):
            print("\nWizard cancelado.")
            return
        
        try:
            # Ejecutar pasos
            self.limpiar_pantalla()
            self.paso_1_informacion_empresa()
            
            self.limpiar_pantalla()
            self.paso_2_parametros_tdabc()
            
            self.limpiar_pantalla()
            self.paso_3_centros_costo()
            
            self.limpiar_pantalla()
            self.paso_4_servicios()
            
            self.limpiar_pantalla()
            self.paso_5_sedes()
            
            self.limpiar_pantalla()
            self.paso_6_clientes()
            
            self.limpiar_pantalla()
            self.paso_7_hojas_excel()
            
            # Mostrar resumen
            self.resumen_configuracion()
            
            if self.preguntar_si_no("\n¿Guardar esta configuración?", True):
                if self.guardar_configuracion():
                    print("\n" + "=" * 70)
                    print("🎉 ¡Configuración completada!")
                    print("=" * 70)
                    print("\nPróximos pasos:")
                    print("  1. Revisa los archivos en src/config/")
                    print("  2. Importa tus datos reales (opcional):")
                    print("     python -m src.importador_produccion")
                    print("  3. Genera tu modelo TDABC:")
                    print("     python main.py")
                    print("\n" + "=" * 70)
            else:
                print("\nConfiguración no guardada.")
        
        except KeyboardInterrupt:
            print("\n\n❌ Wizard cancelado por el usuario.")
        except Exception as e:
            print(f"\n\n❌ Error inesperado: {e}")


def main():
    """Punto de entrada del wizard"""
    wizard = WizardTDABC()
    wizard.ejecutar()


if __name__ == "__main__":
    main()
