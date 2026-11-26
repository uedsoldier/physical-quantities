import unittest
from math import pi

from physical_quantities.electrical import AC_Voltage, normalize_phase
from physical_quantities.quantities import AngleQuantity, FrequencyQuantity, VoltageQuantity
from physical_quantities.units import AngleUnits


class TestNormalizePhase(unittest.TestCase):

    def test_degrees_are_wrapped_to_half_open_range(self):
        # (input degrees, expected degrees) -> the range is (-180, 180]
        cases = [
            (0, 0),
            (45, 45),
            (180, 180),
            (-180, 180),
            (270, -90),
            (360, 0),
            (540, 180),
            (-270, 90),
        ]
        for degrees, expected in cases:
            with self.subTest(degrees=degrees):
                result = normalize_phase(AngleQuantity(degrees, AngleUnits.DEGREE.value))
                self.assertAlmostEqual(expected, result.value, places=6)
                self.assertEqual(AngleUnits.DEGREE.value, result.unit)

    def test_radians_keep_their_unit(self):
        result = normalize_phase(AngleQuantity(1.5 * pi, AngleUnits.RADIAN.value))
        self.assertAlmostEqual(-0.5 * pi, result.value, places=9)
        self.assertEqual(AngleUnits.RADIAN.value, result.unit)

    def test_input_is_not_modified(self):
        angle = AngleQuantity(270, AngleUnits.DEGREE.value)
        normalize_phase(angle)
        self.assertEqual(270, angle.value)


class TestAcVoltage(unittest.TestCase):

    def test_default_phase_is_zero(self):
        ac_voltage = AC_Voltage(VoltageQuantity(120), FrequencyQuantity(60))
        self.assertEqual(0, ac_voltage._phase_angle.value)

    def test_phase_is_normalized_without_touching_the_argument(self):
        phase = AngleQuantity(270, AngleUnits.DEGREE.value)
        ac_voltage = AC_Voltage(VoltageQuantity(120), FrequencyQuantity(60), phase)
        self.assertAlmostEqual(-90, ac_voltage._phase_angle.value, places=6)
        self.assertEqual(270, phase.value)

    def test_amplitude_is_rms_times_sqrt2(self):
        ac_voltage = AC_Voltage(VoltageQuantity(100), FrequencyQuantity(50))
        self.assertAlmostEqual(141.42135623, ac_voltage._amplitude.value, places=6)

    def test_non_positive_frequency_raises(self):
        for frequency in (0, -50):
            with self.subTest(frequency=frequency):
                with self.assertRaises(ValueError):
                    AC_Voltage(VoltageQuantity(120), FrequencyQuantity(frequency))

    def test_str(self):
        text = str(AC_Voltage(VoltageQuantity(120), FrequencyQuantity(60)))
        self.assertIn("120 [V] RMS", text)


if __name__ == "__main__":
    unittest.main()
