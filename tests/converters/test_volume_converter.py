import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from modules.physical_quantities import BaseConversionManager
from modules.unit import VolumeUnits, MockUnits

class TestVolumeConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('volume')

    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (1000, VolumeUnits.CUBIC_CENTIMETER.value, VolumeUnits.CUBIC_METER.value, 0.001, 3),
            (2, VolumeUnits.LITER.value, VolumeUnits.CUBIC_METER.value, 0.002, 3),
            (500, VolumeUnits.MILLILITER.value, VolumeUnits.CUBIC_METER.value, 0.0005, 4),
            (10, VolumeUnits.CUBIC_FOOT.value, VolumeUnits.CUBIC_METER.value, 0.283168, 6),
            (3, VolumeUnits.CUBIC_YARD.value, VolumeUnits.CUBIC_METER.value, 2.293665, 6),
            (5, VolumeUnits.GALLON_US.value, VolumeUnits.CUBIC_METER.value, 0.01892705, 8),
        ]
        for value, from_unit, to_unit, expected, decimal_places in test_cases:
            with self.subTest(value=value, from_unit=from_unit, to_unit=to_unit):
                try:
                    result = self.converter.convert(value, from_unit, to_unit)
                    self.assertAlmostEqual(
                        float(result), expected, places=decimal_places
                    )
                except AssertionError as e:
                    self.fail(
                        f"Conversion failed for {value} {from_unit} to {to_unit}. Expected {expected}, got {result}. Error: {e}"
                    )

    def test_invalid_units(self):
        with self.assertRaises(ValueError):
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, VolumeUnits.CUBIC_METER.value)

        with self.assertRaises(ValueError):
            self.converter.convert(1, VolumeUnits.CUBIC_METER.value, MockUnits.MOCK_UNIT.value)


if __name__ == "__main__":
    unittest.main()
