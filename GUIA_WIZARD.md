# 🧙 Guía del Wizard Interactivo TDABC

## 📋 Descripción

El **Wizard Interactivo** es un asistente CLI que te guía paso a paso para configurar el sistema TDABC sin necesidad de editar archivos JSON manualmente.

---

## 🚀 Cómo Usar el Wizard

### Opción 1: Ejecución Directa
```bash
python wizard_config.py
```

### Opción 2: Como Módulo
```bash
python -m wizard_config
```

---

## 📝 Pasos del Wizard

El wizard te guiará a través de **7 pasos**:

### **Paso 1: Información de la Empresa** (1/7)
```
📋 Información Básica de la Empresa

Nombre de la empresa: Mi Clínica S.A.S.
NIT/RUC/RFC: 900123456-7
Sector de la empresa:
  1. Salud
  2. Educación
  3. Manufactura
  4. Servicios
  5. Otro
Selección: 1
País [Colombia]: 
Ciudad: Bucaramanga
Email de contacto: contacto@miclinica.com

✅ Información de empresa guardada
```

**Validaciones:**
- ✅ Nombre: 3-100 caracteres
- ✅ Email: Formato válido
- ✅ Todos los campos obligatorios

---

### **Paso 2: Parámetros TDABC** (2/7)
```
⚙️ Configuración de Parámetros TDABC

📅 Tiempo de Trabajo:
Días laborales por mes [23]: 23
Horas por día [8]: 8

  ✓ Total: 184 horas/mes (11040 minutos)

💰 Prestaciones Sociales:
¿Usar tasas de Colombia (52.05%)? (S/N) [S]: S

  ✓ Tasa de prestaciones: 52.05%

💵 Formato de Moneda:
Símbolo de moneda [$]: $

✅ Parámetros TDABC configurados
```

**Validaciones:**
- ✅ Días: 20-31
- ✅ Horas: 4-12
- ✅ Tasa prestaciones: 0-1 (0%-100%)

---

### **Paso 3: Centros de Costo** (3/7)
```
🏢 Configuración de Centros de Costo

Ingresa los centros de costo de tu empresa.
(Presiona Enter sin texto para terminar)

Centro de costo #1: Consulta Externa
  ✓ Agregado: CC001 - Consulta Externa
Centro de costo #2: Hospitalización
  ✓ Agregado: CC002 - Hospitalización
Centro de costo #3: Urgencias
  ✓ Agregado: CC003 - Urgencias
Centro de costo #4: [Enter]

✅ 3 centros de costo configurados
```

**Validaciones:**
- ✅ Mínimo 1 centro de costo
- ✅ Códigos auto-generados (CC001, CC002, ...)

---

### **Paso 4: Servicios** (4/7)
```
🔧 Configuración de Servicios

¿Importar servicios desde un archivo Excel? (S/N) [N]: N

Ingresa los servicios que ofreces.
(Presiona Enter sin texto para terminar)

Servicio #1: Ecocardiograma
Categoría de 'Ecocardiograma':
  1. Diagnóstico
  2. Terapéutico
  3. Quirúrgico
  4. Consulta
  5. Otro
Selección: 1
  ✓ Agregado: SV001 - Ecocardiograma (Diagnóstico)

Servicio #2: Cateterismo
Categoría de 'Cateterismo':
Selección: 3
  ✓ Agregado: SV002 - Cateterismo (Quirúrgico)

Servicio #3: [Enter]

✅ 2 servicios configurados
```

**Validaciones:**
- ✅ Mínimo 1 servicio
- ✅ Categoría obligatoria
- ✅ Códigos auto-generados (SV001, SV002, ...)

---

### **Paso 5: Sedes** (5/7)
```
📍 Configuración de Sedes

Ingresa las sedes/sucursales de tu empresa.
(Presiona Enter sin texto para terminar)

Sede #1: Sede Principal
  ✓ Agregado: Sede Principal
Sede #2: Sede Norte
  ✓ Agregado: Sede Norte
Sede #3: [Enter]

✅ 2 sedes configuradas
```

**Validaciones:**
- ✅ Mínimo 1 sede

---

### **Paso 6: Clientes/Aseguradoras** (6/7)
```
👥 Configuración de Clientes/Aseguradoras

Ingresa tus principales clientes o aseguradoras.
(Presiona Enter sin texto para terminar)

Cliente #1: EPS Sura
  ✓ Agregado: EPS Sura
Cliente #2: Sanitas
  ✓ Agregado: Sanitas
Cliente #3: Nueva EPS
  ✓ Agregado: Nueva EPS
Cliente #4: [Enter]

✅ 3 clientes configurados
```

**Validaciones:**
- ✅ Mínimo 1 cliente

---

### **Paso 7: Hojas del Modelo** (7/7)
```
📊 Configuración de Hojas del Modelo

¿Qué tipo de modelo deseas?
  1. Completo (11 hojas - análisis detallado)
  2. Simplificado (6 hojas - análisis básico)
  3. Personalizado (seleccionar hojas manualmente)

Selección: 2

✅ Modelo configurado con 6 hojas activas
```

**Opciones:**
- **Completo**: Todas las 11 hojas
- **Simplificado**: Solo 6 hojas básicas
- **Personalizado**: Seleccionar una por una

---

## 📊 Resumen Final

```
============================================================
RESUMEN DE CONFIGURACIÓN
============================================================

🏢 Empresa: Mi Clínica S.A.S.
   NIT: 900123456-7
   Sector: Salud
   País: Colombia

⚙️  Parámetros TDABC:
   Horas/mes: 184
   Prestaciones: 52.05%

📊 Elementos Configurados:
   Centros de costo: 3
   Servicios: 2
   Sedes: 2
   Clientes: 3
   Hojas activas: 6

============================================================

¿Guardar esta configuración? (S/N) [S]: S
```

---

## 💾 Archivos Generados

Al finalizar, el wizard crea automáticamente:

```
src/config/
├── empresa_config.json      ✅ Información de empresa, sedes, clientes
├── parametros_tdabc.json    ✅ Parámetros TDABC (horas, prestaciones)
├── centros_costo.json       ✅ Centros de costo
└── servicios.json           ✅ Servicios (si se configuraron manualmente)
```

---

## ✅ Validaciones en Tiempo Real

El wizard valida **automáticamente**:

| Campo | Validación |
|-------|------------|
| **Nombre empresa** | 3-100 caracteres |
| **Email** | Formato válido (usuario@dominio.com) |
| **Días laborales** | 20-31 días |
| **Horas por día** | 4-12 horas |
| **Tasa prestaciones** | 0-100% |
| **Centros de costo** | Mínimo 1 |
| **Servicios** | Mínimo 1 |
| **Sedes** | Mínimo 1 |
| **Clientes** | Mínimo 1 |

---

## 🎯 Ventajas del Wizard

| Característica | Beneficio |
|----------------|-----------|
| **Interactivo** | Guía paso a paso |
| **Validación en tiempo real** | Detecta errores inmediatamente |
| **Sin editar JSON** | No necesitas conocer la estructura |
| **Códigos auto-generados** | CC001, SV001, etc. |
| **Valores por defecto** | Acelera la configuración |
| **Resumen final** | Revisa antes de guardar |
| **Cancelable** | Ctrl+C en cualquier momento |

---

## 🔄 Flujo Completo

```
1. Ejecutar wizard
   └─> python wizard_config.py

2. Seguir 7 pasos
   ├─> Información empresa
   ├─> Parámetros TDABC
   ├─> Centros de costo
   ├─> Servicios
   ├─> Sedes
   ├─> Clientes
   └─> Hojas Excel

3. Revisar resumen
   └─> Confirmar o cancelar

4. Archivos generados
   └─> src/config/*.json

5. Importar datos reales (opcional)
   └─> python -m src.importador_produccion

6. Generar modelo TDABC
   └─> python main.py

7. ¡Listo! 🎉
```

---

## 💡 Consejos de Uso

### ✅ **Recomendaciones:**
1. **Ten a mano**: Lista de servicios, sedes, clientes
2. **Usa valores reales**: Horas laborales, prestaciones de tu país
3. **Empieza simple**: Usa modelo "Simplificado" primero
4. **Revisa el resumen**: Antes de guardar

### ⚠️ **Evita:**
1. ❌ Dejar campos vacíos (todos son obligatorios)
2. ❌ Usar caracteres especiales raros
3. ❌ Ingresar demasiados servicios manualmente (mejor importar)

---

## 🆘 Solución de Problemas

### **Error: "Valor inválido"**
- Verifica que el formato sea correcto
- Ejemplo email: `usuario@dominio.com`
- Ejemplo número: `23` o `0.52`

### **Error: "Este campo es obligatorio"**
- No dejes campos vacíos
- Presiona Enter para usar valor por defecto `[valor]`

### **Cancelar el wizard**
- Presiona `Ctrl+C` en cualquier momento
- Los cambios no se guardan hasta el final

---

## 🎓 Ejemplo Completo

```bash
$ python wizard_config.py

============================================================
  🧙 WIZARD DE CONFIGURACIÓN TDABC
============================================================

Bienvenido al asistente de configuración del sistema TDABC.
Este wizard te guiará paso a paso para configurar tu empresa.

¿Deseas continuar? (S/N) [S]: S

[████████████████████] 100% - Paso 7/7: Hojas del Modelo Excel

============================================================
RESUMEN DE CONFIGURACIÓN
============================================================

🏢 Empresa: Mi Clínica S.A.S.
   NIT: 900123456-7
   Sector: Salud
   País: Colombia

⚙️  Parámetros TDABC:
   Horas/mes: 184
   Prestaciones: 52.05%

📊 Elementos Configurados:
   Centros de costo: 3
   Servicios: 5
   Sedes: 2
   Clientes: 4
   Hojas activas: 6

============================================================

¿Guardar esta configuración? (S/N) [S]: S

💾 Guardando configuración...

  ✓ src/config/empresa_config.json
  ✓ src/config/parametros_tdabc.json
  ✓ src/config/centros_costo.json
  ✓ src/config/servicios.json

✅ Configuración guardada exitosamente!

============================================================
🎉 ¡Configuración completada!
============================================================

Próximos pasos:
  1. Revisa los archivos en src/config/
  2. Importa tus datos reales (opcional):
     python -m src.importador_produccion
  3. Genera tu modelo TDABC:
     python main.py

============================================================
```

---

## 🎉 Resultado

**Antes del wizard:**
- ❌ Editar 4-5 archivos JSON manualmente
- ❌ Conocer estructura exacta
- ❌ Riesgo de errores de sintaxis
- ❌ Validación manual

**Con el wizard:**
- ✅ Interfaz interactiva guiada
- ✅ Validación automática en tiempo real
- ✅ Sin editar JSON
- ✅ Configuración en 5-10 minutos

**¡El wizard reduce la curva de aprendizaje de horas a minutos!** 🚀
