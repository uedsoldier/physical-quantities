import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import TimeUnits
from .base_converter_test import BaseConversionTest

class TestTimeConverter(BaseConversionTest):
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