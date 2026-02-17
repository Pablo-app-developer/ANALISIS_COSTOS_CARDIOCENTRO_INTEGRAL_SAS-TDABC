"""
Demo simple del adaptador generico TDABC
"""
from src.adaptador import AdaptadorEmpresa
import os

# Crear directorio de ejemplos
os.makedirs("ejemplos", exist_ok=True)

print("\n" + "="*60)
print("DEMO: ADAPTADOR GENERICO TDABC")
print("="*60 + "\n")

# Generar plantillas
adaptador = AdaptadorEmpresa()

print("Generando plantillas...")
adaptador.generar_plantilla("ejemplos/clinica_dental.json", "salud")
print()
adaptador.generar_plantilla("ejemplos/instituto_educativo.json", "educacion")
print()
adaptador.generar_plantilla("ejemplos/fabrica.json", "manufactura")

print("\n" + "="*60)
print("PLANTILLAS GENERADAS EN carpeta 'ejemplos/'")
print("="*60)
print("\nPasos siguientes:")
print("  1. Edita uno de los archivos JSON con los datos de tu empresa")
print("  2. Ejecuta: python -c \"from src.adaptador import adaptar_empresa; adaptar_empresa('ejemplos/tu_archivo.json')\"")
print("  3. Ejecuta: python main.py")
print("\n" + "="*60 + "\n")
