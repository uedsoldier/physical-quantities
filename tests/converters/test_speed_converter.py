import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from modules.physical_quantities import BaseConversionManager
from modules.unit import SpeedUnits, MockUnits

class TestSpeedConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('speed')

    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
        (1000, SpeedUnits.METER_PER_SECOND.value, SpeedUnits.KILOMETER_PER_HOUR.value, 3600, 1),  # 1000 m/s to km/h
        (1, SpeedUnits.KILOMETER_PER_HOUR.value, SpeedUnits.METER_PER_SECOND.value, 0.277777778, 9),  # 1 km/h to m/s
        (60, SpeedUnits.MILE_PER_HOUR.value, SpeedUnits.METER_PER_SECOND.value, 26.8224, 4),  # 60 mph to m/s
        (100, SpeedUnits.KNOT.value, SpeedUnits.METER_PER_SECOND.value, 51.4444, 4),  # 100 knots to m/s
        (500, SpeedUnits.CENTIMETER_PER_SECOND.value, SpeedUnits.METER_PER_SECOND.value, 5, 1),  # 500 cm/s to m/s
        (0.5, SpeedUnits.KILOMETER_PER_SECOND.value, SpeedUnits.METER_PER_SECOND.value, 500, 1),  # 0.5 km/s to m/s
        (1200, SpeedUnits.MILLIMETER_PER_SECOND.value, SpeedUnits.METER_PER_SECOND.value, 1.2, 1),  # 1200 mm/s to m/s
        (3, SpeedUnits.MICROMETER_PER_SECOND.value, SpeedUnits.METER_PER_SECOND.value, 0.000003, 6),  # 3 μm/s to m/s
        (15, SpeedUnits.METER_PER_SECOND.value, SpeedUnits.MILE_PER_HOUR.value, 33.554044381, 6),  # 15 m/s to mph
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
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, SpeedUnits.METER_PER_SECOND.value)

        with self.assertRaises(ValueError):
            self.converter.convert(1, SpeedUnits.METER_PER_SECOND.value, MockUnits.MOCK_UNIT.value)


if __name__ == "__main__":
    unittest.main()
