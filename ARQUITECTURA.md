# Arquitectura del Sistema TDABC Modular

## 📐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                  │
│                    (Punto de Entrada)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   src/modelo_tdabc.py                            │
│                   (Orquestador Principal)                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  1. Inicializar Workbook                               │    │
│  │  2. Crear DataInitializer                              │    │
│  │  3. Generar todas las hojas en orden                   │    │
│  │  4. Guardar archivo Excel                              │    │
│  └────────────────────────────────────────────────────────┘    │
└───┬──────────┬──────────┬──────────┬──────────┬────────────────┘
    │          │          │          │          │
    ▼          ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌─────────────┐
│config  │ │styles  │ │utils   │ │data_   │ │sheets/      │
│.py     │ │.py     │ │.py     │ │init.py │ │(11 módulos) │
└────────┘ └────────┘ └────────┘ └────────┘ └─────────────┘
    │          │          │          │              │
    │          │          │          │              │
    ▼          ▼          ▼          ▼              ▼
┌──────────────────────────────────────────────────────────┐
│                  Datos y Configuración                    │
├──────────────────────────────────────────────────────────┤
│ • Constantes (SEDES, SERVICIOS, etc.)                    │
│ • Colores corporativos                                    │
│ • Grupos ocupacionales                                    │
│ • Presupuesto de costos indirectos                       │
│ • Ecuaciones de tiempo (data/ecuaciones_data.py)         │
│ • Insumos por servicio (data/insumos_data.py)            │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│              Generadores de Hojas Excel                   │
├──────────────────────────────────────────────────────────┤
│  1. PARAMETROS      → Configuración general              │
│  2. NOMINA          → Estructura salarial                │
│  3. CAPACIDAD       → Capacidad práctica                 │
│  4. COSTO_POR_MIN   → Costo por minuto (TDABC)          │
│  5. SERVICIOS       → Catálogo de servicios              │
│  6. ECUACIONES      → Ecuaciones de tiempo               │
│  7. INSUMOS         → Costos de materiales               │
│  8. PRODUCCION      → Volúmenes y facturación            │
│  9. COSTEO          → Costeo unitario                    │
│ 10. COSTOS_IND      → Auxiliar contable                  │
│ 11. RESUMEN_EJEC    → Dashboard de rentabilidad          │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│           Modelo_TDABC_CardioCentro.xlsx                  │
│              (Archivo Excel Generado)                     │
└──────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Ejecución

```
1. Usuario ejecuta: python main.py
                         │
                         ▼
2. main.py crea instancia de ModeloTDABC()
                         │
                         ▼
3. ModeloTDABC.__init__()
   ├─ Crea Workbook vacío
   └─ Inicializa DataInitializer
                         │
                         ▼
4. DataInitializer calcula:
   ├─ Distribución de costos indirectos por sede
   ├─ Tasas CIF por sede
   └─ Capacidad mensual por sede
                         │
                         ▼
5. modelo.generar_archivo()
   │
   ├─ sheets/parametros.crear_hoja_parametros(wb)
   │   └─ Lee: config.SEDES, config.GRUPOS_OCUPACIONALES
   │
   ├─ sheets/nomina.crear_hoja_nomina(wb)
   │   └─ Lee: config.GRUPOS_OCUPACIONALES, config.SEDES
   │
   ├─ sheets/capacidad.crear_hoja_capacidad(wb)
   │   └─ Lee: config.GRUPOS_OCUPACIONALES
   │
   ├─ sheets/costo_por_minuto.crear_hoja_costo_por_minuto(wb)
   │   └─ Lee: config.GRUPOS_OCUPACIONALES, config.SEDES
   │
   ├─ sheets/servicios.crear_hoja_servicios(wb)
   │   └─ Lee: config.SERVICIOS, config.CATEGORIAS
   │
   ├─ sheets/ecuaciones_tiempo.crear_hoja_ecuaciones_tiempo(wb)
   │   └─ Lee: data/ecuaciones_data.ECUACIONES_SERVICIOS
   │
   ├─ sheets/insumos.crear_hoja_insumos(wb)
   │   └─ Lee: data/insumos_data.INSUMOS_POR_SERVICIO
   │
   ├─ sheets/produccion.crear_hoja_produccion(wb)
   │   └─ Lee: config.SERVICIOS, config.SEDES, config.ASEGURADORAS
   │
   ├─ sheets/costeo_servicios.crear_hoja_costeo_servicios(wb, data_init)
   │   └─ Usa: data_init.tasas_cif_por_sede
   │
   ├─ sheets/costos_indirectos.crear_hoja_costos_indirectos(wb, data_init)
   │   └─ Usa: data_init.presupuesto_indirectos, data_init.salas_por_sede
   │
   └─ sheets/resumen_ejecutivo.crear_hoja_resumen_ejecutivo(wb)
       └─ Lee datos de todas las hojas anteriores
                         │
                         ▼
6. wb.save("Modelo_TDABC_CardioCentro.xlsx")
                         │
                         ▼
7. Archivo Excel generado exitosamente
```

## 🧩 Dependencias entre Módulos

```
main.py
  └─ modelo_tdabc.py
      ├─ data_initializer.py
      │   └─ config.py
      │
      ├─ sheets/parametros.py
      │   ├─ config.py
      │   └─ styles.py
      │
      ├─ sheets/nomina.py
      │   ├─ config.py
      │   └─ styles.py
      │
      ├─ sheets/capacidad.py
      │   ├─ config.py
      │   └─ styles.py
      │
      ├─ sheets/costo_por_minuto.py
      │   ├─ config.py
      │   └─ styles.py
      │
      ├─ sheets/servicios.py
      │   ├─ config.py
      │   └─ styles.py
      │
      ├─ sheets/ecuaciones_tiempo.py
      │   ├─ config.py
      │   ├─ styles.py
      │   └─ data/ecuaciones_data.py
      │
      ├─ sheets/insumos.py
      │   ├─ config.py
      │   ├─ styles.py
      │   └─ data/insumos_data.py
      │
      ├─ sheets/produccion.py
      │   ├─ config.py
      │   ├─ styles.py
      │   └─ utils.py
      │
      ├─ sheets/costos_indirectos.py
      │   ├─ config.py
      │   ├─ styles.py
      │   ├─ utils.py
      │   └─ data_initializer.py
      │
      ├─ sheets/costeo_servicios.py
      │   ├─ config.py
      │   ├─ styles.py
      │   ├─ utils.py
      │   └─ data_initializer.py
      │
      └─ sheets/resumen_ejecutivo.py
          ├─ config.py
          └─ styles.py
```

## 📊 Matriz de Responsabilidades

| Módulo | Responsabilidad | Depende de | Usado por |
|--------|----------------|------------|-----------|
| **config.py** | Constantes y configuración | - | Todos |
| **styles.py** | Estilos Excel | config.py | Todos los sheets |
| **utils.py** | Utilidades generales | - | sheets con tablas |
| **data_initializer.py** | Cálculos financieros | config.py | modelo_tdabc, costos_indirectos, costeo_servicios |
| **data/ecuaciones_data.py** | Ecuaciones TDABC | - | ecuaciones_tiempo |
| **data/insumos_data.py** | Insumos por servicio | - | insumos |
| **modelo_tdabc.py** | Orquestación | Todos | main.py |
| **sheets/*.py** | Generación de hojas | config, styles, utils | modelo_tdabc |
| **main.py** | Punto de entrada | modelo_tdabc | Usuario |

## 🎯 Patrón de Diseño Aplicado

### **Patrón: Builder + Strategy**

```
Builder Pattern:
  ModeloTDABC actúa como Director
  Cada sheet/*.py es un Builder concreto
  
Strategy Pattern:
  Cada generador de hoja implementa la misma interfaz
  crear_hoja_X(wb) → Estrategia intercambiable
```

## 🔐 Principios SOLID Aplicados

1. **S - Single Responsibility**
   - Cada módulo tiene una única responsabilidad
   - config.py → Solo configuración
   - styles.py → Solo estilos
   - Cada sheet → Solo una hoja

2. **O - Open/Closed**
   - Fácil agregar nuevas hojas sin modificar existentes
   - Extender configuración sin cambiar lógica

3. **L - Liskov Substitution**
   - Todos los generadores de hojas son intercambiables
   - Misma firma: crear_hoja_X(wb)

4. **I - Interface Segregation**
   - Interfaces pequeñas y específicas
   - No se fuerza a implementar métodos innecesarios

5. **D - Dependency Inversion**
   - Módulos de alto nivel no dependen de bajo nivel
   - Ambos dependen de abstracciones (config)

## 📈 Escalabilidad

### Agregar Nueva Hoja

```python
# 1. Crear src/sheets/nueva_hoja.py
def crear_hoja_nueva(wb):
    ws = wb.create_sheet("NUEVA_HOJA")
    # ... implementación

# 2. Importar en src/modelo_tdabc.py
from .sheets import nueva_hoja

# 3. Llamar en generar_archivo()
print("[OK] Creando hoja NUEVA_HOJA...")
nueva_hoja.crear_hoja_nueva(self.wb)
```

### Modificar Configuración

```python
# Editar src/config.py
NUEVO_PARAMETRO = "valor"

# Usar en cualquier módulo
from .. import config
valor = config.NUEVO_PARAMETRO
```

## 🎨 Convenciones de Código

1. **Nombres de archivos**: snake_case
2. **Nombres de funciones**: snake_case
3. **Nombres de constantes**: UPPER_CASE
4. **Nombres de clases**: PascalCase
5. **Imports relativos**: Usar `from .. import`
6. **Docstrings**: Obligatorios en funciones públicas

---

**Arquitectura diseñada para**: Mantenibilidad, Escalabilidad, Testabilidad
