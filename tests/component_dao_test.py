import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
import string

from modules.component_DAO import ComponentDAO
from modules.power_supply_DAO import PowerSupplyDAO
from modules.power_budget import Component
from modules.physical_quantities import Voltage, Current, Charge, Power

def generate_random_id(length: int=6):
    # Choose from letters and digits
    characters = string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


components_dao = ComponentDAO('./test_database.db')
components_dao.create_table()
power_supplies_dao = PowerSupplyDAO('./test_database.db')
power_supplies_dao.create_table()

possible_component_types: list[str] = ['Resistor divider','LEDs']
possible_currents: list[float] = [0.1]
possible_powers: list[float] = [1]


random_component_type: str = random.choice(possible_component_types)
random_current_value: float =  random.choice(possible_currents)
random_power_value: float = random.choice(possible_powers)
random_name: str = f'{random_component_type}'

test_component = Component(random_name,current=Current(random_current_value,'mA'),power=Power(random_power_value,'mW'))


print(test_component)

components_dao.add_component(test_component)

components_dao.assign_power_supply(1,1)

print(components_dao.get_components_by_power_supply(1))

# power_supplies_dao.truncate_table()

components_dao.close()