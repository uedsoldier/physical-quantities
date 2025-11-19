import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import ForceUnits, MockUnits

class TestForceConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('force')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
    # Kilonewtons to Newtons
    (0.5, ForceUnits.KILONEWTON.value, ForceUnits.NEWTON.value, 500, 6),
    # Kilogram-force to Newtons
    (1, ForceUnits.KILOGRAM_FORCE.value, ForceUnits.NEWTON.value, 9.80665, 6),
    # Pound-force to Newtons
    (1, ForceUnits.POUND_FORCE.value, ForceUnits.NEWTON.value, 4.44822, 6),
    # Ounce-force to Newtons
    (1, ForceUnits.OUNCE_FORCE.value, ForceUnits.NEWTON.value, 0.2780139, 6),
    # Additional test cases:
    # Newtons to Kilonewtons
    (500, ForceUnits.NEWTON.value, ForceUnits.KILONEWTON.value, 0.5, 6),
    # Newtons to Kilogram-force
    (9.80665, ForceUnits.NEWTON.value, ForceUnits.KILOGRAM_FORCE.value, 1, 6),
    # Newtons to Pound-force
    (4.44822, ForceUnits.NEWTON.value, ForceUnits.POUND_FORCE.value, 1, 6),
    # Newtons to Ounce-force
    (0.2780139, ForceUnits.NEWTON.value, ForceUnits.OUNCE_FORCE.value, 1, 6),
    # Kilonewtons to Kilogram-force
    (1, ForceUnits.KILONEWTON.value, ForceUnits.KILOGRAM_FORCE.value, 101.97162, 5),
    # Kilonewtons to Pound-force
    (1, ForceUnits.KILONEWTON.value, ForceUnits.POUND_FORCE.value, 224.8089431, 3),
    # Kilogram-force to Pound-force
    (1, ForceUnits.KILOGRAM_FORCE.value, ForceUnits.POUND_FORCE.value, 2.20462, 5),
    # Pound-force to Kilogram-force
    (2.20462, ForceUnits.POUND_FORCE.value, ForceUnits.KILOGRAM_FORCE.value, 1, 5),
    # Ounce-force to Pound-force
    (16, ForceUnits.OUNCE_FORCE.value, ForceUnits.POUND_FORCE.value, 1, 2),
    # Pound-force to Ounce-force
    (1, ForceUnits.POUND_FORCE.value, ForceUnits.OUNCE_FORCE.value, 16, 2),
]

        for value,from_unit,to_unit,expected,decimal_places in test_cases:
            with self.subTest(value=value, from_unit=from_unit, to_unit=to_unit):
                try:
                    result = self.converter.convert(value,from_unit,to_unit)
                    self.assertAlmostEqual(float(result), expected, places=decimal_places)
                except AssertionError as e:
                    self.fail(f"Conversion failed for {value} {from_unit} to {to_unit}. Expected {expected}, got {result}. Error: {e}")
                
    def test_invalid_units(self):
        with self.assertRaises(ValueError):
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, ForceUnits.NEWTON.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, ForceUnits.NEWTON.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()