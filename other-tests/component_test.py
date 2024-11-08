import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from modules.power_budget import Component, DCPowerSupply, PowerBudget
from modules.physical_quantities import VoltageQuantity, ElectricCurrentQuantity, PowerQuantity, EnergyQuantity, TimeQuantity

voltage = VoltageQuantity(5.0)
current = ElectricCurrentQuantity(5,'mA')

cmp1 = Component.from_voltage_current('LED_VI',voltage,current)
power = cmp1.power
print(cmp1)
print(f'power conversion of {cmp1.name}: {cmp1.power.convert_to('mW')}')

voltage.value = 10
power = PowerQuantity(0.025,'W')

cmp2 = Component.from_voltage_power('LED_PV',voltage,power)
cmp2.current = cmp2.current.convert_to('mA')
print(cmp2)
print(f'current conversion of {cmp2.name}: {cmp2.current.convert_to('mA')}')


t = TimeQuantity(1,'year')

bat_voltage = VoltageQuantity(12.0)
bat_max_current = ElectricCurrentQuantity(500,'mA')

battery = DCPowerSupply(name='Battery',supply_type='Battery',supply_subtype='Pb',output_voltage=bat_voltage,max_output_current=bat_max_current,components=[cmp1,cmp2])


print(f'this component will consume {cmp2.energy_consumption(t).convert_to('kWh')} in {t}')

print(battery)
battery.remove_component('LED_VI')
print(battery)

budget = PowerBudget('test')

budget.add_component(cmp1,2)
budget.add_component(cmp2,5)

budget.add_power_supply(battery)

print(budget)

