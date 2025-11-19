import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import ThermalConductivityUnits
from .base_converter_test import BaseConversionTest

class TestThermalConductivityConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('thermal_conductivity')
    
    standard_unit = ThermalConductivityUnits.WATT_PER_METER_KELVIN.value
    
    test_cases = [
        (1.0, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, ThermalConductivityUnits.MILLIWATT_PER_METER_KELVIN.value, 1000.0, 6),
        (1000.0, ThermalConductivityUnits.MILLIWATT_PER_METER_KELVIN.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 1.0, 6),
        (1.0, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, ThermalConductivityUnits.KILOWATT_PER_METER_KELVIN.value, 0.001, 6),
        (1.0, ThermalConductivityUnits.BTU_PER_HOUR_FOOT_FAHRENHEIT.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 1.7295772056, 4),
        (4.184, ThermalConductivityUnits.CALORIE_PER_SECOND_CENTIMETER_CELSIUS.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 1750.5856, 6),
        (100.0, ThermalConductivityUnits.WATT_PER_CENTIMETER_CELSIUS.value, ThermalConductivityUnits.WATT_PER_METER_KELVIN.value, 10000.0, 6),
    ]

if __name__ == '__main__':
    unittest.main()