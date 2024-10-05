import unittest
from modules.physical_quantities import TemperatureConversionManager

class TestTemperatureConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = TemperatureConversionManager()
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (373.15,'K','C',100,6),
            (212.0,'F','C',100,6),
            (0,'C','F',32,6),
            (0,'K','C',-273.15,6),

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
            self.converter.convert(1, 'invalid_unit', 'K')
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, 'K', 'invalid_unit')

if __name__ == '__main__':
    unittest.main()