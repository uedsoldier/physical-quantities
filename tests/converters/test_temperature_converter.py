import unittest
from core.physical_quantities import TemperatureConversionManager
from core.unit import TemperatureUnits
from .base_converter_test import BaseConversionTest

class TestTemperatureConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = TemperatureConversionManager()

    # Definimos una unidad válida para que la base sepa contra qué probar el error
    standard_unit = TemperatureUnits.KELVIN.value

    test_cases = [
        (373.15,TemperatureUnits.KELVIN.value,TemperatureUnits.CELSIUS.value,100,6),
        (212.0,TemperatureUnits.FAHRENHEIT.value,TemperatureUnits.CELSIUS.value,100,6),
        (0,TemperatureUnits.CELSIUS.value,TemperatureUnits.FAHRENHEIT.value,32,6),
        (0,TemperatureUnits.KELVIN.value,TemperatureUnits.CELSIUS.value,-273.15,6),
        (25, TemperatureUnits.CELSIUS.value, TemperatureUnits.CELSIUS.value, 25, 6),
        (32, TemperatureUnits.FAHRENHEIT.value, TemperatureUnits.KELVIN.value, 273.15, 2),
    ]

if __name__ == '__main__':
    unittest.main()