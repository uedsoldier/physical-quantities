import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import LengthUnits, MockUnits

class TestLengthConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('length')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (1.0,LengthUnits.METER.value,LengthUnits.MILLIMETER.value,1000,6),
            (25.4,LengthUnits.MILLIMETER.value,LengthUnits.INCH.value,1,6),
            (10,LengthUnits.KILOMETER.value,LengthUnits.METER.value,10000,6),
            (2.0,LengthUnits.MILLIMETER.value,LengthUnits.MICROMETER.value,2000,6),
            (1,LengthUnits.FOOT.value,LengthUnits.INCH.value,12,2),
            (3,LengthUnits.INCH.value,LengthUnits.MILLIMETER.value,76.2,6)
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, LengthUnits.METER.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, LengthUnits.METER.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()