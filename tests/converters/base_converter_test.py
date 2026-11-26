import unittest
from enum import Enum
from typing import TYPE_CHECKING, Any

from physical_quantities.units import Dimensions, Unit


class MockUnits(Enum):
    """Unit unknown to the library, used to test error handling."""

    MOCK_UNIT = Unit("mock unit", "mock", Dimensions({}))


if TYPE_CHECKING:
    _TestCaseBase = unittest.TestCase
else:
    _TestCaseBase = object


class BaseConversionTest(_TestCaseBase):
    """Mixin shared by all conversion tests.

    It is deliberately NOT a ``unittest.TestCase`` so the test loader never collects it on its
    own. Concrete tests inherit it together with ``unittest.TestCase``::

        class TestLengthConverter(BaseConversionTest, unittest.TestCase): ...
    """

    # Subclasses must override these attributes
    conversion_manager = None
    # Format: (value, from_unit, to_unit, expected_value, decimal_places)
    test_cases: list[tuple[float, Any, Any, float, int]] = []

    standard_unit = None

    def test_batch_conversions(self):
        self.assertIsNotNone(self.conversion_manager, "conversion_manager must be defined")
        self.assertTrue(self.test_cases, "test_cases must not be empty")

        for value, from_unit, to_unit, expected, decimal_places in self.test_cases:
            with self.subTest(value=value, from_u=from_unit, to_u=to_unit):
                result = float(self.conversion_manager.convert(value, from_unit, to_unit))
                self.assertAlmostEqual(
                    result,
                    expected,
                    places=decimal_places,
                    msg=f"\nConversion failed:\n"
                    f"   Input: {value} {from_unit}\n"
                    f"   Output: {result} {to_unit}\n"
                    f"   Expected: {expected}\n",
                )

    def test_invalid_units_generic(self):
        """Converting from/to an unknown unit must raise ValueError."""
        self.assertIsNotNone(self.conversion_manager, "conversion_manager must be defined")
        self.assertIsNotNone(self.standard_unit, "standard_unit must be defined")

        with self.assertRaises(ValueError, msg="Should fail converting to MockUnit"):
            self.conversion_manager.convert(1, self.standard_unit, MockUnits.MOCK_UNIT.value)

        with self.assertRaises(ValueError, msg="Should fail converting from MockUnit"):
            self.conversion_manager.convert(1, MockUnits.MOCK_UNIT.value, self.standard_unit)
