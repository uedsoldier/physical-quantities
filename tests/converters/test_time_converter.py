import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import TimeUnits, MockUnits

class TestTimeConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager('time')
    
    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (2,TimeUnits.HOUR.value,TimeUnits.SECOND.value,7200,6),
            (1200,TimeUnits.SECOND.value,TimeUnits.HOUR.value,0.33333333,8)

        ]
        for value,from_unit,to_unit,expected,decimal_places in test_cases:
            with self.subTest(value=value, from_unit=from_unit, to_unit=to_unit):
                result = self.converter.convert(value,from_unit,to_unit)
                self.assertAlmostEqual(
                    float(result), 
                    expected, 
                    places=decimal_places,
                    msg=f"Failed converting {value} {from_unit} to {to_unit}"
                )
                
    def test_invalid_units(self):
        with self.assertRaises(ValueError):
            self.converter.convert(1, MockUnits.MOCK_UNIT.value, TimeUnits.SECOND.value)
        
        with self.assertRaises(ValueError):
            self.converter.convert(1, TimeUnits.SECOND.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()