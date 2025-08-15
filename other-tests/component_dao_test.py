import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import random
import string

from core.component_DAO import ComponentDAO
from core.power_supply_DAO import PowerSupplyDAO
from core.power_budget import Component
from core.physical_quantities import VoltageQuantity, ElectricCurrentQuantity, ElectricChargeQuantity, PowerQuantity
from core.unit import ElectricCurrentUnits, VoltageUnits, ElectricChargeUnits, PowerUnits

def generate_random_id(length: int=6):
    # Choose from hexdigits
    characters = string.hexdigits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


components_dao = ComponentDAO('./test_database.db')
components_dao.create_table()
power_supplies_dao = PowerSupplyDAO('./test_database.db')
power_supplies_dao.create_table()

possible_component_types: list[str] = ['Resistor divider','LEDs']
possible_currents: list[float] = [1,2,5,10,20,50,100,250]


random_component_type: str = random.choice(possible_component_types)
random_current_value: float =  random.choice(possible_currents)
random_name: str = f'{random_component_type}-{generate_random_id()}'

test_voltage = power_supplies_dao.get_power_supply_voltage(1)
test_component = Component(random_name,current=ElectricCurrentQuantity(random_current_value,ElectricCurrentUnits.MILLIAMPERE.value),voltage=test_voltage)

print(test_component)

components_dao.add_component(test_component)

id: int = 1
components_dao.assign_power_supply_to_component(1,id)

components = components_dao.get_components_list(id)
components_qty = len(components)
print(f'Components with power supply id = {id}: {components_qty}')
print(components)

# # power_supplies_dao.truncate_table()

components_dao.close()