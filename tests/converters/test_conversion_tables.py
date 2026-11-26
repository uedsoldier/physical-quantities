import json
import unittest
from pathlib import Path

from physical_quantities.units import (
    UNIT_ENUM_BY_QUANTITY,
    find_unit_by_symbol,
    find_unit_type_by_symbol,
)

TABLES_DIR = Path(__file__).resolve().parents[2] / "src" / "physical_quantities" / "conversion_tables"
QUANTITY_TYPES = list(UNIT_ENUM_BY_QUANTITY)


def load_table(quantity_type: str) -> dict:
    return json.loads((TABLES_DIR / f"{quantity_type}.json").read_text(encoding="utf-8"))


class TestConversionTablesConsistency(unittest.TestCase):

    def test_every_quantity_type_has_a_table(self):
        for quantity_type in QUANTITY_TYPES:
            with self.subTest(quantity_type=quantity_type):
                self.assertTrue(
                    (TABLES_DIR / f"{quantity_type}.json").is_file(),
                    f"Missing conversion table for '{quantity_type}'",
                )

    def test_no_orphan_tables(self):
        table_names = {path.stem for path in TABLES_DIR.glob("*.json")}
        self.assertEqual(set(), table_names - set(QUANTITY_TYPES), "Tables without a unit enum")

    def test_table_symbols_match_the_unit_enum(self):
        for quantity_type in QUANTITY_TYPES:
            with self.subTest(quantity_type=quantity_type):
                table_symbols = set(load_table(quantity_type))
                enum_symbols = {m.value.symbol for m in UNIT_ENUM_BY_QUANTITY[quantity_type]}
                self.assertEqual(set(), enum_symbols - table_symbols, "Units missing in table")
                self.assertEqual(set(), table_symbols - enum_symbols, "Symbols without a unit")

    def test_linear_factors_are_positive_numbers(self):
        for quantity_type in QUANTITY_TYPES:
            if quantity_type == "temperature":  # affine conversion, checked separately
                continue
            for symbol, factor in load_table(quantity_type).items():
                with self.subTest(quantity_type=quantity_type, symbol=symbol):
                    self.assertIsInstance(factor, (int, float))
                    self.assertGreater(factor, 0)

    def test_every_table_has_a_base_unit_with_factor_one(self):
        for quantity_type in QUANTITY_TYPES:
            if quantity_type == "temperature":
                continue
            with self.subTest(quantity_type=quantity_type):
                self.assertIn(1, load_table(quantity_type).values())

    def test_temperature_table_entries_are_affine_parameters(self):
        for symbol, entry in load_table("temperature").items():
            with self.subTest(symbol=symbol):
                self.assertEqual({"pre_offset", "num", "den", "post_offset"}, set(entry))
                self.assertNotEqual(0, entry["num"])
                self.assertNotEqual(0, entry["den"])


class TestUnitSymbols(unittest.TestCase):

    def test_enums_have_no_aliased_members(self):
        # Enum silently turns two members with equal values into aliases (one hides the other).
        for quantity_type, enum_class in UNIT_ENUM_BY_QUANTITY.items():
            with self.subTest(quantity_type=quantity_type):
                self.assertEqual(len(enum_class.__members__), len(list(enum_class)))

    def test_symbols_are_unique_within_each_enum(self):
        for quantity_type, enum_class in UNIT_ENUM_BY_QUANTITY.items():
            with self.subTest(quantity_type=quantity_type):
                symbols = [m.value.symbol for m in enum_class.__members__.values()]
                self.assertEqual(len(symbols), len(set(symbols)))

    def test_symbols_are_unique_across_quantity_types(self):
        owner: dict[str, str] = {}
        for quantity_type, enum_class in UNIT_ENUM_BY_QUANTITY.items():
            for member in enum_class:
                symbol = member.value.symbol
                with self.subTest(symbol=symbol):
                    self.assertNotIn(
                        symbol, owner, f"'{symbol}' used by {owner.get(symbol)} and {quantity_type}"
                    )
                owner[symbol] = quantity_type

    def test_symbol_lookup_round_trip(self):
        for quantity_type, enum_class in UNIT_ENUM_BY_QUANTITY.items():
            for member in enum_class:
                with self.subTest(symbol=member.value.symbol):
                    self.assertIs(member.value, find_unit_by_symbol(member.value.symbol))
                    self.assertEqual(
                        quantity_type, find_unit_type_by_symbol(member.value.symbol)
                    )


if __name__ == "__main__":
    unittest.main()
