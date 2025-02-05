import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from modules.physical_quantities import BaseConversionManager
from math import pi
from modules.unit import FrequencyUnits, MockUnits

class TestFrequencyConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('frequency')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
        # Hertz to Radians per Second
        (1, FrequencyUnits.HERTZ.value, FrequencyUnits.RAD_PER_SECOND.value, 2 * pi, 6),
        # Revolutions per Minute (rpm) to Radians per Second
        (100, FrequencyUnits.REV_PER_MINUTE.value, FrequencyUnits.RAD_PER_SECOND.value, 10.471976, 6),
        # Additional test cases:
        # Radians per Second to Hertz
        (2 * pi, FrequencyUnits.RAD_PER_SECOND.value, FrequencyUnits.HERTZ.value, 1, 6),
        # Radians per Second to Revolutions per Minute (rpm)
        (10.471976, FrequencyUnits.RAD_PER_SECOND.value, FrequencyUnits.REV_PER_MINUTE.value, 100, 3),
        # Hertz to Revolutions per Minute (rpm)
        (1, FrequencyUnits.HERTZ.value, FrequencyUnits.REV_PER_MINUTE.value, 60, 2),
        # Revolutions per Minute (rpm) to Hertz
        (60, FrequencyUnits.REV_PER_MINUTE.value, FrequencyUnits.HERTZ.value, 1, 2),
        # Hertz to Degrees per Second
        (1, FrequencyUnits.HERTZ.value, FrequencyUnits.DEG_PER_SECOND.value, 360, 2),
        # Degrees per Second to Hertz
        (360, FrequencyUnits.DEG_PER_SECOND.value, FrequencyUnits.HERTZ.value, 1, 2),
        # Radians per Second to Degrees per Second
        (pi, FrequencyUnits.RAD_PER_SECOND.value, FrequencyUnits.DEG_PER_SECOND.value, 180, 2),
        # Degrees per Second to Radians per Second
        (180, FrequencyUnits.DEG_PER_SECOND.value, FrequencyUnits.RAD_PER_SECOND.value, pi, 6),
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, FrequencyUnits.HERTZ.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, FrequencyUnits.HERTZ.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()