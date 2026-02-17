# Guía: Importar Datos Reales de Producción y Facturación

## 📋 Descripción

El sistema TDABC ahora soporta **importar datos REALES de facturación** en lugar de generar datos aleatorios. Esto permite que el modelo refleje exactamente lo que tu empresa facturó.

---

## 🎯 Datos Requeridos

Para cada servicio prestado, necesitas:

1. **Código del servicio** - Código único (ej: SV001)
2. **Nombre del servicio** - Nombre completo (ej: "Ecocardiograma Transtorácico")
3. **Sede** - Sede donde se prestó (ej: "Sede Principal")
4. **Cliente/EPS** - Entidad que pagó (ej: "EPS Sura", "Sanitas")
5. **Cantidad** - Cantidad EXACTA de servicios prestados
6. **Valor Unitario** - Precio EXACTO facturado por unidad

---

## 📝 Paso a Paso

### Paso 1: Generar Plantilla Excel

```python
from src.importador_produccion import ImportadorProduccion

importador = ImportadorProduccion()
importador.generar_plantilla_excel("mis_datos_produccion.xlsx")
```

Esto crea un archivo Excel con las columnas correctas.

### Paso 2: Llenar la Plantilla

Abre `mis_datos_produccion.xlsx` y llena con tus datos REALES:

| codigo_servicio | nombre_servicio | sede | cliente | cantidad | valor_unitario |
|-----------------|-----------------|------|---------|----------|----------------|
| SV001 | Ecocardiograma Transtorácico | Sede Principal | EPS Sura | 25 | 150000 |
| SV001 | Ecocardiograma Transtorácico | Sede Principal | Sanitas | 18 | 155000 |
| SV002 | Cateterismo Cardíaco | Sede Norte | EPS Sura | 5 | 2500000 |
| ... | ... | ... | ... | ... | ... |

**IMPORTANTE:**
- ✅ Usa los valores EXACTOS que facturaste
- ✅ Incluye TODOS los registros del mes
- ✅ Una fila por cada combinación servicio-sede-cliente

### Paso 3: Generar Modelo con Datos Reales

```python
from src.modelo_tdabc import ModeloTDABC

# Crear modelo con datos reales
modelo = ModeloTDABC()
modelo.generar_archivo(
    nombre_archivo="Modelo_TDABC_Real.xlsx",
    datos_produccion_path="mis_datos_produccion.xlsx"
)
```

---

## 🔄 Comparación: Simulado vs Real

### Modo Simulado (Anterior)
```python
# Genera datos aleatorios
python main.py
# Resultado: Datos de demostración
```

### Modo Real (Nuevo)
```python
# Usa tus datos reales
modelo = ModeloTDABC()
modelo.generar_archivo(
    datos_produccion_path="mis_datos_produccion.xlsx"
)
# Resultado: Modelo basado en facturación real
```

---

## ✅ Validaciones Automáticas

El importador valida:

1. ✅ **Columnas requeridas** - Todas las columnas necesarias están presentes
2. ✅ **Tipos de datos** - Cantidad y valor son numéricos
3. ✅ **Valores positivos** - Cantidad > 0, Valor > 0
4. ✅ **Campos obligatorios** - No hay valores vacíos

Si hay errores, recibirás un reporte detallado:

```
============================================================
REPORTE DE IMPORTACIÓN DE DATOS DE PRODUCCIÓN
============================================================

[ERROR] ERRORES (2):
  - Fila 5: cantidad debe ser mayor a 0
  - Fila 8: valor_unitario debe ser mayor a 0

============================================================
```

---

## 📊 Ejemplo Completo

```python
# 1. Generar plantilla
from src.importador_produccion import ImportadorProduccion

importador = ImportadorProduccion()
importador.generar_plantilla_excel("datos_enero_2026.xlsx")

# 2. Llenar plantilla con datos reales (en Excel)
# ... usuario llena el archivo ...

# 3. Validar datos
importador.cargar_desde_excel("datos_enero_2026.xlsx")
print(importador.obtener_reporte())

# Si hay errores, corregir y volver a cargar
# Si todo está bien, generar modelo:

# 4. Generar modelo TDABC con datos reales
from src.modelo_tdabc import ModeloTDABC

modelo = ModeloTDABC()
modelo.generar_archivo(
    nombre_archivo="Modelo_TDABC_Enero_2026.xlsx",
    datos_produccion_path="datos_enero_2026.xlsx"
)
```

---

## 🎯 Beneficios

### Con Datos Reales:
- ✅ **Precisión 100%** - Refleja exactamente lo facturado
- ✅ **Análisis real** - Costos vs ingresos reales
- ✅ **Toma de decisiones** - Basada en datos verídicos
- ✅ **Auditable** - Trazabilidad completa

### Con Datos Simulados:
- ✅ **Demostración** - Para probar el sistema
- ✅ **Capacitación** - Para entrenar usuarios
- ✅ **Proyecciones** - Para escenarios futuros

---

## 📁 Formatos Soportados

### Excel (.xlsx)
```python
importador.cargar_desde_excel("datos.xlsx")
```

### CSV (.csv)
```python
importador.cargar_desde_csv("datos.csv", separador=",")
```

---

## ⚠️ Notas Importantes

1. **Consistencia de Códigos**: Los códigos de servicio deben coincidir con los definidos en `servicios.json`

2. **Nombres de Sedes**: Deben coincidir con las sedes configuradas

3. **Nombres de Clientes/EPS**: Deben coincidir con las aseguradoras configuradas

4. **Periodo**: Los datos deben ser de un solo mes para análisis mensual

---

## 🔧 Solución de Problemas

### Error: "Columnas faltantes"
**Solución:** Usa la plantilla generada, no crees tu propio archivo

### Error: "cantidad debe ser mayor a 0"
**Solución:** Verifica que no haya celdas vacías o con valor 0

### Error: "Archivo no encontrado"
**Solución:** Verifica la ruta del archivo

### Advertencia: "Código de servicio no encontrado"
**Solución:** Agrega el servicio a `servicios.json` primero

---

## 📞 Soporte

Si tienes problemas importando tus datos:

1. Ejecuta `importador.obtener_reporte()` para ver errores detallados
2. Verifica que la plantilla esté completa
3. Asegúrate de que los datos sean del formato correcto

---

## ✨ Resultado Final

Con datos reales importados, tu modelo TDABC mostrará:

- ✅ Facturación REAL por servicio
- ✅ Volúmenes REALES por sede
- ✅ Distribución REAL por cliente/EPS
- ✅ Costos vs Ingresos REALES
- ✅ Rentabilidad REAL por servicio

**¡Tu modelo TDABC ahora refleja la realidad de tu negocio!** 🎉
