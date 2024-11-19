import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest

from modules.unit import *

class TestDimensions(unittest.TestCase):

    def setUp(self) -> None:
        pass
    
    def test_div_dimension1(self):
        test_dim = LENGTH_DIMENSIONS / TIME_DIMENSIONS
        self.assertEqual(test_dim,SPEED_DIMENSIONS)
    
    def test_div_dimension2(self):
        test_dim = MASS_DIMENSIONS / TIME_DIMENSIONS
        self.assertEqual(test_dim,MASS_FLOW_RATE_DIMENSIONS)
    
    def test_div_dimension3(self):
        test_dim = VOLUME_DIMENSIONS / TIME_DIMENSIONS
        self.assertEqual(test_dim,FLOW_RATE_DIMENSIONS)
    
    def test_mul_dimension1(self):
        test_dim = LENGTH_DIMENSIONS * LENGTH_DIMENSIONS
        self.assertEqual(test_dim,AREA_DIMENSIONS)
    
    def test_mul_dimension2(self):
        test_dim = LENGTH_DIMENSIONS * LENGTH_DIMENSIONS * LENGTH_DIMENSIONS
        self.assertEqual(test_dim,VOLUME_DIMENSIONS)
    
    def test_pow_dimension1(self):
        test_dim = LENGTH_DIMENSIONS**1
        self.assertEqual(test_dim,LENGTH_DIMENSIONS)
    
    def test_pow_dimension2(self):
        test_dim = LENGTH_DIMENSIONS**2
        self.assertEqual(test_dim,AREA_DIMENSIONS)
    
    def test_str_dimension1(self):
        test_str = str(MASS_DIMENSIONS)
        self.assertEqual(test_str,'M')
    
    def test_str_dimension2(self):
        test_str = str(MASS_FLOW_RATE_DIMENSIONS)
        self.assertEqual(test_str,'M*T^-1')
    
    def test_str_dimension3(self):
        test_str = str(VOLTAGE_DIMENSIONS)
        self.assertEqual(test_str,'M*L^2*T^-3*I^-1')
    
    def test_dimensionless1(self):
        test_dim = FORCE_DIMENSIONS/FORCE_DIMENSIONS
        self.assertEqual(test_dim.is_dimensionless(),True)
        
    def test_dimensionless2(self):
        test_dim = CAPACITANCE_DIMENSIONS * FORCE_DIMENSIONS * LENGTH_DIMENSIONS * TIME_DIMENSIONS / (FORCE_DIMENSIONS * LENGTH_DIMENSIONS * TIME_DIMENSIONS * CAPACITANCE_DIMENSIONS)
        print(test_dim)
        self.assertEqual(test_dim.is_dimensionless(),True)
        
        
        # # Test cases: (input value, input unit, output unit,expected value, decimal places)
        # test_cases = [
        #     # Degrees to Radians
        #     (90, AngleUnits.DEGREE.value, AngleUnits.RADIAN.value, pi / 2, 6),
        #     # Radians to Degrees
        #     (pi, AngleUnits.RADIAN.value, AngleUnits.DEGREE.value, 180, 6),
        #     # Degrees to Gradians
        #     (90, AngleUnits.DEGREE.value, AngleUnits.GRADIAN.value, 100, 2),
        #     # Gradians to Degrees
        #     (100, AngleUnits.GRADIAN.value, AngleUnits.DEGREE.value, 90, 2),
        #     # Radians to Gradians
        #     (pi / 2, AngleUnits.RADIAN.value, AngleUnits.GRADIAN.value, 100, 2),
        #     # Gradians to Radians
        #     (100, AngleUnits.GRADIAN.value, AngleUnits.RADIAN.value, pi / 2, 6),
        #     # Full Circle (360 Degrees) to Radians
        #     (360, AngleUnits.DEGREE.value, AngleUnits.RADIAN.value, 2 * pi, 6),
        #     # Full Circle (400 Gradians) to Radians
        #     (400, AngleUnits.GRADIAN.value, AngleUnits.RADIAN.value, 2 * pi, 6),
        #     # Full Circle (2π Radians) to Degrees
        #     (2 * pi, AngleUnits.RADIAN.value, AngleUnits.DEGREE.value, 360, 2),
        #     # Small Angle in Degrees to Radians
        #     (1, AngleUnits.DEGREE.value, AngleUnits.RADIAN.value, pi / 180, 6),
        #     # Small Angle in Gradians to Radians
        #     (1, AngleUnits.GRADIAN.value, AngleUnits.RADIAN.value, pi / 200, 6),

        # ]
        # for value,from_unit,to_unit,expected,decimal_places in test_cases:
        #     with self.subTest(value=value, from_unit=from_unit, to_unit=to_unit):
        #         try:
        #             result = self.converter.convert(value,from_unit,to_unit)
        #             self.assertAlmostEqual(float(result), expected, places=decimal_places)
        #         except AssertionError as e:
        #             self.fail(f"Conversion failed for {value} {from_unit} to {to_unit}. Expected {expected}, got {result}. Error: {e}")
        pass
    
    
    # def test_invalid_units(self):
    #     with self.assertRaises(ValueError):
    #         self.converter.convert(1, MockUnits.MOCK_UNIT.value, AngleUnits.DEGREE.value)
        
    #     with self.assertRaises(ValueError):
    #         self.converter.convert(1, AngleUnits.DEGREE.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()