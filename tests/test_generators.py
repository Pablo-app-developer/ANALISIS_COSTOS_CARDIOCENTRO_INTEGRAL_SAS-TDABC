"""
Tests unitarios para generadores de datos.

Estos tests demuestran el beneficio de separar la lógica de negocio
de la presentación: podemos testear la lógica sin necesidad de Excel.
"""
import unittest
from src.generators.servicios_generator import generar_datos_servicios
from src.generators.produccion_generator import generar_datos_produccion


class TestServiciosGenerator(unittest.TestCase):
    """Tests para el generador de servicios"""
    
    def setUp(self):
        """Configuración de datos de prueba"""
        self.servicios_completos = [
            {
                "codigo": "SV001",
                "nombre": "Ecocardiograma Transtorácico",
                "categoria": "Diagnóstico No Invasivo",
                "complejidad": "Media",
                "requiere_insumos": False
            },
            {
                "codigo": "SV002",
                "nombre": "Cateterismo Cardíaco",
                "categoria": "Diagnóstico Invasivo",
                "requiere_insumos": True
                # Sin complejidad explícita - debe usar default
            }
        ]
        
        self.categorias_info = {
            "Diagnóstico No Invasivo": {
                "complejidad_base": "Baja",
                "requiere_insumos_default": False
            },
            "Diagnóstico Invasivo": {
                "complejidad_base": "Alta",
                "requiere_insumos_default": True
            }
        }
    
    def test_generar_servicios_con_datos_completos(self):
        """Test: servicio con todos los datos debe usar sus propios valores"""
        resultado = generar_datos_servicios(self.servicios_completos, self.categorias_info)
        
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['codigo'], 'SV001')
        self.assertEqual(resultado[0]['complejidad'], 'Media')
        self.assertFalse(resultado[0]['requiere_insumos'])
    
    def test_generar_servicios_usa_defaults(self):
        """Test: servicio sin complejidad debe usar default de categoría"""
        resultado = generar_datos_servicios(self.servicios_completos, self.categorias_info)
        
        # SV002 no tiene complejidad, debe usar "Alta" de su categoría
        self.assertEqual(resultado[1]['complejidad'], 'Alta')
        self.assertTrue(resultado[1]['requiere_insumos'])
    
    def test_generar_servicios_estado_activo(self):
        """Test: todos los servicios deben tener estado 'Activo'"""
        resultado = generar_datos_servicios(self.servicios_completos, self.categorias_info)
        
        for servicio in resultado:
            self.assertEqual(servicio['estado'], 'Activo')


class TestProduccionGenerator(unittest.TestCase):
    """Tests para el generador de producción"""
    
    def setUp(self):
        """Configuración de datos de prueba"""
        self.servicios_lista = ["Ecocardiograma", "Cateterismo"]
        self.servicios_dict = {
            "Ecocardiograma": {
                "codigo": "SV001",
                "categoria": "Diagnóstico No Invasivo",
                "volumen_min": 15,
                "volumen_max": 40,
                "valor_min": 120000,
                "valor_max": 350000
            },
            "Cateterismo": {
                "codigo": "SV002",
                "categoria": "Diagnóstico Invasivo",
                "volumen_min": 2,
                "volumen_max": 6,
                "valor_min": 1500000,
                "valor_max": 3500000
            }
        }
        self.categorias_info = {}
        self.sedes = ["Sede A", "Sede B"]
        self.aseguradoras = ["EPS 1", "EPS 2"]
    
    def test_generar_produccion_cantidad_correcta(self):
        """Test: debe generar un registro por cada combinación servicio-sede-aseguradora"""
        resultado = generar_datos_produccion(
            self.servicios_lista,
            self.servicios_dict,
            self.categorias_info,
            self.sedes,
            self.aseguradoras
        )
        
        # 2 servicios * 2 sedes * 2 aseguradoras = 8 registros
        self.assertEqual(len(resultado), 8)
    
    def test_generar_produccion_rangos_volumen(self):
        """Test: volúmenes deben estar dentro de los rangos configurados"""
        resultado = generar_datos_produccion(
            self.servicios_lista,
            self.servicios_dict,
            self.categorias_info,
            self.sedes,
            self.aseguradoras
        )
        
        for dato in resultado:
            if dato['servicio'] == "Ecocardiograma":
                self.assertGreaterEqual(dato['cantidad'], 15)
                self.assertLessEqual(dato['cantidad'], 40)
            elif dato['servicio'] == "Cateterismo":
                self.assertGreaterEqual(dato['cantidad'], 2)
                self.assertLessEqual(dato['cantidad'], 6)
    
    def test_generar_produccion_estructura_datos(self):
        """Test: cada registro debe tener la estructura correcta"""
        resultado = generar_datos_produccion(
            self.servicios_lista,
            self.servicios_dict,
            self.categorias_info,
            self.sedes,
            self.aseguradoras
        )
        
        campos_requeridos = ['codigo', 'servicio', 'sede', 'aseguradora', 
                            'cantidad', 'valor_unitario', 'categoria']
        
        for dato in resultado:
            for campo in campos_requeridos:
                self.assertIn(campo, dato)


if __name__ == '__main__':
    unittest.main()
