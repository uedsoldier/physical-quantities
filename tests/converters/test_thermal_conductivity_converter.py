import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from modules.physical_quantities import BaseConversionManager
from modules.unit import ThermalConductivityUnits, MockUnits

class TestThermalConductivityConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('thermal_conductivity')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit, expected value, decimal places)
        test_cases = [
            (1.0, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, ThermalConductivityUnits.MILLIWATT_PER_METER_KELVIN.value, 1000.0, 6),
            (1000.0, ThermalConductivityUnits.MILLIWATT_PER_METER_KELVIN.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 1.0, 6),
            (1.0, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, ThermalConductivityUnits.KILOWATT_PER_METER_KELVIN.value, 0.001, 6),
            (1.0, ThermalConductivityUnits.BTU_PER_HOUR_FOOT_FAHRENHEIT.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 1.7295772056, 4),
            (4.184, ThermalConductivityUnits.CALORIE_PER_SECOND_CENTIMETER_CELSIUS.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 1750.5856, 6),
            (100.0, ThermalConductivityUnits.WATT_PER_CENTIMETER_CELSIUS.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 10000.0, 6),
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()