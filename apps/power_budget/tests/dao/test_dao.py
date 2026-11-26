import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from power_budget.component_dao import ComponentDAO
from power_budget import BuckConverter, Component, LeadAcidBattery
from power_budget.power_supply_dao import PowerSupplyDAO
from physical_quantities.quantities import (
    ElectricChargeQuantity,
    ElectricCurrentQuantity,
    PowerQuantity,
    VoltageQuantity,
)
from physical_quantities.units import ElectricChargeUnits

SQL_SCRIPT = Path(__file__).with_name("create_mock_database.sql")


class PowerSuppliesComponentsDAOTester(unittest.TestCase):
    """DAO tests against a fresh temporary SQLite database created for every test."""

    def setUp(self) -> None:
        self._tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp_dir.cleanup)
        self.db_path = str(Path(self._tmp_dir.name) / "mock_database.db")

        with closing(sqlite3.connect(self.db_path)) as connection:
            connection.executescript(SQL_SCRIPT.read_text(encoding="utf-8"))

        self.components_dao = ComponentDAO(self.db_path)
        self.addCleanup(self.components_dao.close)
        self.power_supplies_dao = PowerSupplyDAO(self.db_path)
        self.addCleanup(self.power_supplies_dao.close)

    def test_voltages(self):
        test_cases = [
            (1, VoltageQuantity(12.0)),
            (2, VoltageQuantity(5.0)),
            (3, VoltageQuantity(12.0)),
            (4, VoltageQuantity(6.0)),
            (5, VoltageQuantity(12.0)),
            (6, VoltageQuantity(24.0)),
            (7, VoltageQuantity(6.0)),
            (8, VoltageQuantity(14.4)),
            (9, VoltageQuantity(3.7)),
        ]

        for power_supply_id, expected_voltage in test_cases:
            with self.subTest(power_supply_id=power_supply_id):
                actual_voltage = self.power_supplies_dao.get_power_supply_voltage(power_supply_id)
                self.assertEqual(expected_voltage, actual_voltage)

    def test_invalid_ids(self):
        invalid_ids = [999, 1000, -1, 999]  # IDs that do not exist in the database
        for invalid_id in invalid_ids:
            with self.subTest(invalid_id=invalid_id):
                with self.assertRaises(ValueError):
                    self.power_supplies_dao.get_power_supply_voltage(invalid_id)
                with self.assertRaises(ValueError):
                    self.power_supplies_dao.get_power_supply_output_current(invalid_id)
                with self.assertRaises(ValueError):
                    self.power_supplies_dao.get_power_supply_by_id(invalid_id)

    def test_invalid_component_ids(self):
        for invalid_id in [999, 1000, -1]:
            with self.subTest(invalid_id=invalid_id):
                with self.assertRaises(ValueError):
                    self.components_dao.get_component_by_id(invalid_id)
                with self.assertRaises(ValueError):
                    self.components_dao.get_component_voltage(invalid_id)
                with self.assertRaises(ValueError):
                    self.components_dao.get_component_current(invalid_id)
                with self.assertRaises(ValueError):
                    self.components_dao.get_component_power(invalid_id)
                with self.assertRaises(ValueError):
                    self.components_dao.get_component_assigned_power_supply(invalid_id)
                with self.assertRaises(ValueError):
                    self.components_dao.is_component_assigned(invalid_id)

    def test_currents(self):
        test_cases = [
            (1, ElectricCurrentQuantity(10)),
            (2, ElectricCurrentQuantity(3.0)),
            (3, ElectricCurrentQuantity(10.0)),
            (4, ElectricCurrentQuantity(2.0)),
            (5, ElectricCurrentQuantity(5.0)),
            (6, ElectricCurrentQuantity(3.0)),
            (7, ElectricCurrentQuantity(5.0)),
            (8, ElectricCurrentQuantity(3.0)),
            (9, ElectricCurrentQuantity(1.0)),
        ]

        for power_supply_id, expected_max_output_current in test_cases:
            with self.subTest(power_supply_id=power_supply_id):
                actual = self.power_supplies_dao.get_power_supply_output_current(power_supply_id)
                self.assertEqual(expected_max_output_current, actual)

    def test_component_counts(self):
        test_cases = [(1, 4), (2, 3), (3, 0), (4, 0), (5, 3), (6, 0), (7, 0), (8, 1)]
        for power_supply_id, component_count in test_cases:
            with self.subTest(power_supply_id=power_supply_id):
                actual = self.components_dao.get_components_count(power_supply_id)
                self.assertEqual(component_count, actual)

    def test_components_assigned_to_id(self):
        test_cases = [
            (1, None),  # Component-NULL1
            (2, None),  # Component-NULL2
            (3, None),  # Component-NULL3
            (4, 1),  # Component-FF12A3
            (5, 1),  # Component-AB34C5
            (6, 1),  # Component-9D45E6
            (7, 1),  # Component-A1B2C3
            (8, 2),  # Component-D4E5F6
            (9, 2),  # Component-E7F8G9
            (10, 2),  # Component-H1I2J3
            (11, 5),  # Component-F4G5H6
            (12, 5),  # Component-G7H8I9
            (13, 5),  # Component-K1L2M3
            (14, 8),  # Component-N4O5P6
        ]

        for component_id, power_supply_id in test_cases:
            with self.subTest(component_id=component_id):
                actual = self.components_dao.get_component_assigned_power_supply(component_id)
                self.assertEqual(power_supply_id, actual)

    def test_components_are_assigned(self):
        unassigned_ids = {1, 2, 3}
        for component_id in range(1, 15):
            with self.subTest(component_id=component_id):
                actual = self.components_dao.is_component_assigned(component_id)
                self.assertEqual(component_id not in unassigned_ids, actual)

    def test_add_component(self):
        component = Component(
            "Component-NEW",
            voltage=VoltageQuantity(5.0),
            current=ElectricCurrentQuantity(0.1),
        )
        self.components_dao.add_component(component)

        new_id = 15  # The mock database already holds 14 components
        self.assertEqual("Component-NEW", self.components_dao.get_component_by_id(new_id)[1])
        self.assertEqual(VoltageQuantity(5.0), self.components_dao.get_component_voltage(new_id))
        self.assertEqual(
            ElectricCurrentQuantity(0.1), self.components_dao.get_component_current(new_id)
        )
        self.assertEqual(PowerQuantity(0.5), self.components_dao.get_component_power(new_id))
        self.assertFalse(self.components_dao.is_component_assigned(new_id))

    def test_assign_power_supply_updates_component_count(self):
        self.assertEqual(0, self.components_dao.get_components_count(3))
        self.components_dao.assign_power_supply_to_component(1, 3)

        self.assertEqual(3, self.components_dao.get_component_assigned_power_supply(1))
        self.assertEqual(1, self.components_dao.get_components_count(3))

    def test_add_power_supply_battery(self):
        batt1 = LeadAcidBattery(
            "testBattery",
            ElectricCurrentQuantity(2),
            ElectricChargeQuantity(1000, ElectricChargeUnits.MILLIAMPERE_HOUR.value),
            6,
        )
        batt2 = LeadAcidBattery(
            "testBattery",
            ElectricCurrentQuantity(1),
            ElectricChargeQuantity(500, ElectricChargeUnits.MILLIAMPERE_HOUR.value),
            3,
        )
        self.power_supplies_dao.add_power_supply(batt1)
        self.power_supplies_dao.add_power_supply(batt2)

        ids = self.power_supplies_dao.get_power_supply_ids_by_name("testBattery")
        self.assertEqual(2, len(ids))
        self.assertEqual(VoltageQuantity(12.0), self.power_supplies_dao.get_power_supply_voltage(ids[0]))
        self.assertEqual(VoltageQuantity(6.0), self.power_supplies_dao.get_power_supply_voltage(ids[1]))
        self.assertEqual(
            ElectricCurrentQuantity(2), self.power_supplies_dao.get_power_supply_output_current(ids[0])
        )

    def test_additional_information_is_valid_json(self):
        battery = LeadAcidBattery(
            "battery",
            ElectricCurrentQuantity(2),
            ElectricChargeQuantity(1000, ElectricChargeUnits.MILLIAMPERE_HOUR.value),
            6,
        )
        info = json.loads(self.power_supplies_dao.get_power_supply_additional_information(battery))
        self.assertEqual("Lead-Acid", info["chemistry"])
        self.assertEqual(6, info["cell_count"])
        self.assertEqual({"value": 2.0, "unit": "V"}, info["cell_voltage"])
        self.assertEqual({"value": 1000, "unit": "mAh"}, info["capacity"])

        buck = BuckConverter(
            "buck",
            VoltageQuantity(3.3),
            ElectricCurrentQuantity(1),
            VoltageQuantity(5),
            VoltageQuantity(12),
            0.9,
        )
        info = json.loads(self.power_supplies_dao.get_power_supply_additional_information(buck))
        self.assertEqual("Buck", info["dcdc_type"])
        self.assertEqual(0.9, info["efficiency"])
        self.assertEqual({"value": 12, "unit": "V"}, info["max_input_voltage"])

    def test_added_power_supply_is_stored_with_valid_json(self):
        battery = LeadAcidBattery(
            "json_battery",
            ElectricCurrentQuantity(2),
            ElectricChargeQuantity(1000, ElectricChargeUnits.MILLIAMPERE_HOUR.value),
            6,
        )
        self.power_supplies_dao.add_power_supply(battery)
        (power_supply_id,) = self.power_supplies_dao.get_power_supply_ids_by_name("json_battery")

        self.power_supplies_dao.cursor.execute(
            "SELECT additional_information FROM PowerSupplies WHERE power_supply_id = ?",
            (power_supply_id,),
        )
        (stored,) = self.power_supplies_dao.cursor.fetchone()
        self.assertEqual("Lead-Acid", json.loads(stored)["chemistry"])


if __name__ == "__main__":
    unittest.main()
