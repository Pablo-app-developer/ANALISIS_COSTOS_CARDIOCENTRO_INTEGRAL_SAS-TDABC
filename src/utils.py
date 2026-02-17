"""
Utilidades generales del modelo TDABC
"""
from openpyxl.worksheet.table import Table, TableStyleInfo


def crear_tabla(ws, nombre_tabla, rango_datos):
    """Convierte un rango de celdas en una Tabla de Excel oficial"""
    tab = Table(displayName=nombre_tabla, ref=rango_datos)
    style = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )
    tab.tableStyleInfo = style
    ws.add_table(tab)
    return tab
