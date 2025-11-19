import unittest

from core.physical_quantities import BaseConversionManager
from math import pi
from core.unit import AngleUnits
from .base_converter_test import BaseConversionTest

class TestAngleConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('angle')
    
    standard_unit = AngleUnits.DEGREE.value

    test_cases = [
            # Degrees to Radians
            (90, AngleUnits.DEGREE.value, AngleUnits.RADIAN.value, pi / 2, 6),
            # Radians to Degrees
            (pi, AngleUnits.RADIAN.value, AngleUnits.DEGREE.value, 180, 6),
            # Degrees to Gradians
            (90, AngleUnits.DEGREE.value, AngleUnits.GRADIAN.value, 100, 2),
            # Gradians to Degrees
            (100, AngleUnits.GRADIAN.value, AngleUnits.DEGREE.value, 90, 2),
            # Radians to Gradians
            (pi / 2, AngleUnits.RADIAN.value, AngleUnits.GRADIAN.value, 100, 2),
            # Gradians to Radians
            (100, AngleUnits.GRADIAN.value, AngleUnits.RADIAN.value, pi / 2, 6),
            # Full Circle (360 Degrees) to Radians
            (360, AngleUnits.DEGREE.value, AngleUnits.RADIAN.value, 2 * pi, 6),
            # Full Circle (400 Gradians) to Radians
            (400, AngleUnits.GRADIAN.value, AngleUnits.RADIAN.value, 2 * pi, 6),
            # Full Circle (2π Radians) to Degrees
            (2 * pi, AngleUnits.RADIAN.value, AngleUnits.DEGREE.value, 360, 2),

        ]

if __name__ == '__main__':
    unittest.main()