import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import PowerUnits

from .base_converter_test import BaseConversionTest


class TestPowerConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager("power")

    standard_unit = PowerUnits.WATT.value

    test_cases = [
        (1, PowerUnits.KILOWATT.value, PowerUnits.WATT.value, 1000, 6),
        (1500, PowerUnits.MILLIWATT.value, PowerUnits.WATT.value, 1.5, 6),
        (1, PowerUnits.MEGAWATT.value, PowerUnits.KILOWATT.value, 1000, 6),
        # Mechanical horsepower: 1 hp = 745.6998715822702 W (regression: factor used to be inverted)
        (1, PowerUnits.HORSEPOWER.value, PowerUnits.WATT.value, 745.6998715822702, 6),
        (745.6998715822702, PowerUnits.WATT.value, PowerUnits.HORSEPOWER.value, 1, 6),
        (1, PowerUnits.HORSEPOWER.value, PowerUnits.KILOWATT.value, 0.7456998715822702, 6),
        (3600, PowerUnits.BTU_PER_HOUR.value, PowerUnits.WATT.value, 1055.05585262, 6),
        (1, PowerUnits.REFRIGERATION_TON.value, PowerUnits.KILOWATT.value, 3.5168525, 6),
    ]


if __name__ == "__main__":
    unittest.main()
