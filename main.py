"""
Generador de Modelo TDABC para CardioCentro Diagnóstico Integral S.A.S.
Modelo profesional de costeo basado en Time-Driven Activity-Based Costing

Este es el punto de entrada principal del programa modular.
"""

from src.modelo_tdabc import ModeloTDABC


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("GENERADOR DE MODELO TDABC")
    print("CardioCentro Diagnóstico Integral S.A.S.")
    print("="*60 + "\n")
    
    modelo = ModeloTDABC()
    modelo.generar_archivo("Modelo_TDABC_CardioCentro.xlsx")
    
    print("\n[SUCCESS] MODELO TDABC GENERADO CORRECTAMENTE")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
