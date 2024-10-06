import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from modules.physical_quantities import BaseConversionManager
from math import pi

class TestAngleConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = BaseConversionManager('angle')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (90,'deg','rad',pi/2,6),

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
            self.converter.convert(1, 'invalid_unit', 'deg')
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, 'deg', 'invalid_unit')

if __name__ == '__main__':
    unittest.main()