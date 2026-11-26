import unittest

from physical_quantities.quantities import (
    ElectricCurrentQuantity,
    FrequencyQuantity,
    LengthQuantity,
    ResistanceQuantity,
    TemperatureQuantity,
    VoltageQuantity,
)
from physical_quantities.units import (
    FrequencyUnits,
    LengthUnits,
    ResistanceUnits,
    TemperatureUnits,
    VoltageUnits,
)


class TestTemperatureQuantity(unittest.TestCase):

    def test_default_unit_is_kelvin(self):
        self.assertEqual(TemperatureUnits.KELVIN.value, TemperatureQuantity(10).unit)

    def test_celsius_to_kelvin(self):
        celsius = TemperatureQuantity(0, TemperatureUnits.CELSIUS.value)
        kelvin = celsius.convert_to(TemperatureUnits.KELVIN.value)
        self.assertIsInstance(kelvin, TemperatureQuantity)
        self.assertAlmostEqual(273.15, kelvin.value, places=6)
        self.assertEqual(TemperatureUnits.KELVIN.value, kelvin.unit)

    def test_fahrenheit_to_celsius(self):
        fahrenheit = TemperatureQuantity(212, TemperatureUnits.FAHRENHEIT.value)
        celsius = fahrenheit.convert_to(TemperatureUnits.CELSIUS.value)
        self.assertAlmostEqual(100.0, celsius.value, places=6)

    def test_same_unit_returns_a_copy(self):
        original = TemperatureQuantity(25, TemperatureUnits.CELSIUS.value)
        copy = original.convert_to(TemperatureUnits.CELSIUS.value)
        self.assertEqual(original, copy)
        self.assertIsNot(original, copy)

    def test_incompatible_unit_raises(self):
        with self.assertRaises(ValueError):
            TemperatureQuantity(1).convert_to(LengthUnits.METER.value)


class TestResistanceQuantity(unittest.TestCase):

    def test_can_be_created_and_converted(self):
        resistance = ResistanceQuantity(1000)
        converted = resistance.convert_to(ResistanceUnits.KILOHM.value)
        self.assertAlmostEqual(1.0, converted.value, places=9)
        self.assertEqual(ResistanceUnits.KILOHM.value, converted.unit)


class TestQuantityComparison(unittest.TestCase):

    def test_equal_across_compatible_units(self):
        self.assertEqual(
            LengthQuantity(1000, LengthUnits.MILLIMETER.value),
            LengthQuantity(1, LengthUnits.METER.value),
        )

    def test_ordering_across_compatible_units(self):
        self.assertLess(
            LengthQuantity(1, LengthUnits.FOOT.value), LengthQuantity(1, LengthUnits.YARD.value)
        )
        self.assertGreater(
            VoltageQuantity(1, VoltageUnits.KILOVOLT.value),
            VoltageQuantity(999, VoltageUnits.VOLT.value),
        )

    def test_equality_between_different_quantity_types_is_false(self):
        self.assertFalse(VoltageQuantity(1) == ElectricCurrentQuantity(1))
        self.assertTrue(VoltageQuantity(1) != ElectricCurrentQuantity(1))

    def test_ordering_between_different_quantity_types_raises(self):
        with self.assertRaises(TypeError):
            VoltageQuantity(1) < ElectricCurrentQuantity(2)
        with self.assertRaises(TypeError):
            VoltageQuantity(1) >= ElectricCurrentQuantity(2)

    def test_equality_with_non_quantity_is_false(self):
        self.assertFalse(VoltageQuantity(1) == 1)


class TestQuantityJsonSerialization(unittest.TestCase):

    def test_round_trip(self):
        original = VoltageQuantity(5, VoltageUnits.MILLIVOLT.value)
        restored = VoltageQuantity.from_json_string(original.to_json_string())
        self.assertEqual(original, restored)
        self.assertEqual(VoltageUnits.MILLIVOLT.value, restored.unit)

    def test_unicode_symbols_are_preserved(self):
        original = FrequencyQuantity(1, FrequencyUnits.KILOHERTZ.value)
        self.assertIn("kHz", original.to_json_string())
        original = ResistanceQuantity(4.7, ResistanceUnits.KILOHM.value)
        self.assertEqual(original, ResistanceQuantity.from_json_string(original.to_json_string()))

    def test_unknown_unit_symbol_raises(self):
        with self.assertRaises(ValueError):
            VoltageQuantity.from_json_string('{"value": 1, "unit": "not-a-unit"}')


if __name__ == "__main__":
    unittest.main()
