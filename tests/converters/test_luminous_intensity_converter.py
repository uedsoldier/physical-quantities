import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import LuminousIntensityUnits
from .base_converter_test import BaseConversionTest

class TestLuminousIntensityConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('luminous_intensity')
    
    standard_unit = LuminousIntensityUnits.CANDELA.value
    
    test_cases = [
        # Candela to Millcandela
        (1.0, LuminousIntensityUnits.CANDELA.value, LuminousIntensityUnits.MILLICANDELA.value, 1000, 6),
        # Millcandela to Candela
        (1000, LuminousIntensityUnits.MILLICANDELA.value, LuminousIntensityUnits.CANDELA.value, 1.0, 6),
        # Microcandela to Millcandela
        (1, LuminousIntensityUnits.MICROCANDELA.value, LuminousIntensityUnits.MILLICANDELA.value, 0.001, 6),
        # Millcandela to Microcandela
        (1, LuminousIntensityUnits.MILLICANDELA.value, LuminousIntensityUnits.MICROCANDELA.value, 1000, 6),
        # Kilocandela to Candela
        (1, LuminousIntensityUnits.KILOCANDELA.value, LuminousIntensityUnits.CANDELA.value, 1000, 6),
        # Candela to Kilocandela
        (1000, LuminousIntensityUnits.CANDELA.value, LuminousIntensityUnits.KILOCANDELA.value, 1, 6),
        # Megacandela to Kilocandela
        (1, LuminousIntensityUnits.MEGACANDELA.value, LuminousIntensityUnits.KILOCANDELA.value, 1000, 6),
        # Kilocandela to Megacandela
        (1000, LuminousIntensityUnits.KILOCANDELA.value, LuminousIntensityUnits.MEGACANDELA.value, 1, 6),
        # Gigacandela to Megacandela
        (1, LuminousIntensityUnits.GIGACANDELA.value, LuminousIntensityUnits.MEGACANDELA.value, 1000, 6),
        # Megacandela to Gigacandela
        (1000, LuminousIntensityUnits.MEGACANDELA.value, LuminousIntensityUnits.GIGACANDELA.value, 1, 6)
    ]

if __name__ == '__main__':
    unittest.main()