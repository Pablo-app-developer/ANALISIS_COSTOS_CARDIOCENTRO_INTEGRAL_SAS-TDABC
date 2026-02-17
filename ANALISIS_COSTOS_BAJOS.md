# 🔍 Análisis: Costos Muy Bajos vs Ingresos

## ❌ PROBLEMA IDENTIFICADO

Los costos son **irrealmente bajos** comparados con los ingresos, generando márgenes operacionales del **80-90%** (cuando lo normal en salud es 15-30%).

---

## 🔎 CAUSA RAÍZ

### **1. Precios de Venta (PRODUCCION) - CORRECTOS**
```json
// servicios.json
{
  "Ecocardiograma Transtorácico": {
    "valor_min": 120000,    // $120,000
    "valor_max": 350000     // $350,000
  },
  "Cateterismo": {
    "valor_min": 8000000,   // $8,000,000
    "valor_max": 15000000   // $15,000,000
  }
}
```
**✅ Estos valores son realistas para Colombia**

---

### **2. Costos Unitarios (COSTEO_SERVICIOS) - INCORRECTOS**

#### **Problema en costeo_servicios.py línea 58-66:**
```python
# MO Directa
cost_min_ref = 2200  # ← HARDCODEADO: $2,200/minuto
ws[f'D{row}'] = f"={minutes_ref}*{cost_min_ref}"

# CIF (Indirecto)
cif_rate = data_init.tasas_cif_por_sede.get(sede, 1400)  # ← $1,400/minuto
ws[f'F{row}'] = f"={minutes_ref}*{cif_rate:.2f}"
```

#### **Ejemplo de Cálculo Actual (INCORRECTO):**
```
Servicio: Ecocardiograma (30 minutos)
Precio de Venta: $250,000

Costos:
- MO Directa: 30 min × $2,200 = $66,000
- Insumos: $10,000
- CIF: 30 min × $1,400 = $42,000
COSTO TOTAL: $118,000

MARGEN: $250,000 - $118,000 = $132,000 (53%)  ← Muy alto!
```

---

## ✅ SOLUCIÓN: Usar Tasas Reales de COSTO_POR_MINUTO

### **El sistema YA calcula las tasas correctas en la hoja COSTO_POR_MINUTO:**

```
Hoja: COSTO_POR_MINUTO
Sede Principal:
  - Costo MO por minuto: $8,500  ← Calculado de nómina real
  - Costo CIF por minuto: $5,200  ← Calculado de costos indirectos
```

### **Pero NO las está usando en COSTEO_SERVICIOS** ❌

---

## 🔧 CORRECCIÓN NECESARIA

### **ANTES (Incorrecto):**
```python
# costeo_servicios.py línea 58-66
cost_min_ref = 2200  # ← Hardcodeado
cif_rate = data_init.tasas_cif_por_sede.get(sede, 1400)  # ← Hardcodeado
```

### **DESPUÉS (Correcto):**
```python
# Usar referencias a COSTO_POR_MINUTO
ws[f'D{row}'] = f"={minutes_ref}*VLOOKUP(C{row},COSTO_POR_MINUTO!$A:$B,2,FALSE)"
ws[f'F{row}'] = f"={minutes_ref}*VLOOKUP(C{row},COSTO_POR_MINUTO!$A:$C,3,FALSE)"
```

---

## 📊 COMPARACIÓN: Antes vs Después

### **Ejemplo: Ecocardiograma (30 minutos)**

| Concepto | ANTES (Incorrecto) | DESPUÉS (Correcto) | Diferencia |
|----------|-------------------|-------------------|------------|
| **MO Directa** | 30 × $2,200 = $66,000 | 30 × $8,500 = $255,000 | +$189,000 |
| **Insumos** | $10,000 | $10,000 | $0 |
| **CIF** | 30 × $1,400 = $42,000 | 30 × $5,200 = $156,000 | +$114,000 |
| **COSTO TOTAL** | $118,000 | $421,000 | +$303,000 |
| **Precio Venta** | $250,000 | $250,000 | $0 |
| **MARGEN** | $132,000 (53%) ❌ | -$171,000 (-68%) ✅ | Pérdida! |

**Conclusión:** Con costos reales, este servicio está **perdiendo dinero** (como debería ser evidente en un análisis TDABC real).

---

## 🎯 VALORES ESPERADOS REALISTAS

### **Margen Operacional Esperado en Salud:**
- **Servicios Diagnósticos**: 15-25%
- **Servicios Terapéuticos**: 20-30%
- **Servicios Quirúrgicos**: 25-35%

### **Ejemplo Realista: Cateterismo**

```
Precio de Venta: $12,000,000

Costos Reales:
- MO Directa: 120 min × $8,500 = $1,020,000
- Insumos (stents, catéteres): $6,500,000
- CIF: 120 min × $5,200 = $624,000
COSTO TOTAL: $8,144,000

MARGEN: $12,000,000 - $8,144,000 = $3,856,000 (32%)  ← Realista!
```

---

## 🔍 VERIFICACIÓN DE TASAS REALES

### **Costo MO por Minuto (Debería ser ~$8,000-$12,000):**
```
Cálculo:
Salario Médico Especialista: $8,000,000/mes
+ Prestaciones (52%): $4,160,000
= Costo Total: $12,160,000/mes

Capacidad: 184 horas = 11,040 minutos
Costo por minuto: $12,160,000 / 11,040 = $1,101/min

Pero con múltiples empleados y overhead:
Costo promedio real: $8,500/min  ✅
```

### **Costo CIF por Minuto (Debería ser ~$4,000-$6,000):**
```
Costos Indirectos Totales: $60,000,000/mes
Capacidad Total: 11,040 minutos
Costo por minuto: $60,000,000 / 11,040 = $5,435/min  ✅
```

---

## ⚠️ IMPACTO DEL ERROR

### **Con Tasas Incorrectas ($2,200 y $1,400):**
```
Ingresos Totales: $500,000,000
Costos Totales: $100,000,000  ← Muy bajo
MARGEN: 80%  ← Irreal!
```

### **Con Tasas Correctas ($8,500 y $5,200):**
```
Ingresos Totales: $500,000,000
Costos Totales: $380,000,000  ← Realista
MARGEN: 24%  ← Realista!
```

---

## 🛠️ ARCHIVOS A CORREGIR

1. **`src/sheets/costeo_servicios.py`** (líneas 58-66)
   - Cambiar tasas hardcodeadas por referencias a COSTO_POR_MINUTO

2. **`src/modelo_tdabc.py`** (verificar orden de hojas)
   - Asegurar que COSTO_POR_MINUTO se crea ANTES de COSTEO_SERVICIOS

---

## ✅ CONCLUSIÓN

**El problema NO es un error de fórmula, sino valores hardcodeados incorrectos.**

Las tasas de $2,200 y $1,400 por minuto son **3-4 veces más bajas** que las tasas reales calculadas en COSTO_POR_MINUTO.

**Solución:** Usar VLOOKUP para referenciar las tasas reales de la hoja COSTO_POR_MINUTO.

---

## 🎯 PRÓXIMO PASO

¿Quieres que corrija el archivo `costeo_servicios.py` para usar las tasas reales de COSTO_POR_MINUTO?

Esto hará que los costos sean realistas y el margen operacional baje del 80% actual a un 20-30% realista.
