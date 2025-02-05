import sys
import os
import unittest
import subprocess
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.component_DAO import ComponentDAO
from modules.power_supply_DAO import PowerSupplyDAO
from modules.physical_quantities import VoltageQuantity, ElectricCurrentQuantity, ElectricChargeQuantity, PowerQuantity
from modules.unit import ElectricChargeUnits
from modules.power_supply import LeadAcidBattery

MOCK_DATABASE_FILENAME = 'mock_database.db'

class PowerSuppliesComponentsDAOTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BASE_PATH = Path.cwd()
        DAO_PATH: Path = BASE_PATH/'tests'/'DAO/'
        print(f'BASE path: {BASE_PATH}')
        print(f'DAO path: {DAO_PATH}')
        
        os.chdir(DAO_PATH)
        
        WINDOWS_SQL_SCRIPT_PATH = 'dao_init.bat'
        LINUX_SQL_SCRIPT_PATH = 'dao_init.sh'
        
        sql_script = WINDOWS_SQL_SCRIPT_PATH if sys.platform.startswith('win') else LINUX_SQL_SCRIPT_PATH
        print(f'SQL script: {sql_script}')
        if(os.path.exists(sql_script)):
            print('DAO init script will be executed')
            subprocess.run([sql_script],shell=True, check=True)
        else:
            print('Not found')
            raise FileNotFoundError(f'DAO init script <<{sql_script}>> does not exist.')

        cls.components_dao = ComponentDAO('./mock_database.db')
        cls.components_dao.create_table()
        cls.power_supplies_dao = PowerSupplyDAO('./mock_database.db')
        cls.power_supplies_dao.create_table()
        
        os.chdir(BASE_PATH)
        

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
        invalid_ids = [999, 1000]  # IDs que no existen en la base de datos
        for invalid_id in invalid_ids:
            with self.subTest(invalid_id=invalid_id):
                with self.assertRaises(ValueError):
                    self.power_supplies_dao.get_power_supply_voltage(invalid_id)

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
                actual_max_output_current = self.power_supplies_dao.get_power_supply_output_current(power_supply_id)
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
                actual_power_supply_id = self.components_dao.get_component_assigned_power_supply(component_id)
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
    
    def test_add_power_supply1(self):
        test_batt1 = LeadAcidBattery('testBattery',ElectricCurrentQuantity(2),ElectricChargeQuantity(1000,ElectricChargeUnits.MILLIAMPERE_HOUR.value),6)
        test_batt2 = LeadAcidBattery('testBattery',ElectricCurrentQuantity(1),ElectricChargeQuantity(500,ElectricChargeUnits.MILLIAMPERE_HOUR.value),3)
        self.power_supplies_dao.add_power_supply(test_batt1)
        self.power_supplies_dao.add_power_supply(test_batt2)
        test_current = ElectricCurrentQuantity(2)
        test_capacity = ElectricChargeQuantity(1000,ElectricChargeUnits.MILLIAMPERE_HOUR.value)
        
        ids = self.power_supplies_dao.get_power_supply_ids_by_name('testBattery')
        print(ids,len(ids))
        # self.assertEqual(test_current)
        # self.assertEqual(test_capacity)
    
if __name__ == '__main__':
    unittest.main()