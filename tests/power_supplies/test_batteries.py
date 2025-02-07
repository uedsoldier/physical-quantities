import sys
import os
import unittest
from typing import List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.physical_quantities import VoltageQuantity, ElectricCurrentQuantity, PowerQuantity, ElectricChargeQuantity
from modules.unit import VoltageUnits, ElectricCurrentUnits, PowerUnits, ElectricChargeUnits
from modules.power_budget import LeadAcidBattery, LithiumBattery

class LeadAcidBatteriesTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass
    
    def setUp(self):
        return super().setUp()
    
    def test_voltages(self):
        TEST_LEAD_ACID_BATTERIES: List[Tuple[ElectricCurrentQuantity,ElectricChargeUnits,int,VoltageQuantity]] = [
            (ElectricCurrentQuantity(2), ElectricChargeQuantity(5000,ElectricChargeUnits.MILLIAMPERE_HOUR.value), 6, VoltageQuantity(12.0)),
            (ElectricCurrentQuantity(1), ElectricChargeQuantity(2000,ElectricChargeUnits.MILLIAMPERE_HOUR.value), 3, VoltageQuantity(6.0))
        ]

        for current,charge,cell_count,voltage in TEST_LEAD_ACID_BATTERIES:
            battery = LeadAcidBattery('test_leadAcid_battery',current,charge,cell_count)
            with self.subTest(voltage=voltage):
                self.assertEqual(voltage,battery.nominal_voltage)
                
class LithiumBatteriesTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass
    
    def setUp(self):
        return super().setUp()
    
    def test_voltages(self):
        TEST_LITHIUM_BATTERIES: List[Tuple[ElectricCurrentQuantity,ElectricChargeUnits,int,str,VoltageQuantity]] = [
            (ElectricCurrentQuantity(2), ElectricChargeQuantity(5000,ElectricChargeUnits.MILLIAMPERE_HOUR.value), 1, 'LiPo',VoltageQuantity(3.7)),
            (ElectricCurrentQuantity(1), ElectricChargeQuantity(2000,ElectricChargeUnits.MILLIAMPERE_HOUR.value), 2, 'Li-ion',VoltageQuantity(7.2))
        ]

        for current,charge,cell_count,subchemistry,voltage in TEST_LITHIUM_BATTERIES:
            battery = LithiumBattery('test_lithium_battery',current,charge,cell_count=cell_count,subchemistry=subchemistry)
            with self.subTest(voltage=voltage):
                self.assertEqual(voltage,battery.nominal_voltage)
                
if __name__ == '__main__':
    unittest.main()