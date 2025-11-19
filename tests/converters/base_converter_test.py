import unittest
from typing import List, Tuple, Any
from core.unit import MockUnits

class BaseConversionTest(unittest.TestCase):
    """
    Clase base para todos los tests de conversión.
    Implementa la lógica de iteración y aserción.
    """
    
    # Los hijos deben sobrescribir estos atributos
    conversion_manager = None
    # Formato: (valor, unidad_origen, unidad_destino, valor_esperado, decimales)
    test_cases: List[Tuple[float, Any, Any, float, int]] = []

    standard_unit = None

    def test_batch_conversions(self):
        if not self.test_cases or self.conversion_manager is None:
            self.skipTest('Base class or empty test cases')
        
        for value, from_unit, to_unit, expected, decimal_places in self.test_cases:
            with self.subTest(value=value, from_u=from_unit, to_u=to_unit):
                result = self.conversion_manager.convert(value,from_unit,to_unit)
                self.assertAlmostEqual(
                    result_float:=float(result), 
                    expected, 
                    places=decimal_places,
                    msg=f'\nConversion failed:\n'
                        f'   Input: {value} {from_unit}\n'
                        f'   Output: {result_float} {to_unit}\n'
                        f'   Expected: {expected}\n'
                )
    
    def test_invalid_units_generic(self):
        """Test genérico que verifica que explote con unidades inválidas"""
        if self.conversion_manager is None or self.standard_unit is None:
            self.skipTest("Converter or standard_unit not defined")

        # Prueba 1: Unidad válida -> Mock
        with self.assertRaises(ValueError, msg="Should fail converting to MockUnit"):
            self.conversion_manager.convert(1, self.standard_unit, MockUnits.MOCK_UNIT.value)
        
        # Prueba 2: Mock -> Unidad válida
        with self.assertRaises(ValueError, msg="Should fail converting from MockUnit"):
            self.conversion_manager.convert(1, MockUnits.MOCK_UNIT.value, self.standard_unit)
    
