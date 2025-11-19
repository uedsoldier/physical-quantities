import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import LengthUnits
from .base_converter_test import BaseConversionTest

class TestLengthConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager('length')
    
    standard_unit = LengthUnits.METER.value
    
    test_cases = [
        (1.0,LengthUnits.METER.value,LengthUnits.MILLIMETER.value,1000,6),
        (25.4,LengthUnits.MILLIMETER.value,LengthUnits.INCH.value,1,6),
        (10,LengthUnits.KILOMETER.value,LengthUnits.METER.value,10000,6),
        (2.0,LengthUnits.MILLIMETER.value,LengthUnits.MICROMETER.value,2000,6),
        (1,LengthUnits.FOOT.value,LengthUnits.INCH.value,12,2),
        (3,LengthUnits.INCH.value,LengthUnits.MILLIMETER.value,76.2,6)
    ]

if __name__ == '__main__':
    unittest.main()