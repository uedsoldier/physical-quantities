import unittest

from physical_quantities.units import *


class TestUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass
    
    def test_compatible_units1(self):
        test_unit1 = LengthUnits.METER.value
        test_unit2 = LengthUnits.KILOMETER.value
        self.assertTrue(test_unit1.is_compatible_with(test_unit2))
    
    def test_compatible_units2(self):
        test_unit1 = TemperatureUnits.KELVIN.value
        test_unit2 = LengthUnits.KILOMETER.value
        self.assertFalse(test_unit1.is_compatible_with(test_unit2))
    
    def test_compatible_units3(self):
        test_unit1 = LuminousIntensityUnits.CANDELA.value
        test_unit2 = None
        with self.assertRaises(TypeError):
            test_unit1.is_compatible_with(test_unit2)
    
    def test_repr1(self):
        self.assertEqual(
            'Unit(name=ton per second, symbol=ton/s, dimensions=M*T^-1)',
            repr(MassFlowRateUnits.TON_PER_SECOND.value),
        )
        self.assertEqual('Unit(name=yard, symbol=yd, dimensions=L)', repr(LengthUnits.YARD.value))
        self.assertEqual(
            'Unit(name=weber, symbol=Wb, dimensions=M*L^2*T^-2*I^-1)',
            repr(MagneticFluxUnits.WEBER.value),
        )
        self.assertEqual(
            'Unit(name=newton, symbol=N, dimensions=M*L*T^-2)', repr(ForceUnits.NEWTON.value)
        )
        momentum_unit = MassUnits.KILOGRAM.value * LengthUnits.METER.value / TimeUnits.SECOND.value
        self.assertEqual(
            'Unit(name=kilogram*meter/second, symbol=kg*m/s, dimensions=M*L*T^-1)',
            repr(momentum_unit),
        )

    def test_str1(self):
        self.assertEqual('kg/min', str(MassFlowRateUnits.KILOGRAM_PER_MINUTE.value))
        self.assertEqual('μm', str(LengthUnits.MICROMETER.value))
        self.assertEqual('MWb', str(MagneticFluxUnits.MEGAWEBER.value))
        self.assertEqual('lbf', str(ForceUnits.POUND_FORCE.value))
        self.assertEqual('Ω*m', str(ResistanceUnits.OHM.value * LengthUnits.METER.value))

    def test_hash_is_consistent_with_eq(self):
        newton = ForceUnits.NEWTON.value
        equivalent_newton = Unit('kg*m/s²', 'kg*m/s²', FORCE_DIMENSIONS)
        self.assertEqual(newton, equivalent_newton)
        self.assertEqual(hash(newton), hash(equivalent_newton))

    def test_units_are_usable_as_dict_keys_and_in_sets(self):
        units = {LengthUnits.METER.value: 'm', TimeUnits.SECOND.value: 's'}
        self.assertEqual('m', units[LengthUnits.METER.value])
        self.assertIn(LengthUnits.METER.value, {LengthUnits.METER.value})

    def test_unit_without_dimensions_is_dimensionless(self):
        unit = Unit('dimensionless', '-', None)
        self.assertIsInstance(unit.dimensions, Dimensions)
        self.assertTrue(unit.is_dimensionless())

    def test_symbols_resolve_to_the_right_unit(self):
        self.assertIs(MassUnits.GRAM.value, find_unit_by_symbol('g'))
        self.assertIs(AccelerationUnits.G_FORCE.value, find_unit_by_symbol('gₙ'))
        self.assertIs(IlluminationUnits.MILLILUX.value, find_unit_by_symbol('mlx'))
        self.assertIs(IlluminationUnits.MEGALUX.value, find_unit_by_symbol('Mlx'))

    def test_mul_units1(self):
        test_unit1 = LengthUnits.METER.value
        test_unit2 = LengthUnits.METER.value
        test_unit_mul = test_unit1 * test_unit2
        self.assertTrue(test_unit_mul == AreaUnits.SQUARE_METER.value)

    def test_mul_units2(self):
        test_unit1 = ElectricCurrentUnits.AMPERE.value
        test_unit2 = TimeUnits.SECOND.value
        test_unit_mul = test_unit1 * test_unit2
        self.assertTrue(test_unit_mul == ElectricChargeUnits.COULOMB.value)
    
    def test_div_units1(self):
        test_unit1 = LengthUnits.METER.value / TimeUnits.SECOND.value
        self.assertTrue(test_unit1.is_compatible_with(SpeedUnits.CENTIMETER_PER_SECOND.value))
    
    def test_div_units2(self):
        test_unit1 = LengthUnits.METER.value / TimeUnits.SECOND.value
        self.assertEqual(test_unit1,SpeedUnits.METER_PER_SECOND.value)
    
    def test_div_units3(self):
        test_unit1 = ForceUnits.NEWTON.value / AreaUnits.SQUARE_METER.value
        self.assertEqual(test_unit1,PressureUnits.PASCAL.value)
    
    def test_equal_units1(self):
        test_unit1 = MassFlowRateUnits.KILOGRAM_PER_MINUTE.value
        test_unit2 = MassUnits.KILOGRAM.value / TimeUnits.MINUTE.value
        self.assertTrue(test_unit1 == test_unit2)
    
    def test_equal_units2(self):
        test_unit1 = MassUnits.KILOGRAM.value * LengthUnits.METER.value / (TimeUnits.SECOND.value * TimeUnits.SECOND.value)
        self.assertTrue(test_unit1 == ForceUnits.NEWTON.value)
    
    def test_dimensionless_units1(self):
        test_unit1 = AreaUnits.SQUARE_METER.value * PressureUnits.PASCAL.value / ForceUnits.NEWTON.value
        self.assertTrue(test_unit1.is_dimensionless())
    
    def test_dimensionless_units2(self):
        test_unit1 = AngleUnits.RADIAN.value / AngleUnits.ARC_MINUTE.value
        self.assertTrue(test_unit1.is_dimensionless())
    
    
    # def test_div_dimension2(self):
    #     test_dim = MASS_DIMENSIONS / TIME_DIMENSIONS
    #     self.assertEqual(test_dim,MASS_FLOW_RATE_DIMENSIONS)
    
    # def test_div_dimension3(self):
    #     test_dim = VOLUME_DIMENSIONS / TIME_DIMENSIONS
    #     self.assertEqual(test_dim,FLOW_RATE_DIMENSIONS)
    
    
    
    # def test_pow_dimension1(self):
    #     test_dim = LENGTH_DIMENSIONS**1
    #     self.assertEqual(test_dim,LENGTH_DIMENSIONS)
    
    # def test_pow_dimension2(self):
    #     test_dim = LENGTH_DIMENSIONS**2
    #     self.assertEqual(test_dim,AREA_DIMENSIONS)
    
    # def test_str_dimension1(self):
    #     test_str = str(MASS_DIMENSIONS)
    #     self.assertEqual(test_str,'M')
    
    # def test_str_dimension2(self):
    #     test_str = str(MASS_FLOW_RATE_DIMENSIONS)
    #     self.assertEqual(test_str,'M*T^-1')
    
    # def test_str_dimension3(self):
    #     test_str = str(VOLTAGE_DIMENSIONS)
    #     self.assertEqual(test_str,'M*L^2*T^-3*I^-1')
    
    # def test_dimensionless1(self):
    #     test_dim = FORCE_DIMENSIONS/FORCE_DIMENSIONS
    #     self.assertEqual(test_dim.is_dimensionless(),True)
        
    # def test_dimensionless2(self):
    #     test_dim = CAPACITANCE_DIMENSIONS * FORCE_DIMENSIONS * LENGTH_DIMENSIONS * TIME_DIMENSIONS / (FORCE_DIMENSIONS * LENGTH_DIMENSIONS * TIME_DIMENSIONS * CAPACITANCE_DIMENSIONS)
    #     self.assertEqual(test_dim.is_dimensionless(),True)
    
    # def test_repr1(self):
    #     print(f'\nInductance dimensions: {repr(INDUCTANCE_DIMENSIONS)}')
    #     print(f'Magnetic field dimensions: {repr(MAGNETIC_FIELD_DIMENSIONS)}')
    #     print(f'Thermal conductivity dimensions: {repr(THERMAL_CONDUCTIVITY_DIMENSIONS)}')
    #     pass
        
        
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
    
    
    # def test_invalid_units(self):
    #     with self.assertRaises(ValueError):
    #         self.converter.convert(1, MockUnits.MOCK_UNIT.value, AngleUnits.DEGREE.value)
        
    #     with self.assertRaises(ValueError):
    #         self.converter.convert(1, AngleUnits.DEGREE.value, MockUnits.MOCK_UNIT.value)

if __name__ == '__main__':
    unittest.main()