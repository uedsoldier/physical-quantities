import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import MassUnits, MockUnits

class TestMassConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('mass')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (1.0,MassUnits.KILOGRAM.value,MassUnits.GRAM.value,1000,6),
            (454,MassUnits.GRAM.value,MassUnits.POUND.value,1,2)
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, MassUnits.KILOGRAM.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, MassUnits.KILOGRAM.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()