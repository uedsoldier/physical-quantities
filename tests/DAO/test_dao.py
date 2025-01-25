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

        for power_supply_id, expected_voltage in test_cases:
            with self.subTest(power_supply_id=power_supply_id):
                actual_voltage = self.power_supplies_dao.get_voltage(power_supply_id)
                self.assertEqual(expected_voltage, actual_voltage)

    def test_invalid_ids(self):
        invalid_ids = [999, 1000]  # IDs que no existen en la base de datos
        for invalid_id in invalid_ids:
            with self.subTest(invalid_id=invalid_id):
                with self.assertRaises(ValueError):
                    self.power_supplies_dao.get_voltage(invalid_id)

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
                actual_max_output_current = self.power_supplies_dao.get_output_current(power_supply_id)
                self.assertEqual(expected_max_output_current, actual_max_output_current)
    
    def test_component_counts(self):
        test_cases = [
            (1,4),(2,3),(3,0),(4,0),(5,3),(6,0),(7,0),(8,1)
        ]
        for power_supply_id, component_count in test_cases:
            with self.subTest(power_supply_id=power_supply_id):
                actual_component_count = self.components_dao.get_components_count(power_supply_id)
                self.assertEqual(component_count, actual_component_count)

    def test_components_assigned_to_id(self):
        test_cases = [
            (1, None),  # Component-NULL1
            (2, None),  # Component-NULL2
            (3, None),  # Component-NULL3
            (4, 1),     # Component-FF12A3
            (5, 1),     # Component-AB34C5
            (6, 1),     # Component-9D45E6
            (7, 1),     # Component-A1B2C3
            (8, 2),     # Component-D4E5F6
            (9, 2),     # Component-E7F8G9
            (10, 2),    # Component-H1I2J3
            (11, 5),    # Component-F4G5H6
            (12, 5),    # Component-G7H8I9
            (13, 5),    # Component-K1L2M3
            (14, 8),    # Component-N4O5P6
        ]
        
        for component_id, power_supply_id in test_cases:
            with self.subTest(component_id=component_id):
                actual_power_supply_id = self.components_dao.get_assigned_power_supply(component_id)
                self.assertEqual(power_supply_id, actual_power_supply_id)
    
    def test_components_are_assigned(self):
        test_cases = [
            (1, False),  # Component-NULL1
            (2, False),  # Component-NULL2
            (3, False),  # Component-NULL3
            (4, True),     # Component-FF12A3
            (5, True),     # Component-AB34C5
            (6, True),     # Component-9D45E6
            (7, True),     # Component-A1B2C3
            (8, True),     # Component-D4E5F6
            (9, True),     # Component-E7F8G9
            (10, True),    # Component-H1I2J3
            (11, True),    # Component-F4G5H6
            (12, True),    # Component-G7H8I9
            (13, True),    # Component-K1L2M3
            (14, True),    # Component-N4O5P6
        ]
        
        for component_id, is_assigned in test_cases:
            with self.subTest(component_id=component_id):
                actual_assigned = self.components_dao.is_component_assigned(component_id)
                self.assertEqual(is_assigned, actual_assigned)
            
if __name__ == '__main__':
    unittest.main()