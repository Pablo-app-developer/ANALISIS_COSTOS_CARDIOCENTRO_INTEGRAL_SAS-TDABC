"""
Script de ejemplo: Cómo adaptar el sistema TDABC a una nueva empresa.

Este script demuestra el uso del adaptador genérico para crear
configuraciones para diferentes tipos de empresas.
"""
from src.adaptador import AdaptadorEmpresa, adaptar_empresa


def ejemplo_generar_plantilla():
    """Ejemplo 1: Generar una plantilla de configuración"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Generar Plantilla de Configuración")
    print("="*60 + "\n")
    
    adaptador = AdaptadorEmpresa()
    
    # Generar plantilla para sector salud
    adaptador.generar_plantilla(
        output_path="ejemplos/clinica_dental.json",
        sector="salud"
    )
    
    # Generar plantilla para sector educación
    adaptador.generar_plantilla(
        output_path="ejemplos/instituto_educativo.json",
        sector="educacion"
    )
    
    # Generar plantilla para sector manufactura
    adaptador.generar_plantilla(
        output_path="ejemplos/fabrica.json",
        sector="manufactura"
    )
    
    print("\n✓ Plantillas generadas en carpeta 'ejemplos/'")
    print("  Edita estos archivos según tu empresa y luego usa adaptar_empresa()")


def ejemplo_validar_configuracion():
    """Ejemplo 2: Validar una configuración existente"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Validar Configuración")
    print("="*60 + "\n")
    
    # Crear configuración de prueba con errores
    config_invalida = {
        "empresa": {
            "nombre_empresa": "Test Clínica",
            # Falta NIT (error)
            "sector": "salud"
        },
        "servicios": []  # Sin servicios (advertencia)
    }
    
    adaptador = AdaptadorEmpresa()
    adaptador.config_data = config_invalida
    
    # Validar
    es_valida = adaptador.validar_configuracion()
    
    # Mostrar reporte
    print(adaptador.obtener_reporte_validacion())
    
    if not es_valida:
        print("\n❌ La configuración tiene errores que deben corregirse")
    else:
        print("\n✓ Configuración válida")


def ejemplo_adaptar_empresa_completo():
    """Ejemplo 3: Proceso completo de adaptación"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Proceso Completo de Adaptación")
    print("="*60 + "\n")
    
    # Paso 1: Generar plantilla
    print("PASO 1: Generar plantilla base")
    adaptador = AdaptadorEmpresa()
    adaptador.generar_plantilla(
        output_path="ejemplos/mi_empresa.json",
        sector="salud"
    )
    
    print("\nPASO 2: Editar el archivo 'ejemplos/mi_empresa.json'")
    print("  - Cambiar nombre de empresa")
    print("  - Agregar/modificar servicios")
    print("  - Ajustar categorías")
    print("  - Definir centros de costo")
    
    print("\nPASO 3: Ejecutar adaptación")
    print("  >>> from src.adaptador import adaptar_empresa")
    print("  >>> adaptar_empresa('ejemplos/mi_empresa.json')")
    
    print("\nPASO 4: Generar modelo TDABC")
    print("  >>> python main.py")
    
    print("\n✓ Proceso completo documentado")


def ejemplo_uso_rapido():
    """Ejemplo 4: Uso rápido con plantilla predefinida"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Uso Rápido - Generar y Adaptar")
    print("="*60 + "\n")
    
    # Generar plantilla
    adaptador = AdaptadorEmpresa()
    adaptador.generar_plantilla(
        output_path="ejemplos/clinica_ejemplo.json",
        sector="salud"
    )
    
    print("\nAhora puedes adaptar directamente:")
    print("  >>> adaptar_empresa('ejemplos/clinica_ejemplo.json')")
    print("\nEsto generará los archivos de configuración en src/config/")
    print("y podrás ejecutar 'python main.py' para generar el modelo TDABC")


if __name__ == "__main__":
    import os
    
    # Crear directorio de ejemplos si no existe
    os.makedirs("ejemplos", exist_ok=True)
    
    print("\n" + "="*60)
    print("EJEMPLOS DE USO DEL ADAPTADOR GENÉRICO TDABC")
    print("="*60)
    
    # Ejecutar ejemplos
    ejemplo_generar_plantilla()
    ejemplo_validar_configuracion()
    ejemplo_adaptar_empresa_completo()
    ejemplo_uso_rapido()
    
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print("\nPara adaptar el sistema a tu empresa:")
    print("  1. Genera una plantilla: adaptador.generar_plantilla('mi_config.json', 'salud')")
    print("  2. Edita el archivo JSON con los datos de tu empresa")
    print("  3. Ejecuta: adaptar_empresa('mi_config.json')")
    print("  4. Genera el modelo: python main.py")
    print("\n" + "="*60 + "\n")
