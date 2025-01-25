import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.component_DAO import ComponentDAO
from modules.power_supply_DAO import PowerSupplyDAO
from modules.physical_quantities import VoltageQuantity, ElectricCurrentQuantity

class PowerSuppliesDAOTester(unittest.TestCase):
    def setUp(self) -> None:
        self.components_dao = ComponentDAO('./tests/DAO/mock_database.db')
        self.components_dao.create_table()
        self.power_supplies_dao = PowerSupplyDAO('./tests/DAO/mock_database.db')
        self.power_supplies_dao.create_table()
        return super().setUp()

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

        for id, expected_voltage in test_cases:
            with self.subTest(id=id):
                actual_voltage = self.power_supplies_dao.get_power_supply_voltage(id)
                self.assertEqual(expected_voltage, actual_voltage)

    def test_invalid_ids(self):
        invalid_ids = [999, 1000]  # IDs que no existen en la base de datos
        for id in invalid_ids:
            with self.subTest(id=id):
                with self.assertRaises(ValueError):
                    self.power_supplies_dao.get_power_supply_voltage(id)

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

        for id, expected_max_output_current in test_cases:
            with self.subTest(id=id):
                actual_max_output_current = self.power_supplies_dao.get_power_supply_output_current(id)
                self.assertEqual(expected_max_output_current, actual_max_output_current)

if __name__ == '__main__':
    unittest.main()