# Guía: Importar Datos Reales del Sistema

## 📋 Estructura de Datos Real

El sistema ahora soporta importar datos directamente desde tus exportaciones del sistema médico/contable.

---

## 1️⃣ SERVICIOS PRESTADOS (Producción)

### Estructura Real del Archivo:
```
Nombres | Apellidos | Identificacion | Departamento | Ciudad | Fecha Cita | codigo_servicio | servicio | MD Nomb | area | estado | entidad Codi | entidad | Valor Servicio | Valor Recaudo | No Factura | Sede | Ciudad Servicio | Especialidad
```

### Columnas Requeridas:
- `codigo_servicio` - Código del servicio
- `servicio` - Nombre del servicio  
- `Sede` - Sede donde se prestó
- `entidad` - Nombre de la EPS/Aseguradora
- `Valor Servicio` - Valor facturado

### Ejemplo de Importación:
```python
from src.importador_produccion import ImportadorProduccion

# Cargar datos reales
importador = ImportadorProduccion()
exito = importador.cargar_desde_excel("servicios_prestados_enero.xlsx")

if exito:
    print(importador.obtener_reporte())
    
    # El sistema agrupa automáticamente por servicio-sede-entidad
    # y cuenta cuántos servicios se prestaron
else:
    print("Errores:", importador.errores)
```

---

## 2️⃣ AUXILIARES CONTABLES (Costos Indirectos)

### Estructura Real del Archivo:
```
CLASE | Fecha | Auxiliar | Desc. auxiliar | C.O. movto. | Desc. C.O. movto. | U.N. | Docto. Proveedor | Desc. U.N. | Tercero movto. | Razón social tercero movto. | Débitos | Créditos | Neto
```

### Ejemplo:
```
7 - COSTOS SGSSS | 26/09/2025 | 73130601 | ACUEDUCTO Y ALCANTARILLADO | 003 | SEDE CABECERA | 001 | 3369294--08756797 | SERVICIO MEDICO | 890200162 | ACUEDUCTO METROPOLITANO DE BUCARAMANGA SA ESP | $457.880,00 | $0,00 | $457.880,00
```

### Ejemplo de Importación:
```python
from src.importador_contabilidad import ImportadorContabilidad

# Cargar auxiliares contables
importador = ImportadorContabilidad()
exito = importador.cargar_desde_excel("auxiliares_septiembre.xlsx")

if exito:
    # Obtener costos por cuenta
    costos_cuenta = importador.obtener_costos_por_cuenta()
    
    # Obtener costos por centro
    costos_centro = importador.obtener_costos_por_centro()
    
    # Filtrar solo costos (clase 7)
    solo_costos = importador.filtrar_por_clase("7 - COSTOS")
```

---

## 3️⃣ NÓMINA (Mano de Obra)

### Estructura Real del Archivo:
```
Empleado | Nombre del empleado | Ndc | Descripcion estado | Descripcion C.O. | Descripcion ccosto | Descripcion proyecto | Descripcion un | Fecha ingreso | Fecha retiro | Fecha contrato hasta | Descripcion del cargo | Salario
```

### Ejemplo:
```
13870807 | SEPULVEDA PINTO LUIS FERNANDO | 1 | Activo | SEDE BARRANCA | PRODUCCION | NOMINA | ADMINISTRACION (BACKOFFICE) | 2022-06-21 | | 2026-06-20 | COORDINADOR DE SEDES MUNICIPALES | 3048000,00
```

### Ejemplo de Importación:
```python
from src.importador_nomina import ImportadorNomina

# Cargar nómina
importador = ImportadorNomina()
exito = importador.cargar_desde_excel("nomina_activos.xlsx")

if exito:
    # Obtener empleados por sede
    por_sede = importador.obtener_empleados_por_sede()
    
    # Obtener costo total de nómina
    costo_total = importador.obtener_costo_total_nomina()
    
    # Obtener solo empleados activos
    activos = importador.filtrar_activos()
```

---

## 🔄 Flujo Completo de Importación

```python
from src.modelo_tdabc import ModeloTDABC

# 1. Preparar rutas de archivos
archivos = {
    'produccion': 'datos/servicios_prestados_enero_2026.xlsx',
    'contabilidad': 'datos/auxiliares_enero_2026.xlsx',
    'nomina': 'datos/nomina_enero_2026.xlsx'
}

# 2. Generar modelo con datos reales
modelo = ModeloTDABC()
modelo.generar_archivo_con_datos_reales(
    nombre_archivo="Modelo_TDABC_Enero_2026_Real.xlsx",
    archivo_produccion=archivos['produccion'],
    archivo_contabilidad=archivos['contabilidad'],
    archivo_nomina=archivos['nomina']
)
```

---

## ✅ Ventajas del Sistema Actualizado

1. **Importación Directa**: Exporta desde tu sistema y carga directamente
2. **Sin Reformateo**: Usa las columnas tal como vienen del sistema
3. **Validación Automática**: Detecta errores y valores faltantes
4. **Agrupación Inteligente**: Agrupa automáticamente por servicio-sede-cliente
5. **Limpieza Automática**: Limpia formatos de moneda ($, comas, etc.)

---

## 📊 Procesamiento Automático

### Para Servicios Prestados:
- ✅ Agrupa por: `codigo_servicio` + `Sede` + `entidad`
- ✅ Cuenta: Número de registros = Cantidad de servicios
- ✅ Suma: `Valor Servicio` total facturado
- ✅ Calcula: Valor promedio por servicio

### Para Contabilidad:
- ✅ Limpia: Formatos de moneda ($457.880,00 → 457880)
- ✅ Agrupa: Por cuenta contable
- ✅ Agrupa: Por centro de costo
- ✅ Filtra: Por clase contable (7 - COSTOS)

### Para Nómina:
- ✅ Filtra: Solo empleados activos
- ✅ Agrupa: Por sede
- ✅ Agrupa: Por cargo
- ✅ Calcula: Costo total de nómina

---

## 🎯 Ejemplo Completo Real

```python
# Paso 1: Importar servicios prestados
from src.importador_produccion import ImportadorProduccion

imp_prod = ImportadorProduccion()
imp_prod.cargar_desde_excel("Servicios_Enero_2026.xlsx")
print(imp_prod.obtener_reporte())

# Paso 2: Importar contabilidad
from src.importador_contabilidad import ImportadorContabilidad

imp_cont = ImportadorContabilidad()
imp_cont.cargar_desde_excel("Auxiliares_Enero_2026.xlsx")
print(imp_cont.obtener_reporte())

# Paso 3: Generar modelo TDABC
from src.modelo_tdabc import ModeloTDABC

modelo = ModeloTDABC()
modelo.generar_archivo(
    nombre_archivo="TDABC_Enero_2026.xlsx",
    datos_produccion_path="Servicios_Enero_2026.xlsx",
    datos_contabilidad_path="Auxiliares_Enero_2026.xlsx"
)

print("\n✅ Modelo TDABC generado con datos reales!")
```

---

## ⚠️ Notas Importantes

1. **Exporta desde tu sistema**: No modifiques las columnas, el importador las reconoce automáticamente
2. **Un mes a la vez**: Exporta datos de un solo mes para análisis mensual
3. **Verifica el reporte**: Siempre revisa el reporte de importación para detectar problemas
4. **Backup**: Guarda copias de tus exportaciones originales

---

¡El sistema ahora trabaja con TUS datos reales! 🎉
