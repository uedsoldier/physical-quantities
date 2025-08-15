import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import random
import string

from core.power_supply_DAO import PowerSupplyDAO
from core.power_budget import LithiumBattery,LeadAcidBattery,BuckConverter,BoostConverter,BuckBoostConverter
from core.physical_quantities import VoltageQuantity, ElectricCurrentQuantity, ElectricChargeQuantity
def generate_random_id(length: int=6):
    # Choose from hexdigits
    characters = string.hexdigits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


power_supplies_dao = PowerSupplyDAO('./test_database.db')
power_supplies_dao.create_table()

possible_ps_types: list[str] = ['Battery','DCDC_Converter']  # 
possible_currents: list[float] = [0.25,0.5,1.0,2.0,5.0]

random_type: str = random.choice(possible_ps_types)
random_current_value: float =  random.choice(possible_currents)
random_current = VoltageQuantity(random_current_value,'A')
random_name: str = f'{random_type}'
match(random_type):
    case 'Battery':
        possible_cells: list[int] = [1,2,3,4,5,6]
        
        possible_capacities: list[float] = [250.0,500.0,1000.0,5000.0,10000.0]
        possible_battery_types: list[str] = ['Lithium','LeadAcid']
        
        random_battery_type = random.choice(possible_battery_types)
        random_name += f'-{random_battery_type}'
        random_cell_value: int =  random.choice(possible_cells)
        random_capacity_value: float = random.choice(possible_capacities)
        
        random_capacity = ElectricChargeQuantity(random_capacity_value,'mAh')
        
        match(random_battery_type):
            case 'Lithium':
                possible_subchemistries: list[str] = LithiumBattery.LITHIUM_CHEMISTRIES
                possible_subchemistries = [sc for sc in possible_subchemistries if sc != 'Other']
                random_subchemistry: str = random.choice(possible_subchemistries)
                random_name += f'-{random_subchemistry}-{generate_random_id()}'
                test_ps = LithiumBattery(f'{random_name}',random_current,random_capacity,cell_count=random_cell_value,subchemistry=random_subchemistry)

            case 'LeadAcid':
                possible_subchemistries: list[str] = [LeadAcidBattery.LEAD_ACID_SUBCHEMISTRY]
                random_subchemistry: str = random.choice(possible_subchemistries)
                random_name += f'-{generate_random_id()}'
                test_ps = LeadAcidBattery(f'{random_name}',random_current,random_capacity,cell_count=random_cell_value)
    case 'DCDC_Converter':
        possible_dcdc_types: list[str] = ['Buck' ,'Buck-Boost','Boost'] # 
        random_dcdc_type = random.choice(possible_dcdc_types)
        random_name += f'-{random_dcdc_type}-{generate_random_id()}'
        possible_efficiencies: list[float] = [0.85, 0.90, 0.95, 1.0]
        random_efficiency: float = random.choice(possible_efficiencies)
        
        match(random_dcdc_type):
            case 'Buck':
                output_voltage = VoltageQuantity(3.3)
                min_in = VoltageQuantity(12.0)
                max_in = VoltageQuantity(24.0)
                test_ps = BuckConverter(random_name,output_voltage,random_current,min_in,max_in,random_efficiency)
            case 'Boost':
                output_voltage = VoltageQuantity(32.0)
                min_in = VoltageQuantity(12.0)
                max_in = VoltageQuantity(24.0)
                test_ps = BoostConverter(random_name,output_voltage,random_current,min_in,max_in,random_efficiency)
            case 'Buck-Boost':
                output_voltage = VoltageQuantity(18.0)
                min_in = VoltageQuantity(12.0)
                max_in = VoltageQuantity(24.0)
                test_ps = BuckBoostConverter(random_name,output_voltage,random_current,min_in,max_in,random_efficiency)

            case _:
                pass
    case _:
        pass
    
    

print(test_ps)

power_supplies_dao.add_power_supply(test_ps)

# power_supplies_dao.truncate_table()


print(power_supplies_dao.get_power_supply_by_id(1))

power_supplies_dao.close()