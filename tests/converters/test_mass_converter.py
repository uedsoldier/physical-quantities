import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import MassUnits

from .base_converter_test import BaseConversionTest


class TestMassConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager("mass")

    standard_unit = MassUnits.KILOGRAM.value

    test_cases = [
        (1.0, MassUnits.KILOGRAM.value, MassUnits.GRAM.value, 1000, 6),
        (454, MassUnits.GRAM.value, MassUnits.POUND.value, 1, 2),
    ]


if __name__ == "__main__":
    unittest.main()
