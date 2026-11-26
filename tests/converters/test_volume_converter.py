import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import VolumeUnits

from .base_converter_test import BaseConversionTest


class TestVolumeConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('volume')

    standard_unit = VolumeUnits.CUBIC_METER.value
    
    test_cases = [
        (1000, VolumeUnits.CUBIC_CENTIMETER.value, VolumeUnits.CUBIC_METER.value, 0.001, 3),
        (2, VolumeUnits.LITER.value, VolumeUnits.CUBIC_METER.value, 0.002, 3),
        (500, VolumeUnits.MILLILITER.value, VolumeUnits.CUBIC_METER.value, 0.0005, 4),
        (10, VolumeUnits.CUBIC_FOOT.value, VolumeUnits.CUBIC_METER.value, 0.283168, 6),
        (3, VolumeUnits.CUBIC_YARD.value, VolumeUnits.CUBIC_METER.value, 2.293665, 6),
        (5, VolumeUnits.GALLON_US.value, VolumeUnits.CUBIC_METER.value, 0.01892705892, 8),
    ]


if __name__ == "__main__":
    unittest.main()
