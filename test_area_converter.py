import unittest
from modules.physical_quantities import BaseConversionManager


class TestAreaConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = BaseConversionManager("area")

    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            (250, "cm^2", "m^2", 0.025, 6),
            (1.5, "ft^2", "m^2", 0.13935, 4),
            (0.75, "yd^2", "m^2", 0.6271, 4),
            (5, "acre", "km^2", 0.020234, 4),
            (2.2, "km^2", "ha", 220, 3),
        ]
        for value, from_unit, to_unit, expected, decimal_places in test_cases:
            with self.subTest(value=value, from_unit=from_unit, to_unit=to_unit):
                try:
                    result = self.converter.convert(value, from_unit, to_unit)
                    self.assertAlmostEqual(
                        float(result), expected, places=decimal_places
                    )
                except AssertionError as e:
                    self.fail(
                        f"Conversion failed for {value} {from_unit} to {to_unit}. Expected {expected}, got {result}. Error: {e}"
                    )

    def test_invalid_units(self):
        with self.assertRaises(ValueError):
            self.converter.convert(1, "invalid_unit", "m^2")

        with self.assertRaises(ValueError):
            self.converter.convert(1, "m^2", "invalid_unit")


if __name__ == "__main__":
    unittest.main()
