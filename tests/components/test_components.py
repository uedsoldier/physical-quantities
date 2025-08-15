import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.physical_quantities import VoltageQuantity, ElectricCurrentQuantity, PowerQuantity
from core.unit import VoltageUnits, ElectricCurrentUnits, PowerUnits
from core.power_budget import Component

TEST_NAME='test_component'

TEST_VIP = [
            (VoltageQuantity(1.2),  ElectricCurrentQuantity(1,ElectricCurrentUnits.MILLIAMPERE.value), PowerQuantity(1.2,PowerUnits.MILLIWATT.value)),  # 1.2 V, 1 mA, 1.2 mW
            (VoltageQuantity(1.5),  ElectricCurrentQuantity(5,ElectricCurrentUnits.MILLIAMPERE.value),     PowerQuantity(7.5,PowerUnits.MILLIWATT.value)),  # 1.5 V, 5 mA, 7.5 mW
            (VoltageQuantity(1.8),  ElectricCurrentQuantity(10,ElectricCurrentUnits.MILLIAMPERE.value),     PowerQuantity(18,PowerUnits.MILLIWATT.value)),  # 1.8 V, 10 mA, 18 mW
            (VoltageQuantity(2.0),  ElectricCurrentQuantity(20,ElectricCurrentUnits.MILLIAMPERE.value),     PowerQuantity(40,PowerUnits.MILLIWATT.value)),  # 2.0 V, 20 mA, 40 mW
            (VoltageQuantity(3.3),  ElectricCurrentQuantity(100,ElectricCurrentUnits.MILLIAMPERE.value),     PowerQuantity(330,PowerUnits.MILLIWATT.value)),  # 3.3 V, 100 mA, 330 mW
            (VoltageQuantity(5.0),  ElectricCurrentQuantity(500,ElectricCurrentUnits.MILLIAMPERE.value),     PowerQuantity(2.5)),  # 5.0 V, 500 mA 2.5 W
            (VoltageQuantity(9.0),  ElectricCurrentQuantity(1.0),     PowerQuantity(9)),    # 9.0 V, 1 A, 9 W
            (VoltageQuantity(12.0), ElectricCurrentQuantity(5.0),     PowerQuantity(60)),    # 12.0 V, 5 A, 60 W
            (VoltageQuantity(24.0), ElectricCurrentQuantity(10.0),     PowerQuantity(240)),   # 24.0 V, 10 A, 240 W
            (VoltageQuantity(48.0), ElectricCurrentQuantity(20.0),     PowerQuantity(960)),   # 48.0 V, 20 A, 960 W
        ]

class ComponentsTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.voltages = [vip[0] for vip in TEST_VIP]
        cls.currents = [vip[1] for vip in TEST_VIP]
        cls.powers = [vip[2] for vip in TEST_VIP]

    def test_from_voltage_and_current(self):
        for test_V,test_I,test_P in TEST_VIP:
            component = Component(TEST_NAME,voltage=test_V,current=test_I)
            with self.subTest(power=test_P):
                self.assertAlmostEqual(component.power,test_P)

    def test_from_voltage_and_power(self):
        for test_V,test_I,test_P in TEST_VIP:
            component = Component(TEST_NAME,voltage=test_V,power=test_P)
            with self.subTest(current=test_I):
                self.assertAlmostEqual(component.current,test_I)

    def test_from_current_and_power(self):
        for test_V,test_I,test_P in TEST_VIP:
            component = Component(TEST_NAME,current=test_I,power=test_P)
            with self.subTest(voltage=test_V):
                self.assertAlmostEqual(component.voltage.value,test_V.value,delta=1e-15)

if __name__ == '__main__':
    unittest.main()