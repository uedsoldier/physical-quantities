import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import LuminousIntensityUnits, MockUnits

class TestLuminousIntensityConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('luminous_intensity')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
        # Candela to Millcandela
        (1.0, LuminousIntensityUnits.CANDELA.value, LuminousIntensityUnits.MILLICANDELA.value, 1000, 6),
        # Millcandela to Candela
        (1000, LuminousIntensityUnits.MILLICANDELA.value, LuminousIntensityUnits.CANDELA.value, 1.0, 6),
        # Microcandela to Millcandela
        (1, LuminousIntensityUnits.MICROCANDELA.value, LuminousIntensityUnits.MILLICANDELA.value, 0.001, 6),
        # Millcandela to Microcandela
        (1, LuminousIntensityUnits.MILLICANDELA.value, LuminousIntensityUnits.MICROCANDELA.value, 1000, 6),
        # Kilocandela to Candela
        (1, LuminousIntensityUnits.KILOCANDELA.value, LuminousIntensityUnits.CANDELA.value, 1000, 6),
        # Candela to Kilocandela
        (1000, LuminousIntensityUnits.CANDELA.value, LuminousIntensityUnits.KILOCANDELA.value, 1, 6),
        # Megacandela to Kilocandela
        (1, LuminousIntensityUnits.MEGACANDELA.value, LuminousIntensityUnits.KILOCANDELA.value, 1000, 6),
        # Kilocandela to Megacandela
        (1000, LuminousIntensityUnits.KILOCANDELA.value, LuminousIntensityUnits.MEGACANDELA.value, 1, 6),
        # Gigacandela to Megacandela
        (1, LuminousIntensityUnits.GIGACANDELA.value, LuminousIntensityUnits.MEGACANDELA.value, 1000, 6),
        # Megacandela to Gigacandela
        (1000, LuminousIntensityUnits.MEGACANDELA.value, LuminousIntensityUnits.GIGACANDELA.value, 1, 6)
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, LuminousIntensityUnits.CANDELA.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, LuminousIntensityUnits.CANDELA.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()