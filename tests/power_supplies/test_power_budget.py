import unittest

from physical_quantities.quantities import (
    ElectricChargeQuantity,
    ElectricCurrentQuantity,
    VoltageQuantity,
)
from core.power_budget import (
    BuckConverter,
    Component,
    LeadAcidBattery,
    LinearRegulator,
    PowerBudget,
)
from physical_quantities.units import ElectricChargeUnits, ElectricCurrentUnits, PowerUnits


def make_battery() -> LeadAcidBattery:
    """6-cell lead-acid battery -> 12 V nominal."""
    return LeadAcidBattery(
        "battery",
        ElectricCurrentQuantity(5),
        ElectricChargeQuantity(5000, ElectricChargeUnits.MILLIAMPERE_HOUR.value),
        6,
    )


def make_component(name: str = "load", volts: float = 5.0, amps: float = 0.1) -> Component:
    return Component(name, voltage=VoltageQuantity(volts), current=ElectricCurrentQuantity(amps))


def make_buck(efficiency: float | None = None) -> BuckConverter:
    kwargs = {} if efficiency is None else {"efficiency": efficiency}
    return BuckConverter(
        "buck",
        VoltageQuantity(3.3),
        ElectricCurrentQuantity(1),
        VoltageQuantity(5),
        VoltageQuantity(12),
        **kwargs,
    )


class TestComponent(unittest.TestCase):

    def test_power_supply_defaults_to_none(self):
        self.assertIsNone(make_component().power_supply)

    def test_power_supply_can_be_assigned(self):
        component = make_component()
        battery = make_battery()
        component.power_supply = battery
        self.assertIs(battery, component.power_supply)

    def test_str(self):
        self.assertEqual(
            "Component name: load V=5.0 [V] I=0.1 [A] P=0.5 [W]", str(make_component())
        )

    def test_requires_two_parameters(self):
        with self.assertRaises(ValueError):
            Component("invalid", voltage=VoltageQuantity(5))


class TestPowerSupplyBudget(unittest.TestCase):

    def test_totals_start_at_zero(self):
        battery = make_battery()
        self.assertEqual(0.0, battery.total_current.value)
        self.assertEqual(0.0, battery.total_power.value)

    def test_add_component_updates_budget(self):
        battery = make_battery()
        battery.add_component(make_component(amps=0.1), 2)  # 2 x 100 mA

        self.assertAlmostEqual(200.0, battery.total_current.value, places=6)
        self.assertEqual(ElectricCurrentUnits.MILLIAMPERE.value, battery.total_current.unit)
        self.assertAlmostEqual(2400.0, battery.total_power.value, places=6)  # 200 mA * 12 V
        self.assertEqual(PowerUnits.MILLIWATT.value, battery.total_power.unit)
        self.assertEqual(2, battery.total_components)

    def test_components_with_different_units_are_added_correctly(self):
        battery = make_battery()
        battery.add_component(
            Component(
                "small",
                voltage=VoltageQuantity(3.3),
                current=ElectricCurrentQuantity(10, ElectricCurrentUnits.MILLIAMPERE.value),
            )
        )
        battery.add_component(make_component(amps=0.1))
        self.assertAlmostEqual(110.0, battery.total_current.value, places=6)

    def test_modify_and_remove_component(self):
        battery = make_battery()
        battery.add_component(make_component(amps=0.1), 1)

        battery.modify_component_quantity(0, 3)
        self.assertAlmostEqual(300.0, battery.total_current.value, places=6)

        battery.modify_component_quantity(0, 0)
        self.assertEqual(0, len(battery.components))
        self.assertEqual(0.0, battery.total_current.value)

    def test_modify_invalid_index_raises(self):
        with self.assertRaises(IndexError):
            make_battery().modify_component_quantity(3, 1)

    def test_remove_from_empty_raises(self):
        with self.assertRaises(ValueError):
            make_battery().remove_component(0)


class TestRegulators(unittest.TestCase):

    def test_linear_regulator_can_be_instantiated(self):
        regulator = LinearRegulator(
            "ldo",
            VoltageQuantity(3.3),
            ElectricCurrentQuantity(1),
            VoltageQuantity(5),
            VoltageQuantity(12),
        )
        self.assertAlmostEqual(3.3 / 12, regulator.efficiency, places=9)

    def test_linear_regulator_accepts_explicit_efficiency(self):
        regulator = LinearRegulator(
            "ldo",
            VoltageQuantity(3.3),
            ElectricCurrentQuantity(1),
            VoltageQuantity(5),
            VoltageQuantity(12),
            efficiency=0.5,
        )
        self.assertEqual(0.5, regulator.efficiency)

    def test_buck_converter_budget(self):
        buck = make_buck()
        buck.add_component(make_component(volts=3.3, amps=0.1))
        self.assertAlmostEqual(100.0, buck.total_current.value, places=6)
        self.assertAlmostEqual(330.0, buck.total_power.value, places=6)  # 100 mA * 3.3 V
        self.assertIn("Buck converter name: buck", str(buck))

    def test_invalid_efficiency_raises(self):
        with self.assertRaises(ValueError):
            make_buck(efficiency=1.5)


class TestPowerBudget(unittest.TestCase):

    def test_add_and_remove(self):
        budget = PowerBudget("system")
        budget.add_component(make_component(), 2)
        budget.add_power_supply(make_battery())
        self.assertEqual(1, len(budget.components))
        self.assertEqual(1, len(budget.dc_power_supplies))

        budget.remove_component(0)
        budget.remove_power_supply(0)
        self.assertEqual([], budget.components)
        self.assertEqual([], budget.dc_power_supplies)

    def test_remove_invalid_index_raises(self):
        budget = PowerBudget("system")
        with self.assertRaises(IndexError):
            budget.remove_component(0)
        with self.assertRaises(IndexError):
            budget.remove_power_supply(0)


if __name__ == "__main__":
    unittest.main()
