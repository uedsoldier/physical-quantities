import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import ForceUnits
from .base_converter_test import BaseConversionTest

class TestForceConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('force')
    
    standard_unit = ForceUnits.NEWTON.value
    
    test_cases = [
        # Kilonewtons to Newtons
        (0.5, ForceUnits.KILONEWTON.value, ForceUnits.NEWTON.value, 500, 6),
        # Kilogram-force to Newtons
        (1, ForceUnits.KILOGRAM_FORCE.value, ForceUnits.NEWTON.value, 9.80665, 6),
        # Pound-force to Newtons
        (1, ForceUnits.POUND_FORCE.value, ForceUnits.NEWTON.value, 4.44822, 6),
        # Ounce-force to Newtons
        (1, ForceUnits.OUNCE_FORCE.value, ForceUnits.NEWTON.value, 0.2780139, 6),
        # Additional test cases:
        # Newtons to Kilonewtons
        (500, ForceUnits.NEWTON.value, ForceUnits.KILONEWTON.value, 0.5, 6),
        # Newtons to Kilogram-force
        (9.80665, ForceUnits.NEWTON.value, ForceUnits.KILOGRAM_FORCE.value, 1, 6),
        # Newtons to Pound-force
        (4.44822, ForceUnits.NEWTON.value, ForceUnits.POUND_FORCE.value, 1, 6),
        # Newtons to Ounce-force
        (0.2780139, ForceUnits.NEWTON.value, ForceUnits.OUNCE_FORCE.value, 1, 6),
        # Kilonewtons to Kilogram-force
        (1, ForceUnits.KILONEWTON.value, ForceUnits.KILOGRAM_FORCE.value, 101.97162, 5),
        # Kilonewtons to Pound-force
        (1, ForceUnits.KILONEWTON.value, ForceUnits.POUND_FORCE.value, 224.8089431, 3),
        # Kilogram-force to Pound-force
        (1, ForceUnits.KILOGRAM_FORCE.value, ForceUnits.POUND_FORCE.value, 2.20462, 5),
        # Pound-force to Kilogram-force
        (2.20462, ForceUnits.POUND_FORCE.value, ForceUnits.KILOGRAM_FORCE.value, 1, 5),
        # Ounce-force to Pound-force
        (16, ForceUnits.OUNCE_FORCE.value, ForceUnits.POUND_FORCE.value, 1, 2),
        # Pound-force to Ounce-force
        (1, ForceUnits.POUND_FORCE.value, ForceUnits.OUNCE_FORCE.value, 16, 2),
]

if __name__ == '__main__':
    unittest.main()