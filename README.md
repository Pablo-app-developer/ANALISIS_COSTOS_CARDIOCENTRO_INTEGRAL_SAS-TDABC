# Sistema TDABC Genérico - Documentación Completa

## 📋 Descripción

Sistema genérico de **Time-Driven Activity-Based Costing (TDABC)** adaptable a cualquier empresa del sector salud (y otros sectores) mediante configuración JSON, sin necesidad de modificar código Python.

## ✨ Características Principales

### ✅ **100% Parametrizable**
- Configuración completa vía archivos JSON
- Sin lógica de negocio hardcodeada
- Adaptable a diferentes sectores (salud, educación, manufactura)

### ✅ **Arquitectura Modular**
- Separación de lógica de datos y presentación
- Generadores de datos testeables
- Fácil mantenimiento y extensión

### ✅ **Validación Automática**
- Validación de configuraciones antes de generar modelo
- Reportes detallados de errores y advertencias
- Plantillas predefinidas por sector

---

## 🚀 Inicio Rápido

### Para CardioCentro (Cliente Actual)
```bash
python main.py
```
Genera: `Modelo_TDABC_CardioCentro.xlsx`

### Para Nueva Empresa

#### Opción 1: Usar Plantilla Predefinida
```python
from src.adaptador import AdaptadorEmpresa

# Generar plantilla para tu sector
adaptador = AdaptadorEmpresa()
adaptador.generar_plantilla("mi_empresa.json", sector="salud")
# Sectores disponibles: "salud", "educacion", "manufactura"
```

#### Opción 2: Adaptar Directamente
```python
from src.adaptador import adaptar_empresa

# 1. Edita el archivo JSON generado con tus datos
# 2. Ejecuta la adaptación
adaptar_empresa("mi_empresa.json")

# 3. Genera el modelo TDABC
# python main.py
```

---

## 📁 Estructura del Proyecto

```
ANALISIS_COSTOS_CARDIOCENTRO_INTEGRAL_SAS-TDABC-main/
│
├── src/
│   ├── config/                    # Configuraciones JSON
│   │   ├── empresa_config.json    # Datos de la empresa
│   │   ├── servicios.json         # Catálogo de servicios
│   │   ├── centros_costo.json     # Centros de costo/sedes
│   │   ├── plan_contable.json     # Plan contable
│   │   ├── grupos_ocupacionales.json
│   │   └── mapeo_columnas.json    # Mapeo de columnas Excel
│   │
│   ├── generators/                # Generadores de datos (lógica pura)
│   │   ├── servicios_generator.py
│   │   └── produccion_generator.py
│   │
│   ├── sheets/                    # Generadores de hojas Excel
│   │   ├── parametros.py
│   │   ├── nomina.py
│   │   ├── servicios.py
│   │   ├── produccion.py
│   │   └── ...
│   │
│   ├── adaptador.py               # Adaptador genérico ⭐
│   ├── mapper.py                  # Capa de mapeo
│   ├── config.py                  # Configuración central
│   └── modelo_tdabc.py            # Orquestador principal
│
├── tests/
│   └── test_generators.py        # Tests unitarios
│
├── ejemplos/                      # Plantillas de ejemplo
│   ├── clinica_dental.json
│   ├── instituto_educativo.json
│   └── fabrica.json
│
├── main.py                        # Punto de entrada
└── README.md                      # Este archivo
```

---

## 🔧 Configuración de Nueva Empresa

### Estructura del Archivo JSON

```json
{
  "empresa": {
    "nombre_empresa": "Mi Clínica S.A.S.",
    "nit": "900123456-7",
    "sector": "salud",
    "pais": "Colombia",
    "ciudad": "Bogotá"
  },
  "servicios": [
    {
      "codigo": "SV001",
      "nombre": "Consulta General",
      "categoria": "Consulta Externa",
      "complejidad": "Baja",
      "requiere_insumos": false,
      "volumen_min": 50,
      "volumen_max": 100,
      "valor_min": 50000,
      "valor_max": 80000
    }
  ],
  "categorias": {
    "Consulta Externa": {
      "descripcion": "Consultas médicas ambulatorias",
      "complejidad_base": "Baja",
      "requiere_insumos_default": false,
      "volumen_min_default": 40,
      "volumen_max_default": 100
    }
  },
  "centros": [
    {
      "nombre": "Sede Principal",
      "ciudad": "Bogotá",
      "salas": 3
    }
  ],
  "grupos_ocupacionales": [
    ["Médico General", 8000000],
    ["Enfermera", 3000000]
  ]
}
```

### Campos Requeridos

#### Empresa
- `nombre_empresa` (string): Nombre de la empresa
- `nit` (string): NIT o identificación fiscal
- `sector` (string): Sector económico
- `pais` (string): País de operación

#### Servicios
- `codigo` (string): Código único del servicio
- `nombre` (string): Nombre del servicio
- `categoria` (string): Categoría del servicio

#### Campos Opcionales (con defaults)
- `complejidad`: Se usa `complejidad_base` de la categoría
- `requiere_insumos`: Se usa `requiere_insumos_default` de la categoría
- `volumen_min/max`: Se usan `volumen_min/max_default` de la categoría
- `valor_min/max`: Valores por defecto del sistema

---

## 🧪 Testing

### Ejecutar Tests Unitarios
```bash
python -m unittest tests.test_generators -v
```

### Tests Disponibles
- ✅ Generación de servicios con datos completos
- ✅ Uso de defaults de categoría
- ✅ Generación de producción con rangos correctos
- ✅ Validación de estructura de datos

---

## 📊 Salida del Sistema

El sistema genera un archivo Excel con 11 hojas:

1. **PARAMETROS** - Configuración general
2. **NOMINA** - Estructura salarial
3. **CAPACIDAD** - Capacidad práctica (184h/mes)
4. **COSTO_POR_MINUTO** - Núcleo TDABC
5. **SERVICIOS** - Catálogo de servicios
6. **ECUACIONES_TIEMPO** - Ecuaciones TDABC por servicio
7. **INSUMOS** - Costos de materiales
8. **COSTOS_INDIRECTOS** - Costos administrativos
9. **PRODUCCION** - Volúmenes y facturación
10. **COSTEO_SERVICIOS** - Costo total por servicio
11. **RESUMEN_EJECUTIVO** - Dashboard de rentabilidad

---

## 🎯 Casos de Uso

### Caso 1: Clínica Dental
```python
from src.adaptador import AdaptadorEmpresa

adaptador = AdaptadorEmpresa()
adaptador.generar_plantilla("clinica_dental.json", "salud")

# Editar clinica_dental.json con servicios odontológicos:
# - Limpieza Dental
# - Endodoncia
# - Ortodoncia
# etc.

from src.adaptador import adaptar_empresa
adaptar_empresa("clinica_dental.json")
```

### Caso 2: Instituto Educativo
```python
adaptador.generar_plantilla("instituto.json", "educacion")

# Editar con cursos/programas:
# - Curso Básico
# - Diplomado
# - Especialización
# etc.

adaptar_empresa("instituto.json")
```

### Caso 3: Fábrica
```python
adaptador.generar_plantilla("fabrica.json", "manufactura")

# Editar con productos:
# - Producto Estándar
# - Producto Premium
# - Producto Custom
# etc.

adaptar_empresa("fabrica.json")
```

---

## 🔄 Proceso de Refactorización (Fases Completadas)

### ✅ FASE 1: Detectar Rigidez
- Análisis completo de dependencias hardcodeadas
- Identificación de 10 categorías de rigidez
- Nivel de rigidez: CRÍTICO

### ✅ FASE 2: Crear Capa de Mapeo
- Archivos JSON de configuración
- Clase `ConfigMapper`
- Compatibilidad 100% con sistema original

### ✅ FASE 3: Desacoplar Motor TDABC
- Headers dinámicos desde `mapeo_columnas.json`
- Formato interno estandarizado (`df_std`)
- Motor TDABC independiente de nombres de columnas

### ✅ FASE 4: Parametrizar Servicios
- Lógica condicional → Configuración JSON
- Complejidad, volúmenes, insumos parametrizados
- Sin `if/elif` hardcodeados

### ✅ FASE 5: Separar Flujo en Funciones
- Directorio `generators/` para lógica pura
- Separación datos vs presentación
- Tests unitarios (6 tests, 100% pass)

### ✅ FASE 6: Crear Adaptador Genérico
- Función `adaptar_empresa(config_json)`
- Validación automática de configuraciones
- Plantillas por sector
- Generación automática de archivos de configuración

---

## 📈 Métricas del Proyecto

- **Líneas de código refactorizadas**: ~2,000
- **Archivos de configuración**: 6 JSON
- **Generadores modulares**: 2
- **Tests unitarios**: 6 (100% pass)
- **Compatibilidad**: 100% con sistema original
- **Sectores soportados**: 3 (salud, educación, manufactura)
- **Tiempo de adaptación**: < 5 minutos con plantilla

---

## 🛠️ Requisitos

- Python 3.11+
- openpyxl
- pathlib (incluido en Python 3.4+)

### Instalación
```bash
pip install openpyxl
```

---

## 📝 Licencia

Proyecto desarrollado para CardioCentro Diagnóstico Integral S.A.S.

---

## 👥 Soporte

Para adaptar el sistema a tu empresa:
1. Genera una plantilla con `adaptador.generar_plantilla()`
2. Edita el JSON con los datos de tu empresa
3. Ejecuta `adaptar_empresa('tu_config.json')`
4. Genera el modelo con `python main.py`

**¿Problemas?** El adaptador genera reportes detallados de validación con errores y advertencias específicas.

---

## 🎉 Resultado Final

**Sistema TDABC 100% genérico y adaptable** que permite a cualquier empresa del sector salud (y otros sectores) generar su modelo de costeo basado en actividades sin modificar una sola línea de código Python.

**De hardcodeado a configurable en 6 fases. ✅**
