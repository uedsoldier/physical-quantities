import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from modules.physical_quantities import BaseConversionManager
from modules.unit import MassFlowRateUnits, MockUnits

class TestMassFlowRateConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = BaseConversionManager('mass_flow_rate')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
    # Kilograms per second to grams per second
    (1.0, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.GRAM_PER_SECOND.value, 1000.0, 6),
    # Grams per second to kilograms per second
    (1000, MassFlowRateUnits.GRAM_PER_SECOND.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 1.0, 6),
    # Kilograms per second to milligrams per second
    (1, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.MILLIGRAM_PER_SECOND.value, 1e6, 6),
    # Milligrams per second to kilograms per second
    (1e6, MassFlowRateUnits.MILLIGRAM_PER_SECOND.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 1.0, 6),
    # Kilograms per second to micrograms per second
    (1, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.MICROGRAM_PER_SECOND.value, 1e9, 6),
    # Micrograms per second to kilograms per second
    (1e9, MassFlowRateUnits.MICROGRAM_PER_SECOND.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 1.0, 6),
    # Kilograms per second to nanograms per second
    (1, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.NANOGRAM_PER_SECOND.value, 1e12, 6),
    # Nanograms per second to kilograms per second
    (1e12, MassFlowRateUnits.NANOGRAM_PER_SECOND.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 1.0, 6),
    # Pounds per second to kilograms per second
    (1, MassFlowRateUnits.POUND_PER_SECOND.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 0.45359237, 6),
    # Kilograms per second to pounds per second
    (0.45359237, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.POUND_PER_SECOND.value, 1.0, 6),
    # Ounces per second to kilograms per second
    (1, MassFlowRateUnits.OUNCE_PER_SECOND.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 0.0283495, 6),
    # Kilograms per second to ounces per second
    (0.0283495, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.OUNCE_PER_SECOND.value, 1.0, 6),
    
    # Kilograms per minute to kilograms per second
    (1, MassFlowRateUnits.KILOGRAM_PER_MINUTE.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 0.016666666666666666, 6),
    # Kilograms per second to kilograms per minute
    (0.016666666666666666, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.KILOGRAM_PER_MINUTE.value, 1.0, 6),
    
    # Grams per minute to kilograms per second
    (1, MassFlowRateUnits.GRAM_PER_MINUTE.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 0.000016666666666666667, 6),
    # Kilograms per second to grams per minute
    (0.000016666666666666667, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.GRAM_PER_MINUTE.value, 1.0, 6),
    
    # Milligrams per minute to kilograms per second
    (1, MassFlowRateUnits.MILLIGRAM_PER_MINUTE.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 1.6666666666666667e-8, 6),
    # Kilograms per second to milligrams per minute
    (1.6666666666666667e-8, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.MILLIGRAM_PER_MINUTE.value, 1.0, 6),
    
    # Pounds per minute to kilograms per second
    (1, MassFlowRateUnits.POUND_PER_MINUTE.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 0.007559872833333333, 6),
    # Kilograms per second to pounds per minute
    (0.007559872833333333, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.POUND_PER_MINUTE.value, 1.0, 6),
    
    # Ounces per minute to kilograms per second
    (1, MassFlowRateUnits.OUNCE_PER_MINUTE.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, 0.00047249166666666665, 6),
    # Kilograms per second to ounces per minute
    (0.00047249166666666665, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MassFlowRateUnits.OUNCE_PER_MINUTE.value, 1.0, 6)
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, MassFlowRateUnits.KILOGRAM_PER_SECOND.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, MassFlowRateUnits.KILOGRAM_PER_SECOND.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()