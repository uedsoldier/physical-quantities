import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import ThermalResistanceUnits
from .base_converter_test import BaseConversionTest

class TestThermalConductivityConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('thermal_resistance')
    
    standard_unit = ThermalResistanceUnits.KELVIN_PER_WATT.value
    
    test_cases = [
        # SI unit conversions
        (1.0, ThermalResistanceUnits.KELVIN_PER_WATT.value, ThermalResistanceUnits.MILLIKELVIN_PER_WATT.value, 1000.0, 6),
        (1000.0, ThermalResistanceUnits.MILLIKELVIN_PER_WATT.value, ThermalResistanceUnits.KELVIN_PER_WATT.value, 1.0, 6),
        (1.0, ThermalResistanceUnits.KELVIN_PER_WATT.value, ThermalResistanceUnits.KILOKELVIN_PER_WATT.value, 0.001, 6),
        (1.0, ThermalResistanceUnits.KILOKELVIN_PER_WATT.value, ThermalResistanceUnits.KELVIN_PER_WATT.value, 1000.0, 6),
    ]

if __name__ == '__main__':
    unittest.main()