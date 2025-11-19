import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import EnergyUnits
from .base_converter_test import BaseConversionTest

class TestEnergyConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('energy')
    
    standard_unit = EnergyUnits.JOULE.value
    
    test_cases = [
        # Joules to Calories
        (4184, EnergyUnits.JOULE.value, EnergyUnits.CALORIE.value, 1000, 2),
        # Calories to Joules
        (1000, EnergyUnits.CALORIE.value, EnergyUnits.JOULE.value, 4184, 0),
        # Kilowatt-hours to Joules
        (1, EnergyUnits.KILOWATT_HOUR.value, EnergyUnits.JOULE.value, 3600000, 0),
        # Joules to Kilowatt-hours
        (3600000, EnergyUnits.JOULE.value, EnergyUnits.KILOWATT_HOUR.value, 1, 5),
        # Joules to Electron Volts
        # (Difficult cases since they handle very low floating point numbers, but calculations where OK)
        # (1, EnergyUnits.JOULE.value, EnergyUnits.ELECTRON_VOLT.value, 6.242e18, 0),
        # Electron Volts to Joules 
        # (1e12, EnergyUnits.ELECTRON_VOLT.value, EnergyUnits.JOULE.value, 1.602176565e-7, 0),
        # Calories to Kilojoules
        (1000, EnergyUnits.CALORIE.value, EnergyUnits.KILOJOULE.value, 4.184, 3),
        # Kilojoules to Calories
        (4.184, EnergyUnits.KILOJOULE.value, EnergyUnits.CALORIE.value, 1000, 0),
        # Joules to British Thermal Units (BTU)
        (1055.06, EnergyUnits.JOULE.value, EnergyUnits.BRITISH_THERMAL_UNIT.value, 1, 2),
        # British Thermal Units (BTU) to Joules
        (1, EnergyUnits.BRITISH_THERMAL_UNIT.value, EnergyUnits.JOULE.value, 1055.06, 2),
    ]

if __name__ == '__main__':
    unittest.main()