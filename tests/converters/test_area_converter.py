import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import AreaUnits
from .base_converter_test import BaseConversionTest


class TestAreaConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager("area")

    standard_unit = AreaUnits.SQUARE_METER.value
    test_cases = [
            # Square Centimeters to Square Meters
            (250, AreaUnits.SQUARE_CENTIMETER.value, AreaUnits.SQUARE_METER.value, 0.025, 6),
            # Square Feet to Square Meters
            (1.5, AreaUnits.SQUARE_FOOT.value, AreaUnits.SQUARE_METER.value, 0.13935, 4),
            # Square Yards to Square Meters
            (0.75, AreaUnits.SQUARE_YARD.value, AreaUnits.SQUARE_METER.value, 0.6271, 4),
            # Acres to Square Kilometers
            (5, AreaUnits.ACRE.value, AreaUnits.SQUARE_KILOMETER.value, 0.020234, 4),
            # Square Kilometers to Hectares
            (2.2, AreaUnits.SQUARE_KILOMETER.value, AreaUnits.HECTARE.value, 220, 3),
            # Additional test cases:
            # Square Meters to Square Centimeters
            (0.025, AreaUnits.SQUARE_METER.value, AreaUnits.SQUARE_CENTIMETER.value, 250, 0),
            # Square Meters to Square Feet
            (0.13935, AreaUnits.SQUARE_METER.value, AreaUnits.SQUARE_FOOT.value, 1.5, 2),
            # Square Meters to Square Yards
            (0.6271, AreaUnits.SQUARE_METER.value, AreaUnits.SQUARE_YARD.value, 0.75, 2),
            # Square Kilometers to Acres
            (0.020234, AreaUnits.SQUARE_KILOMETER.value, AreaUnits.ACRE.value, 5, 2),
            # Hectares to Square Kilometers
            (220, AreaUnits.HECTARE.value, AreaUnits.SQUARE_KILOMETER.value, 2.2, 1),
            # Acres to Square Meters
            (1, AreaUnits.ACRE.value, AreaUnits.SQUARE_METER.value, 4046.85642, 5),
            # Square Meters to Acres
            (4046.85642, AreaUnits.SQUARE_METER.value, AreaUnits.ACRE.value, 1, 6),
            # Hectares to Acres
            (1, AreaUnits.HECTARE.value, AreaUnits.ACRE.value, 2.47105, 5),
            # Acres to Hectares
            (2.47105, AreaUnits.ACRE.value, AreaUnits.HECTARE.value, 1, 5),
            # Square Miles to Square Kilometers
            (1, AreaUnits.SQUARE_MILE.value, AreaUnits.SQUARE_KILOMETER.value, 2.58999, 5),
            # Square Kilometers to Square Miles
            (2.58999, AreaUnits.SQUARE_KILOMETER.value, AreaUnits.SQUARE_MILE.value, 1, 5),
        ]


if __name__ == "__main__":
    unittest.main()
