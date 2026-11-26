import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import TimeUnits

from .base_converter_test import BaseConversionTest


class TestTimeConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('time')
    
    standard_unit = TimeUnits.SECOND.value
    
    test_cases = [
        (2,TimeUnits.HOUR.value,TimeUnits.SECOND.value,7200,6),
        (1200,TimeUnits.SECOND.value,TimeUnits.HOUR.value,0.33333333,8)
    ]

if __name__ == '__main__':
    unittest.main()