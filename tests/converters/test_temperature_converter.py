import unittest
from core.physical_quantities import TemperatureConversionManager
from core.unit import TemperatureUnits, MockUnits

class TestTemperatureConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = TemperatureConversionManager()
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (373.15,TemperatureUnits.KELVIN.value,TemperatureUnits.CELSIUS.value,100,6),
            (212.0,TemperatureUnits.FAHRENHEIT.value,TemperatureUnits.CELSIUS.value,100,6),
            (0,TemperatureUnits.CELSIUS.value,TemperatureUnits.FAHRENHEIT.value,32,6),
            (0,TemperatureUnits.KELVIN.value,TemperatureUnits.CELSIUS.value,-273.15,6),

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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, TemperatureUnits.KELVIN.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, TemperatureUnits.KELVIN.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()