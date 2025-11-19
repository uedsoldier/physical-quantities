import unittest
from core.physical_quantities import BaseConversionManager
from math import pi
from core.unit import FrequencyUnits
from .base_converter_test import BaseConversionTest

class TestFrequencyConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('frequency')
    
    standard_unit = FrequencyUnits.HERTZ.value

    test_cases = [
        # Hertz to Radians per Second
        (1, FrequencyUnits.HERTZ.value, FrequencyUnits.RAD_PER_SECOND.value, 2 * pi, 6),
        # Revolutions per Minute (rpm) to Radians per Second
        (100, FrequencyUnits.REV_PER_MINUTE.value, FrequencyUnits.RAD_PER_SECOND.value, 10.471976, 6),
        # Additional test cases:
        # Radians per Second to Hertz
        (2 * pi, FrequencyUnits.RAD_PER_SECOND.value, FrequencyUnits.HERTZ.value, 1, 6),
        # Radians per Second to Revolutions per Minute (rpm)
        (10.471976, FrequencyUnits.RAD_PER_SECOND.value, FrequencyUnits.REV_PER_MINUTE.value, 100, 3),
        # Hertz to Revolutions per Minute (rpm)
        (1, FrequencyUnits.HERTZ.value, FrequencyUnits.REV_PER_MINUTE.value, 60, 2),
        # Revolutions per Minute (rpm) to Hertz
        (60, FrequencyUnits.REV_PER_MINUTE.value, FrequencyUnits.HERTZ.value, 1, 2),
        # Hertz to Degrees per Second
        (1, FrequencyUnits.HERTZ.value, FrequencyUnits.DEG_PER_SECOND.value, 360, 2),
        # Degrees per Second to Hertz
        (360, FrequencyUnits.DEG_PER_SECOND.value, FrequencyUnits.HERTZ.value, 1, 2),
        # Radians per Second to Degrees per Second
        (pi, FrequencyUnits.RAD_PER_SECOND.value, FrequencyUnits.DEG_PER_SECOND.value, 180, 2),
        # Degrees per Second to Radians per Second
        (180, FrequencyUnits.DEG_PER_SECOND.value, FrequencyUnits.RAD_PER_SECOND.value, pi, 6),
        ]

if __name__ == '__main__':
    unittest.main()