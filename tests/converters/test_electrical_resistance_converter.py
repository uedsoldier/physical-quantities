import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import ResistanceUnits, MockUnits


class TestElectricalResistanceConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = BaseConversionManager("electrical_resistance")

    def test_conversion(self):
        # Test cases: (input value, input unit, output unit,expected value, decimal places)
        test_cases = [
            # Ohms to Milliohms
            (
                1.0,
                ResistanceUnits.OHM.value,
                ResistanceUnits.MILLIOHM.value,
                1e3,
                6,
            ),  # 1 Ω = 1000 mΩ
            # Milliohms to Ohms
            (
                1e3,
                ResistanceUnits.MILLIOHM.value,
                ResistanceUnits.OHM.value,
                1.0,
                6,
            ),  # 1000 mΩ = 1 Ω
            # Ohms to Microohms
            (
                1,
                ResistanceUnits.OHM.value,
                ResistanceUnits.MICROOHM.value,
                1e6,
                6,
            ),  # 1 Ω = 1,000,000 μΩ
            # Microohms to Ohms
            (
                1e6,
                ResistanceUnits.MICROOHM.value,
                ResistanceUnits.OHM.value,
                1.0,
                6,
            ),  # 1,000,000 μΩ = 1 Ω
            # Ohms to Kiloohms
            (
                1,
                ResistanceUnits.OHM.value,
                ResistanceUnits.KILOHM.value,
                1e-3,
                6,
            ),  # 1 Ω = 0.001 kΩ
            # Kiloohms to Ohms
            (
                1.0,
                ResistanceUnits.KILOHM.value,
                ResistanceUnits.OHM.value,
                1e3,
                6,
            ),  # 1kΩ = 1000  Ω
            # Ohms to Megaohms
            (
                1,
                ResistanceUnits.OHM.value,
                ResistanceUnits.MEGAOHM.value,
                1e-6,
                6,
            ),  # 1 Ω = 0.000001 MΩ
            # Megaohms to Ohms
            (
                1.0,
                ResistanceUnits.MEGAOHM.value,
                ResistanceUnits.OHM.value,
                1.0e6,
                6,
            ),  # 1 MΩ = 1,000,000 Ω
            # Ohms to Gigaohms
            (
                1e9,
                ResistanceUnits.OHM.value,
                ResistanceUnits.GIGOHM.value,
                1,
                6,
            ),  # 1 Ω = 0.000000001 GΩ
            # Gigaohms to Ohms
            (
                1,
                ResistanceUnits.GIGOHM.value,
                ResistanceUnits.OHM.value,
                1.0e9,
                6,
            ),  # 1 GΩ = 1,000,000,000 Ω
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
            self.converter.convert(
                1, MockUnits.MOCK_UNIT.value, ResistanceUnits.OHM.value
            )

        with self.assertRaises(ValueError):
            self.converter.convert(
                1, ResistanceUnits.OHM.value, MockUnits.MOCK_UNIT.value
            )


if __name__ == "__main__":
    unittest.main()
