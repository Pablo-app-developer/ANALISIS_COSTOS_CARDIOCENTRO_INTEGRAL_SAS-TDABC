# 📚 Índice de Documentación - Modelo TDABC

## 🎯 Guía Rápida de Navegación

Este proyecto contiene documentación completa sobre el sistema TDABC modular. Use este índice para encontrar rápidamente la información que necesita.

---

## 📄 Archivos de Documentación

### 1. **README.md** - Documentación Principal
**Propósito**: Introducción general al proyecto
**Audiencia**: Todos los usuarios
**Contenido**:
- Descripción del proyecto
- Estructura modular completa
- Instrucciones de instalación
- Guía de uso básico
- Hojas generadas
- Ventajas de la versión modular
- Personalización básica

**📖 Leer cuando**: Es tu primera vez con el proyecto

---

### 2. **RESUMEN.md** - Resumen Ejecutivo
**Propósito**: Vista general de la transformación
**Audiencia**: Gerentes, líderes técnicos
**Contenido**:
- Estadísticas del proyecto
- Estructura final completa
- Módulos creados
- Beneficios logrados
- Checklist de funcionalidades
- Métricas de calidad

**📖 Leer cuando**: Necesitas una vista rápida del proyecto completo

---

### 3. **MIGRACION.md** - Guía de Migración
**Propósito**: Documentar la transformación de monolítico a modular
**Audiencia**: Desarrolladores, arquitectos
**Contenido**:
- Comparación antes/después
- Mapeo de funcionalidades
- Cambios principales en el código
- Cómo usar la nueva versión
- Verificación de equivalencia
- Próximos pasos recomendados

**📖 Leer cuando**: Quieres entender cómo se hizo la migración

---

### 4. **ARQUITECTURA.md** - Documentación de Arquitectura
**Propósito**: Explicar la arquitectura técnica del sistema
**Audiencia**: Desarrolladores, arquitectos de software
**Contenido**:
- Diagramas de arquitectura
- Flujo de ejecución detallado
- Dependencias entre módulos
- Matriz de responsabilidades
- Patrones de diseño aplicados
- Principios SOLID
- Guías de escalabilidad

**📖 Leer cuando**: Necesitas entender la arquitectura técnica

---

### 5. **INDICE.md** - Este Archivo
**Propósito**: Navegación entre documentos
**Audiencia**: Todos
**Contenido**:
- Índice de toda la documentación
- Guías de uso por rol
- Casos de uso comunes

**📖 Leer cuando**: No sabes por dónde empezar

---

## 👥 Guías por Rol

### 🎓 Nuevo Usuario
**Ruta de aprendizaje recomendada**:
1. **README.md** → Entender qué es el proyecto
2. **RESUMEN.md** → Ver estructura general
3. Ejecutar `python main.py` → Ver el resultado
4. **ARQUITECTURA.md** → Entender cómo funciona

### 💼 Gerente / Líder Técnico
**Documentos clave**:
1. **RESUMEN.md** → Métricas y beneficios
2. **MIGRACION.md** → Cambios realizados
3. **README.md** → Capacidades del sistema

### 👨‍💻 Desarrollador Nuevo
**Ruta de aprendizaje**:
1. **README.md** → Setup inicial
2. **ARQUITECTURA.md** → Entender la arquitectura
3. **MIGRACION.md** → Ver ejemplos de código
4. Explorar `src/` → Revisar código fuente

### 🏗️ Arquitecto de Software
**Documentos técnicos**:
1. **ARQUITECTURA.md** → Diseño completo
2. **MIGRACION.md** → Decisiones de diseño
3. Código fuente en `src/` → Implementación

### 🔧 Mantenedor del Proyecto
**Documentos de referencia**:
1. **ARQUITECTURA.md** → Cómo está organizado
2. **README.md** → Personalización
3. **MIGRACION.md** → Próximos pasos

---

## 🎯 Casos de Uso Comunes

### Caso 1: Quiero ejecutar el programa
**Documentos**: README.md (sección "Uso")
```bash
python main.py
```

### Caso 2: Quiero agregar un nuevo servicio
**Documentos**: README.md (sección "Personalización")
1. Editar `src/config.py` → Agregar a `SERVICIOS`
2. Editar `src/data/ecuaciones_data.py` → Agregar ecuación
3. Editar `src/data/insumos_data.py` → Agregar insumos (si aplica)

### Caso 3: Quiero agregar una nueva hoja Excel
**Documentos**: ARQUITECTURA.md (sección "Escalabilidad")
1. Crear `src/sheets/nueva_hoja.py`
2. Implementar `crear_hoja_nueva(wb)`
3. Importar en `src/modelo_tdabc.py`
4. Llamar en `generar_archivo()`

### Caso 4: Quiero modificar los colores corporativos
**Documentos**: README.md (sección "Estilos y Colores")
1. Editar `src/config.py`
2. Modificar variables `COLOR_*`

### Caso 5: Quiero entender cómo funciona internamente
**Documentos**: ARQUITECTURA.md (completo)
- Ver diagramas de flujo
- Revisar dependencias
- Entender patrones de diseño

### Caso 6: Quiero comparar con la versión original
**Documentos**: MIGRACION.md (sección "Comparación")
- Ver tabla de mapeo
- Comparar estructuras
- Verificar equivalencia

---

## 📊 Estructura de Archivos del Proyecto

```
ANALISIS_COSTOS_CARDIOCENTRO_INTEGRAL_SAS-TDABC-main/
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md              ← Documentación principal
│   ├── RESUMEN.md             ← Resumen ejecutivo
│   ├── MIGRACION.md           ← Guía de migración
│   ├── ARQUITECTURA.md        ← Arquitectura técnica
│   └── INDICE.md              ← Este archivo
│
├── 🚀 EJECUTABLES
│   ├── main.py                ← Versión modular (USAR ESTE)
│   └── generar_modelo_tdabc.py ← Versión original (LEGACY)
│
├── ⚙️ CONFIGURACIÓN
│   └── requirements.txt       ← Dependencias
│
├── 📊 SALIDA
│   └── Modelo_TDABC_CardioCentro.xlsx ← Archivo generado
│
└── 💻 CÓDIGO FUENTE
    └── src/                   ← Todo el código modular
        ├── config.py
        ├── styles.py
        ├── utils.py
        ├── data_initializer.py
        ├── modelo_tdabc.py
        ├── data/
        │   ├── ecuaciones_data.py
        │   └── insumos_data.py
        └── sheets/
            ├── parametros.py
            ├── nomina.py
            ├── capacidad.py
            ├── costo_por_minuto.py
            ├── servicios.py
            ├── ecuaciones_tiempo.py
            ├── insumos.py
            ├── produccion.py
            ├── costos_indirectos.py
            ├── costeo_servicios.py
            └── resumen_ejecutivo.py
```

---

## 🔍 Búsqueda Rápida

### Busco información sobre...

| Tema | Documento | Sección |
|------|-----------|---------|
| Instalación | README.md | "Instalación" |
| Ejecución | README.md | "Uso" |
| Estructura del proyecto | RESUMEN.md | "Estructura Final" |
| Módulos creados | RESUMEN.md | "Módulos Creados" |
| Beneficios | RESUMEN.md | "Beneficios Logrados" |
| Comparación antes/después | MIGRACION.md | "Comparación de Estructuras" |
| Cómo se migró | MIGRACION.md | "Cambios Principales" |
| Arquitectura | ARQUITECTURA.md | Todo el documento |
| Flujo de ejecución | ARQUITECTURA.md | "Flujo de Ejecución" |
| Dependencias | ARQUITECTURA.md | "Dependencias entre Módulos" |
| Patrones de diseño | ARQUITECTURA.md | "Patrón de Diseño" |
| Agregar funcionalidad | ARQUITECTURA.md | "Escalabilidad" |
| Personalizar servicios | README.md | "Personalización" |
| Personalizar colores | README.md | "Estilos y Colores" |
| Próximos pasos | MIGRACION.md | "Próximos Pasos" |

---

## 📞 Contacto y Soporte

Para preguntas adicionales o soporte técnico, contactar al equipo de desarrollo de **CardioCentro Diagnóstico Integral S.A.S.**

---

## 📌 Notas Importantes

⚠️ **Versión Recomendada**: Usar `python main.py` (versión modular)

⚠️ **Compatibilidad**: La versión modular genera exactamente el mismo archivo Excel que la original

⚠️ **Mantenimiento**: El archivo `generar_modelo_tdabc.py` se mantiene solo por compatibilidad legacy

---

**Última actualización**: Febrero 2026
**Versión de documentación**: 1.0.0
**Estado**: ✅ Completo
