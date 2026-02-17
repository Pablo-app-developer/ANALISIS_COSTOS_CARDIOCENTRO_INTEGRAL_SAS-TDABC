# Análisis de Lógica del RESUMEN_EJECUTIVO

## 🔍 PROBLEMAS IDENTIFICADOS

### 1. ❌ INDICADORES GLOBALES - Fórmulas Duplicadas/Incorrectas

**Problema en líneas 40-50:**
```python
indicadores = [
    ("Ingresos Operacionales (Facturación)", "=SUM(TablaProduccion[Total Facturado])", '$#,##0'),
    ("Total Costos Asignados (TDABC)", "=SUM(TablaCosteo[Costo Total]*TablaCosteo[Volumen])", '$#,##0'),
    # ... desglose de costos ...
    ("Utilidad Operacional (Estimada)", "=B7-B8", '$#,##0'),  # ← Fila 12
    ("Margen Operacional %", "=IF(B7>0,B12/B7,0)", '0.0%'),   # ← Fila 13
    ("Total Servicios Prestados", "=SUM(...)", '#,##0'),       # ← Fila 14
    ("MARGEN OPERATIVO", "=B7-B8", '$#,##0'),                  # ← Fila 15 DUPLICADO!
    ("MARGEN OPERATIVO %", "=IF(B7>0,B13/B7,0)", '0.0%'),     # ← Fila 16 DUPLICADO!
]
```

**Problemas:**
1. ❌ "MARGEN OPERATIVO" aparece 2 veces (filas 12 y 15)
2. ❌ Fórmula de % usa B13 pero debería usar B15 (el margen correcto)
3. ❌ Confusión entre "Utilidad Operacional" y "MARGEN OPERATIVO"

---

### 2. ⚠️ CONCILIACIÓN DE COSTOS - Lógica Correcta pero Mejorable

**Líneas 101-114:**
```python
# Materia Prima / Insumos (71)
ws[f'B{row}'] = '=SUMIFS(TablaIndirectos[Valor],TablaIndirectos[Cuenta],"71*")'
ws[f'C{row}'] = '=SUMPRODUCT(TablaCosteo[Costo Insumos],TablaCosteo[Volumen])'

# Mano de Obra Directa (72)
ws[f'B{row}'] = '=SUMIFS(TablaIndirectos[Valor],TablaIndirectos[Cuenta],"72*")'
ws[f'C{row}'] = '=SUMPRODUCT(TablaCosteo[Costo MO],TablaCosteo[Volumen])'

# Costos Indirectos CIF (73)
ws[f'B{row}'] = '=SUMIFS(TablaIndirectos[Valor],TablaIndirectos[Cuenta],"73*")'
ws[f'C{row}'] = '=SUMPRODUCT(TablaCosteo[Costo CIF],TablaCosteo[Volumen])'
```

**Análisis:**
- ✅ Lógica CORRECTA: Compara contabilidad (71*, 72*, 73*) vs TDABC distribuido
- ✅ Diferencia = Capacidad ociosa (correcto)
- ⚠️ PERO: Asume que TablaIndirectos tiene TODAS las cuentas 71, 72, 73

**Problema potencial:**
- Si TablaIndirectos no tiene datos de 71* o 72*, mostrará $0 en columna B
- Esto haría que la diferencia sea incorrecta

---

### 3. ⚠️ RENTABILIDAD POR SERVICIO - Lógica Correcta

**Líneas 163-179:**
```python
for servicio in config.SERVICIOS:
    ws[f'B{row}'] = f"=SUMPRODUCT((TablaCosteo[Servicio]=A{row})*(TablaCosteo[Costo Total])*(TablaCosteo[Volumen]))"
    ws[f'C{row}'] = f"=SUMIFS(TablaProduccion[Total Facturado],TablaProduccion[Servicio],A{row})"
    ws[f'D{row}'] = f"=C{row}-B{row}"  # Margen = Ingresos - Costos
    ws[f'E{row}'] = f"=IF(C{row}>0,D{row}/C{row},0)"  # Margen % = Margen/Ingresos
```

**Análisis:**
- ✅ Costo Total: SUMPRODUCT correcto (suma costos * volumen por servicio)
- ✅ Facturación: SUMIFS correcto (suma facturación por servicio)
- ✅ Margen: Ingresos - Costos (correcto)
- ✅ Margen %: Margen / Ingresos (correcto)

**Problema potencial:**
- ⚠️ Si un servicio NO tiene producción, mostrará Costo=0, Facturación=0, Margen=0
- Esto puede confundir (servicios que existen pero no se prestaron)

---

## 🔧 CORRECCIONES NECESARIAS

### Corrección 1: Eliminar Duplicados en Indicadores Globales

**ANTES:**
```python
indicadores = [
    ("Ingresos Operacionales", "...", ...),
    ("Total Costos Asignados", "...", ...),
    ("   - Costo MO", "...", ...),
    ("   - Costo Insumos", "...", ...),
    ("   - Costo CIF", "...", ...),
    ("Utilidad Operacional", "=B7-B8", ...),      # Fila 12
    ("Margen Operacional %", "=IF(B7>0,B12/B7,0)", ...),  # Fila 13
    ("Total Servicios", "...", ...),              # Fila 14
    ("MARGEN OPERATIVO", "=B7-B8", ...),          # DUPLICADO
    ("MARGEN OPERATIVO %", "=IF(B7>0,B13/B7,0)", ...), # DUPLICADO
]
```

**DESPUÉS:**
```python
indicadores = [
    ("Ingresos Operacionales (Facturación)", "=SUM(TablaProduccion[Total Facturado])", '$#,##0'),
    ("Total Costos Asignados (TDABC)", "=SUM(TablaCosteo[Costo Total]*TablaCosteo[Volumen])", '$#,##0'),
    ("   - Costo Personal Directo", "=SUM(TablaCosteo[Costo MO]*TablaCosteo[Volumen])", '$#,##0'),
    ("   - Costo Insumos", "=SUM(TablaCosteo[Costo Insumos]*TablaCosteo[Volumen])", '$#,##0'),
    ("   - Costos Indirectos (CIF)", "=SUM(TablaCosteo[Costo CIF]*TablaCosteo[Volumen])", '$#,##0'),
    ("", "", ""),  # Línea en blanco
    ("UTILIDAD OPERACIONAL", "=B7-B8", '$#,##0'),
    ("MARGEN OPERACIONAL %", "=IF(B7>0,B12/B7,0)", '0.0%'),
    ("", "", ""),  # Línea en blanco
    ("Total Servicios Prestados", "=SUM(TablaProduccion[Cantidad])", '#,##0'),
    ("Precio Promedio por Servicio", "=IF(B14>0,B7/B14,0)", '$#,##0'),
    ("Costo Promedio por Servicio", "=IF(B14>0,B8/B14,0)", '$#,##0'),
]
```

---

### Corrección 2: Mejorar Conciliación de Costos

**Agregar validación:**
```python
# Después de la diferencia, agregar:
row += 1
ws[f'A{row}'] = "% de Utilización de Capacidad"
ws[f'B{row}'] = f"=IF(SUM(B{r_start}:B{r_end})>0,SUM(C{r_start}:C{r_end})/SUM(B{r_start}:B{r_end}),0)"
ws[f'B{row}'].number_format = '0.0%'
ws.merge_cells(f'B{row}:C{row}')
```

---

### Corrección 3: Filtrar Servicios Sin Producción

**Opción 1: Mostrar solo servicios con producción**
```python
# En lugar de:
for servicio in config.SERVICIOS:
    row += 1
    ws[f'A{row}'] = servicio
    # ...

# Usar:
for servicio in config.SERVICIOS:
    row += 1
    ws[f'A{row}'] = servicio
    ws[f'B{row}'] = f"=SUMPRODUCT(...)"
    ws[f'C{row}'] = f"=SUMIFS(...)"
    ws[f'D{row}'] = f"=C{row}-B{row}"
    ws[f'E{row}'] = f"=IF(C{row}>0,D{row}/C{row},0)"
    
    # Agregar formato condicional para resaltar servicios sin producción
    # (en gris o con nota)
```

**Opción 2: Agregar columna de volumen**
```python
# Agregar columna "Volumen" antes de costos
ws[f'B{row}'] = "Volumen"
ws[f'C{row}'] = "Costo Total"
ws[f'D{row}'] = "Facturación Total"
# ...

# En los datos:
ws[f'B{row}'] = f"=SUMIFS(TablaProduccion[Cantidad],TablaProduccion[Servicio],A{row})"
```

---

## ✅ RESUMEN DE VALIDACIÓN

| Sección | Estado | Problema | Severidad |
|---------|--------|----------|-----------|
| **Indicadores Globales** | ❌ ERROR | Duplicados + fórmulas incorrectas | 🔴 ALTA |
| **Conciliación Costos** | ✅ OK | Lógica correcta, mejorable | 🟡 MEDIA |
| **Rentabilidad Servicio** | ✅ OK | Lógica correcta, puede confundir | 🟢 BAJA |
| **Análisis por Sede** | ✅ OK | Lógica correcta | ✅ OK |

---

## 🎯 RECOMENDACIONES

1. **URGENTE**: Eliminar duplicados en Indicadores Globales
2. **IMPORTANTE**: Agregar % de utilización de capacidad en Conciliación
3. **SUGERIDO**: Agregar columna de volumen en Rentabilidad por Servicio
4. **SUGERIDO**: Formato condicional para servicios sin producción

---

## 📊 EJEMPLO DE VALORES ESPERADOS

### Indicadores Globales (Correcto):
```
Ingresos Operacionales:     $500,000,000
Total Costos Asignados:     $350,000,000
   - Costo Personal:        $200,000,000
   - Costo Insumos:         $100,000,000
   - Costos Indirectos:      $50,000,000

UTILIDAD OPERACIONAL:       $150,000,000  (= 500M - 350M)
MARGEN OPERACIONAL %:       30.0%         (= 150M / 500M)
```

### Conciliación (Correcto):
```
                           Contable    Distribuido
Insumos (71):             $120,000,000  $100,000,000
MO (72):                  $220,000,000  $200,000,000
CIF (73):                  $60,000,000   $50,000,000

DIFERENCIA (Capacidad):    $50,000,000  (= 400M - 350M)
% Utilización:             87.5%        (= 350M / 400M)
```

### Rentabilidad por Servicio (Correcto):
```
Servicio          Volumen  Costo      Facturación  Margen      Margen%
Ecocardiograma    100      $15,000,000 $20,000,000  $5,000,000  25.0%
Cateterismo       20       $50,000,000 $60,000,000  $10,000,000 16.7%
Consulta          500      $10,000,000 $15,000,000  $5,000,000  33.3%
```
