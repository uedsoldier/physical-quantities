import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import VoltageUnits

from .base_converter_test import BaseConversionTest


class TestVoltageConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('voltage')
    
    standard_unit =VoltageUnits.VOLT.value
    
    test_cases = [
        (1,VoltageUnits.VOLT.value,VoltageUnits.MICROVOLT.value,1e6,6),
        (10000,VoltageUnits.VOLT.value,VoltageUnits.KILOVOLT.value,10,9)

    ]

if __name__ == '__main__':
    unittest.main()