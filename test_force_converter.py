import unittest
from modules.physical_quantities import BaseConversionManager

class TestForceConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = BaseConversionManager('force')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (0.5,'kN','N',500,6),
            (1,'kgf','N',9.80665,6),
            (1,'lbf','N',4.44822,6),
            (1,'ozf','N',0.2780139,6)
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
            self.converter.convert(1, 'invalid_unit', 'N')
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, 'N', 'invalid_unit')

if __name__ == '__main__':
    unittest.main()