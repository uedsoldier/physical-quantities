import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.power_budget import *
from modules.physical_quantities import *
from termcolor import colored

V = VoltageQuantity(5)
Imax = ElectricCurrentQuantity(2)
C = ElectricChargeQuantity(1000,'mAh')


# lipo = LithiumBattery(name='Batería',max_output_current=Imax,capacity=C,cell_count=9,subchemistry='LiPo')
# li_ion = LithiumBattery(name='Pila',max_output_current=Imax,capacity=Charge(C.value*2,C.unit),subchemistry='Li-ion')
# sensthys = LithiumBattery(name='SensThys',max_output_current=Imax,capacity=C,cell_voltage=Voltage(3.8),cell_count=9)
# life = LithiumBattery(name='LiFe',max_output_current=Current(4),capacity=Charge(5000,'mAh'),subchemistry='LiFePO4', cell_count=5)
pb = LeadAcidBattery(name='Plomo-ácido',max_output_current=ElectricCurrentQuantity(3.5),capacity=ElectricChargeQuantity(2,'Ah'),cell_count=6)

resistor = Component('Divisor resistivo',current=ElectricCurrentQuantity(2,'mA'),voltage=pb.nominal_voltage)    ## μ
led = Component('LEDs',current=ElectricCurrentQuantity(10,'mA'),voltage=pb.nominal_voltage)

pb.add_component(resistor,5)
pb.add_component(led,3)
pb.compute_power_budget()

# print(lipo)
# print(li_ion)
# print(sensthys)
# print(life)
print(colored(pb,'yellow'))

pb.modify_component_quantity(0,0)
pb.compute_power_budget()
print(colored(pb,'cyan'))
