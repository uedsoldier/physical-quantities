import unittest
from modules.physical_quantities import BaseConversionManager

class TestLengthConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = BaseConversionManager('length')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (1.0,'m','mm',1000,6),
            (25.4,'mm','in',1,6),
            (10,'km','m',10000,6),
            (2.0,'mm','μm',2000,6),
            (1,'ft','in',12,2),
            (3,'in','mm',76.2,6)
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
            self.converter.convert(1, 'invalid_unit', 'm')
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, 'm', 'invalid_unit')

if __name__ == '__main__':
    unittest.main()