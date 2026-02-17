"""
Importador de datos contables (auxiliares contables).

Importa movimientos contables desde el sistema contable de la empresa.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any


class ImportadorContabilidad:
    """
    Importa datos de auxiliares contables para análisis de costos indirectos.
    """
    
    # Mapeo de columnas del sistema contable a columnas estándar
    MAPEO_COLUMNAS = {
        'CLASE': 'clase',
        'Fecha': 'fecha',
        'Auxiliar': 'codigo_cuenta',
        'Desc. auxiliar': 'nombre_cuenta',
        'C.O. movto.': 'codigo_centro',
        'Desc. C.O. movto.': 'nombre_centro',
        'U.N.': 'codigo_unidad',
        'Desc. U.N.': 'nombre_unidad',
        'Tercero movto.': 'nit_tercero',
        'Razón social tercero movto.': 'nombre_tercero',
        'Débitos': 'debitos',
        'Créditos': 'creditos',
        'Neto': 'neto'
    }
    
    def __init__(self):
        self.datos_contables = None
        self.errores = []
        self.advertencias = []
    
    def cargar_desde_excel(self, ruta_archivo: str, hoja: str = None) -> bool:
        """
        Carga datos contables desde Excel.
        
        Args:
            ruta_archivo: Ruta al archivo Excel con auxiliares contables
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
        """Procesa y valida el DataFrame de contabilidad"""
        
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
        
        # Limpiar valores monetarios (quitar $ y comas)
        for col in ['debitos', 'creditos', 'neto']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace('$', '').str.replace(',', '').str.replace('.', '')
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Validar datos
        if len(df) == 0:
            self.errores.append(f"El archivo {origen} no contiene datos")
            return False
        
        # Guardar datos procesados
        self.datos_contables = df.to_dict('records')
        
        # Estadísticas
        total_registros = len(df)
        total_debitos = df['debitos'].sum() if 'debitos' in df.columns else 0
        total_creditos = df['creditos'].sum() if 'creditos' in df.columns else 0
        cuentas_unicas = df['codigo_cuenta'].nunique() if 'codigo_cuenta' in df.columns else 0
        
        self.advertencias.append(f"Datos contables cargados:")
        self.advertencias.append(f"  - Total registros: {total_registros}")
        self.advertencias.append(f"  - Cuentas únicas: {cuentas_unicas}")
        self.advertencias.append(f"  - Total débitos: ${total_debitos:,.0f}")
        self.advertencias.append(f"  - Total créditos: ${total_creditos:,.0f}")
        
        return True
    
    def obtener_costos_por_cuenta(self) -> Dict[str, float]:
        """
        Obtiene costos agrupados por cuenta contable.
        
        Returns:
            Diccionario {codigo_cuenta: monto_total}
        """
        if not self.datos_contables:
            return {}
        
        df = pd.DataFrame(self.datos_contables)
        
        # Agrupar por cuenta
        if 'codigo_cuenta' in df.columns and 'neto' in df.columns:
            costos = df.groupby('codigo_cuenta')['neto'].sum().to_dict()
            return costos
        
        return {}
    
    def obtener_costos_por_centro(self) -> Dict[str, float]:
        """
        Obtiene costos agrupados por centro de costo.
        
        Returns:
            Diccionario {nombre_centro: monto_total}
        """
        if not self.datos_contables:
            return {}
        
        df = pd.DataFrame(self.datos_contables)
        
        if 'nombre_centro' in df.columns and 'neto' in df.columns:
            costos = df.groupby('nombre_centro')['neto'].sum().to_dict()
            return costos
        
        return {}
    
    def filtrar_por_clase(self, clase: str) -> List[Dict]:
        """
        Filtra movimientos por clase contable.
        
        Args:
            clase: Clase contable (ej: "7 - COSTOS SGSSS")
            
        Returns:
            Lista de movimientos filtrados
        """
        if not self.datos_contables:
            return []
        
        df = pd.DataFrame(self.datos_contables)
        
        if 'clase' in df.columns:
            filtrado = df[df['clase'].str.contains(clase, case=False, na=False)]
            return filtrado.to_dict('records')
        
        return []
    
    def obtener_reporte(self) -> str:
        """Genera reporte de importación"""
        reporte = []
        reporte.append("=" * 60)
        reporte.append("REPORTE DE IMPORTACIÓN - DATOS CONTABLES")
        reporte.append("=" * 60)
        
        if self.errores:
            reporte.append(f"\n[ERROR] ERRORES ({len(self.errores)}):")
            for error in self.errores:
                reporte.append(f"  - {error}")
        
        if self.advertencias:
            reporte.append(f"\n[INFO] INFORMACIÓN:")
            for adv in self.advertencias:
                reporte.append(f"  {adv}")
        
        reporte.append("=" * 60)
        return "\n".join(reporte)


def ejemplo_uso_contabilidad():
    """Ejemplo de uso del importador de contabilidad"""
    print("\n" + "="*60)
    print("EJEMPLO: Importar Auxiliares Contables")
    print("="*60 + "\n")
    
    print("Estructura esperada del archivo Excel:")
    print("-" * 60)
    print("CLASE | Fecha | Auxiliar | Desc. auxiliar | C.O. movto. | ...")
    print("7 - COSTOS | 26/09/2025 | 73130601 | ACUEDUCTO | 003 | ...")
    print("-" * 60)
    
    print("\nPasos:")
    print("1. Exporta tus auxiliares contables a Excel")
    print("2. Asegúrate que tenga las columnas: CLASE, Fecha, Auxiliar, etc.")
    print("3. Importa:")
    print("\n   >>> from src.importador_contabilidad import ImportadorContabilidad")
    print("   >>> importador = ImportadorContabilidad()")
    print("   >>> importador.cargar_desde_excel('auxiliares_contables.xlsx')")
    print("   >>> costos = importador.obtener_costos_por_cuenta()")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    ejemplo_uso_contabilidad()
