"""
Importador de datos de nómina (mano de obra).

Importa datos de empleados y salarios desde el sistema de nómina.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ImportadorNomina:
    """
    Importa datos de nómina para análisis de costos de mano de obra.
    """
    
    # Mapeo de columnas del sistema de nómina a columnas estándar
    MAPEO_COLUMNAS = {
        'Empleado': 'identificacion',
        'Nombre del empleado': 'nombre',
        'Descripcion estado': 'estado',
        'Descripcion C.O.': 'sede',
        'Descripcion ccosto': 'centro_costo',
        'Descripcion un': 'unidad_negocio',
        'Fecha ingreso': 'fecha_ingreso',
        'Fecha retiro': 'fecha_retiro',
        'Descripcion del cargo': 'cargo',
        'Salario': 'salario'
    }
    
    def __init__(self):
        self.datos_nomina = None
        self.errores = []
        self.advertencias = []
    
    def cargar_desde_excel(self, ruta_archivo: str, hoja: str = None) -> bool:
        """
        Carga datos de nómina desde Excel.
        
        Args:
            ruta_archivo: Ruta al archivo Excel con nómina
            hoja: Nombre de la hoja (opcional)
            
        Returns:
            True si la carga fue exitosa
        """
        try:
            if hoja:
                df = pd.read_excel(ruta_archivo, sheet_name=hoja)
            else:
                df = pd.read_excel(ruta_archivo)
            
            return self._procesar_dataframe(df, ruta_archivo)
        
        except FileNotFoundError:
            self.errores.append(f"Archivo no encontrado: {ruta_archivo}")
            return False
        except Exception as e:
            self.errores.append(f"Error al leer Excel: {e}")
            return False
    
    def _procesar_dataframe(self, df: pd.DataFrame, origen: str) -> bool:
        """Procesa y valida el DataFrame de nómina"""
        
        # Renombrar columnas según mapeo
        columnas_encontradas = {}
        for col_original, col_estandar in self.MAPEO_COLUMNAS.items():
            if col_original in df.columns:
                columnas_encontradas[col_original] = col_estandar
        
        if not columnas_encontradas:
            self.errores.append(
                f"No se encontraron columnas reconocidas en {origen}. "
                f"Columnas esperadas: {list(self.MAPEO_COLUMNAS.keys())}"
            )
            return False
        
        # Renombrar columnas
        df = df.rename(columns=columnas_encontradas)
        
        # Limpiar salarios (quitar comas y convertir a número)
        if 'salario' in df.columns:
            df['salario'] = df['salario'].astype(str).str.replace(',', '').str.replace('.', '')
            df['salario'] = pd.to_numeric(df['salario'], errors='coerce').fillna(0)
        
        # Validar datos
        if len(df) == 0:
            self.errores.append(f"El archivo {origen} no contiene datos")
            return False
        
        # Guardar datos procesados
        self.datos_nomina = df.to_dict('records')
        
        # Estadísticas
        total_empleados = len(df)
        empleados_activos = len(df[df['estado'].str.contains('Activo', case=False, na=False)]) if 'estado' in df.columns else 0
        sedes_unicas = df['sede'].nunique() if 'sede' in df.columns else 0
        costo_total = df['salario'].sum() if 'salario' in df.columns else 0
        
        self.advertencias.append(f"Datos de nómina cargados:")
        self.advertencias.append(f"  - Total empleados: {total_empleados}")
        self.advertencias.append(f"  - Empleados activos: {empleados_activos}")
        self.advertencias.append(f"  - Sedes: {sedes_unicas}")
        self.advertencias.append(f"  - Costo total nómina: ${costo_total:,.0f}")
        
        return True
    
    def filtrar_activos(self) -> List[Dict]:
        """
        Filtra solo empleados activos.
        
        Returns:
            Lista de empleados activos
        """
        if not self.datos_nomina:
            return []
        
        df = pd.DataFrame(self.datos_nomina)
        
        if 'estado' in df.columns:
            activos = df[df['estado'].str.contains('Activo', case=False, na=False)]
            return activos.to_dict('records')
        
        return self.datos_nomina
    
    def obtener_empleados_por_sede(self) -> Dict[str, List[Dict]]:
        """
        Agrupa empleados por sede.
        
        Returns:
            Diccionario {sede: [empleados]}
        """
        if not self.datos_nomina:
            return {}
        
        df = pd.DataFrame(self.datos_nomina)
        
        if 'sede' not in df.columns:
            return {}
        
        resultado = {}
        for sede in df['sede'].unique():
            if pd.notna(sede):
                empleados = df[df['sede'] == sede].to_dict('records')
                resultado[sede] = empleados
        
        return resultado
    
    def obtener_costo_por_sede(self) -> Dict[str, float]:
        """
        Calcula costo total de nómina por sede.
        
        Returns:
            Diccionario {sede: costo_total}
        """
        if not self.datos_nomina:
            return {}
        
        df = pd.DataFrame(self.datos_nomina)
        
        if 'sede' in df.columns and 'salario' in df.columns:
            costos = df.groupby('sede')['salario'].sum().to_dict()
            return costos
        
        return {}
    
    def obtener_costo_por_cargo(self) -> Dict[str, float]:
        """
        Calcula costo total de nómina por cargo.
        
        Returns:
            Diccionario {cargo: costo_total}
        """
        if not self.datos_nomina:
            return {}
        
        df = pd.DataFrame(self.datos_nomina)
        
        if 'cargo' in df.columns and 'salario' in df.columns:
            costos = df.groupby('cargo')['salario'].sum().to_dict()
            return costos
        
        return {}
    
    def obtener_costo_total_nomina(self) -> float:
        """
        Calcula el costo total de nómina.
        
        Returns:
            Costo total
        """
        if not self.datos_nomina:
            return 0.0
        
        df = pd.DataFrame(self.datos_nomina)
        
        if 'salario' in df.columns:
            return float(df['salario'].sum())
        
        return 0.0
    
    def obtener_reporte(self) -> str:
        """Genera reporte de importación"""
        reporte = []
        reporte.append("=" * 60)
        reporte.append("REPORTE DE IMPORTACIÓN - DATOS DE NÓMINA")
        reporte.append("=" * 60)
        
        if self.errores:
            reporte.append(f"\n[ERROR] ERRORES ({len(self.errores)}):")
            for error in self.errores:
                reporte.append(f"  - {error}")
        
        if self.advertencias:
            reporte.append(f"\n[INFO] INFORMACIÓN:")
            for adv in self.advertencias:
                reporte.append(f"  {adv}")
        
        if not self.errores and self.datos_nomina:
            reporte.append(f"\n[OK] Análisis por sede:")
            costos_sede = self.obtener_costo_por_sede()
            for sede, costo in sorted(costos_sede.items(), key=lambda x: x[1], reverse=True):
                reporte.append(f"  - {sede}: ${costo:,.0f}")
        
        reporte.append("=" * 60)
        return "\n".join(reporte)


def ejemplo_uso_nomina():
    """Ejemplo de uso del importador de nómina"""
    print("\n" + "="*60)
    print("EJEMPLO: Importar Datos de Nómina")
    print("="*60 + "\n")
    
    print("Estructura esperada del archivo Excel:")
    print("-" * 60)
    print("Empleado | Nombre del empleado | Descripcion estado | ...")
    print("13870807 | SEPULVEDA PINTO LUIS | Activo | ...")
    print("-" * 60)
    
    print("\nPasos:")
    print("1. Exporta tu nómina a Excel")
    print("2. Asegúrate que tenga las columnas: Empleado, Nombre, Estado, etc.")
    print("3. Importa:")
    print("\n   >>> from src.importador_nomina import ImportadorNomina")
    print("   >>> importador = ImportadorNomina()")
    print("   >>> importador.cargar_desde_excel('nomina.xlsx')")
    print("   >>> costo_total = importador.obtener_costo_total_nomina()")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    ejemplo_uso_nomina()
