import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import PressureUnits, MockUnits

class TestPressureConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('pressure')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
        # Pascal to Kilopascal
        (1.0, PressureUnits.PASCAL.value, PressureUnits.KILOPASCAL.value, 1e-3, 6),
        # Kilopascal to Pascal
        (1, PressureUnits.KILOPASCAL.value, PressureUnits.PASCAL.value, 1e3, 6),
        # Megapascal to Pascal
        (1, PressureUnits.MEGAPASCAL.value, PressureUnits.PASCAL.value, 1e6, 6),
        # Pascal to Megapascal
        (1e6, PressureUnits.PASCAL.value, PressureUnits.MEGAPASCAL.value, 1.0, 6),
        # Gigapascal to Pascal
        (1, PressureUnits.GIGAPASCAL.value, PressureUnits.PASCAL.value, 1e9, 6),
        # Pascal to Gigapascal
        (1e9, PressureUnits.PASCAL.value, PressureUnits.GIGAPASCAL.value, 1.0, 6),
        # Bar to Pascal
        (1, PressureUnits.BAR.value, PressureUnits.PASCAL.value, 1e5, 6),
        # Pascal to Bar
        (1e5, PressureUnits.PASCAL.value, PressureUnits.BAR.value, 1.0, 6),
        # Millibar to Pascal
        (1, PressureUnits.MILLIBAR.value, PressureUnits.PASCAL.value, 100, 6),
        # Pascal to Millibar
        (100, PressureUnits.PASCAL.value, PressureUnits.MILLIBAR.value, 1.0, 6),
        # Atmosphere to Pascal
        (1, PressureUnits.ATMOSPHERE.value, PressureUnits.PASCAL.value, 101325, 6),
        # Pascal to Atmosphere
        (101325, PressureUnits.PASCAL.value, PressureUnits.ATMOSPHERE.value, 1.0, 6),
        # Millimeter of Mercury to Pascal
        (1, PressureUnits.MILLIMETER_OF_MERCURY.value, PressureUnits.PASCAL.value, 133.322, 6),
        # Pascal to Millimeter of Mercury
        (133.322, PressureUnits.PASCAL.value, PressureUnits.MILLIMETER_OF_MERCURY.value, 1.0, 6),
        # Inch of Mercury to Pascal
        (1, PressureUnits.INCH_OF_MERCURY.value, PressureUnits.PASCAL.value, 3386.39, 6),
        # Pascal to Inch of Mercury
        (3386.39, PressureUnits.PASCAL.value, PressureUnits.INCH_OF_MERCURY.value, 1.0, 6),
        
        # Pound per Square Inch (psi) to Pascal
        (1, PressureUnits.POUND_SQUARE_INCH.value, PressureUnits.PASCAL.value, 6894.76, 6),
        
        # Pascal to Pound per Square Inch (psi)
        (6894.76, PressureUnits.PASCAL.value, PressureUnits.POUND_SQUARE_INCH.value, 1.0, 6),
        
        # Kilogram per Square Centimeter (kgf/cm²) to Pascal
        (1, PressureUnits.KILOGRAM_FORCE_PER_CENTIMETER_SQUARED.value, PressureUnits.PASCAL.value, 98066.5, 6),
        
        # Pascal to Kilogram per Square Centimeter (kgf/cm²)
        (98066.5, PressureUnits.PASCAL.value, PressureUnits.KILOGRAM_FORCE_PER_CENTIMETER_SQUARED.value, 1.0, 6)
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, PressureUnits.PASCAL.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, PressureUnits.PASCAL.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()