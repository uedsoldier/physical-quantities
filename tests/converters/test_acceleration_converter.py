import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import AccelerationUnits
from .base_converter_test import BaseConversionTest


class TestAccelerationConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager("acceleration")

    standard_unit = AccelerationUnits.METER_PER_SECOND_SQUARED.value

    test_cases = [
        (1, AccelerationUnits.G_FORCE.value, AccelerationUnits.METER_PER_SECOND_SQUARED.value, 9.80665, 6),
        (9.80665, AccelerationUnits.METER_PER_SECOND_SQUARED.value, AccelerationUnits.G_FORCE.value, 1, 6),
        (100, AccelerationUnits.CENTIMETER_PER_SECOND_SQUARED.value, AccelerationUnits.METER_PER_SECOND_SQUARED.value, 1, 6),
        (1000, AccelerationUnits.MILLIMETER_PER_SECOND_SQUARED.value, AccelerationUnits.METER_PER_SECOND_SQUARED.value, 1, 6),
        # 12960000 (km/h)/h = 1000 m/s² because 1 km/h² = 1000 / 3600² m/s²
        (12960000, AccelerationUnits.KILOMETER_PER_HOUR_SQUARED.value, AccelerationUnits.METER_PER_SECOND_SQUARED.value, 1000, 6),
        (12960000, AccelerationUnits.MILE_PER_HOUR_SQUARED.value, AccelerationUnits.METER_PER_SECOND_SQUARED.value, 1609.344, 6),
    ]


if __name__ == "__main__":
    unittest.main()
