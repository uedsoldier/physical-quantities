import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import SpeedUnits

from .base_converter_test import BaseConversionTest


class TestSpeedConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('speed')

    standard_unit = SpeedUnits.METER_PER_SECOND.value
    
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
        # Exact definitions: 1 km/h = 1/3.6 m/s, 1 kn = 1852/3600 m/s, 1 mph = 1.609344 km/h
        (36, SpeedUnits.KILOMETER_PER_HOUR.value, SpeedUnits.METER_PER_SECOND.value, 10, 6),
        (1, SpeedUnits.KNOT.value, SpeedUnits.METER_PER_SECOND.value, 1852 / 3600, 9),
        (1, SpeedUnits.KNOT.value, SpeedUnits.KILOMETER_PER_HOUR.value, 1.852, 9),
        (1, SpeedUnits.MILE_PER_HOUR.value, SpeedUnits.KILOMETER_PER_HOUR.value, 1.609344, 9),
    ]

if __name__ == "__main__":
    unittest.main()
