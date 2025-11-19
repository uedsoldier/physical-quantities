import unittest

from core.physical_quantities import BaseConversionManager
from math import pi
from core.unit import AngleUnits, MockUnits

class TestAngleConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('angle')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            # Degrees to Radians
            (90, AngleUnits.DEGREE.value, AngleUnits.RADIAN.value, pi / 2, 6),
            # Radians to Degrees
            (pi, AngleUnits.RADIAN.value, AngleUnits.DEGREE.value, 180, 6),
            # Degrees to Gradians
            (90, AngleUnits.DEGREE.value, AngleUnits.GRADIAN.value, 100, 2),
            # Gradians to Degrees
            (100, AngleUnits.GRADIAN.value, AngleUnits.DEGREE.value, 90, 2),
            # Radians to Gradians
            (pi / 2, AngleUnits.RADIAN.value, AngleUnits.GRADIAN.value, 100, 2),
            # Gradians to Radians
            (100, AngleUnits.GRADIAN.value, AngleUnits.RADIAN.value, pi / 2, 6),
            # Full Circle (360 Degrees) to Radians
            (360, AngleUnits.DEGREE.value, AngleUnits.RADIAN.value, 2 * pi, 6),
            # Full Circle (400 Gradians) to Radians
            (400, AngleUnits.GRADIAN.value, AngleUnits.RADIAN.value, 2 * pi, 6),
            # Full Circle (2π Radians) to Degrees
            (2 * pi, AngleUnits.RADIAN.value, AngleUnits.DEGREE.value, 360, 2),

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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, AngleUnits.DEGREE.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, AngleUnits.DEGREE.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()