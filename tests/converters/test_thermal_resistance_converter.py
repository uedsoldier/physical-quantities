import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from modules.physical_quantities import BaseConversionManager
from modules.unit import ThermalResistanceUnits, MockUnits

class TestThermalConductivityConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('thermal_resistance')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit, expected value, decimal places)
        test_cases = [
        # SI unit conversions
        (1.0, ThermalResistanceUnits.KELVIN_PER_WATT.value, ThermalResistanceUnits.MILLIKELVIN_PER_WATT.value, 1000.0, 6),
        (1000.0, ThermalResistanceUnits.MILLIKELVIN_PER_WATT.value, ThermalResistanceUnits.KELVIN_PER_WATT.value, 1.0, 6),
        (1.0, ThermalResistanceUnits.KELVIN_PER_WATT.value, ThermalResistanceUnits.KILOKELVIN_PER_WATT.value, 0.001, 6),
        (1.0, ThermalResistanceUnits.KILOKELVIN_PER_WATT.value, ThermalResistanceUnits.KELVIN_PER_WATT.value, 1000.0, 6),
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, ThermalResistanceUnits.KELVIN_PER_WATT.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, ThermalResistanceUnits.KELVIN_PER_WATT.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()