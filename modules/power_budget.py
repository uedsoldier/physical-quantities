from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from .physical_quantities import ElectricCurrentQuantity, PowerQuantity, VoltageQuantity, TimeQuantity, EnergyQuantity, ElectricChargeQuantity
from .utilities.json_utilities import json_to_dict
from .unit import ElectricCurrentUnits, PowerUnits, VoltageUnits, TimeUnits, EnergyUnits, ElectricChargeUnits
import os

class Component:
    
    def __str__(self) -> str:
        return(f'{self.name}: {self.voltage}, {self.current}, {self.power}')
    
    @classmethod
    def from_voltage_current(cls, name: str, voltage: VoltageQuantity, current: ElectricCurrentQuantity):
        return cls(name, voltage=voltage, current=current)

    @classmethod
    def from_voltage_power(cls, name: str, voltage: VoltageQuantity, power: PowerQuantity):
        return cls(name, voltage=voltage, power=power)

    @classmethod
    def from_current_power(cls, name: str, current: ElectricCurrentQuantity, power: PowerQuantity):
        return cls(name, current=current, power=power)
    
    """_summary_
    """
    def __init__(self, name: str, voltage:VoltageQuantity = None, current:ElectricCurrentQuantity = None, power:PowerQuantity = None, power_supply: BasePowerSupply = None) -> None:
        self._name: str = name
        self._voltage: VoltageQuantity = voltage
        self._current: ElectricCurrentQuantity = current
        self._power: PowerQuantity = power
        self._power_supply: BasePowerSupply = power_supply
        
        if (voltage is not None and current is not None):
            self.compute_power()
        elif(voltage is not None and power is not None):
            self.compute_current()
        elif(current is not None and power is not None):
            self.compute_voltage()
        else:
            raise ValueError('At least two parameters (voltage, current, power) must be provided.')
        
        
    def energy_consumption(self, t: TimeQuantity) -> EnergyQuantity:
        return EnergyQuantity( self.power.convert_to(PowerUnits.WATT.value).value * t.convert_to(TimeUnits.SECOND.value).value )
    
    def compute_power(self):
        self.power =  PowerQuantity(self.voltage.convert_to(VoltageUnits.VOLT.value).value * self.current.convert_to(ElectricCurrentUnits.AMPERE.value).value )
    
    def compute_current(self):
        self.current = ElectricCurrentQuantity(self.power.convert_to(PowerUnits.WATT.value).value / self.voltage.convert_to(VoltageUnits.VOLT.value).value)
        
    def compute_voltage(self):
        self.voltage = VoltageQuantity(self.power.convert_to(PowerUnits.WATT.value).value / self.current.convert_to(ElectricCurrentUnits.AMPERE.value).value)
    
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @property
    def voltage(self) -> VoltageQuantity:
        return self._voltage

    @voltage.setter
    def voltage(self, value: VoltageQuantity) -> None:
        if not isinstance(value, VoltageQuantity) and value is not None:
            raise ValueError("Voltage must be of type Voltage")
        self._voltage = value

    @property
    def current(self) -> ElectricCurrentQuantity:
        return self._current

    @current.setter
    def current(self, value: ElectricCurrentQuantity) -> None:
        if not isinstance(value, ElectricCurrentQuantity) and value is not None:
            raise ValueError("Current must be of type Current")
        self._current = value

    @property
    def power(self) -> PowerQuantity:
        return self._power

    @power.setter
    def power(self, value: PowerQuantity) -> None:
        if not isinstance(value, PowerQuantity) and value is not None:
            raise ValueError("Power must be of type Power")
        self._power = value
    
    @property
    def power_supply(self) -> BasePowerSupply:
        return self.power_supply

    @power_supply.setter
    def power_supply(self, new_power_supply: BasePowerSupply) -> None:
        if not isinstance(new_power_supply, BasePowerSupply):
            raise ValueError("new_power_supply must be a BasePowerSupply")
        self._power_supply = new_power_supply
    
    def __str__(self) -> str:
        return f'Component name: {self.name} V={self.voltage} I={self.current} P={self.power}'
    

# class DCPowerSupply():
    
#     def __init__(self, name: str ,supply_type: str, supply_subtype:str,output_voltage: Voltage, max_output_current: Current, min_input_voltage: Voltage = 0, max_input_voltage: Voltage = 0, efficiency: float = None, components: Component=None, comment: str = '') -> None:
#         """_summary_

#         Args:
#             name (str): _description_
#             supply_type (str): _description_
#             supply_subtype (str): _description_
#             output_voltage (Voltage): _description_
#             max_output_current (Current): _description_
#             min_input_voltage (Voltage, optional): _description_. Defaults to 0.
#             max_input_voltage (Voltage, optional): _description_. Defaults to 0.
#             efficiency (float, optional): _description_. Defaults to None.
#             components (Component, optional): _description_. Defaults to None.
#             comment (str, optional): _description_. Defaults to ''.

#         Raises:
#             ValueError: _description_
#             ValueError: _description_
#         """
#         filename: str = './power_supplies.json'
#         filepath: str = os.path.join(os.path.dirname(__file__), filename)
#         power_suppply_dict: dict = json_to_dict(filepath)
#         print(power_suppply_dict)
        
#         if(supply_type not in power_suppply_dict.keys()):
#             raise ValueError('Invalid DC power supply type.')
        
#         if(supply_subtype not in power_suppply_dict[supply_type]):
#             raise ValueError(f'Invalid {supply_type} subtype: {supply_subtype}')
            
        
        
#         self._supply_type = supply_type
#         self._name = name
#         self._output_voltage = output_voltage
#         self._max_output_current = max_output_current
#         self._min_input_voltage = min_input_voltage
#         self._max_input_voltage = max_input_voltage
#         self._efficiency = efficiency
#         self._comment: str = comment or ''
        
#         if components is None:
#             self._components: List = [Component]
#         elif isinstance(components,List) and all(isinstance(comp, Component) for comp in components):
#             self._components = components
#         else:
#             raise ValueError('Components must be a list of Component objects.')
    
#     @property
#     def supply_type(self):
#         """_summary_

#         Returns:
#             _type_: _description_
#         """
#         return self._supply_type
    
#     @supply_type.setter
#     def supply_type(self, supply_type: Voltage):
#         """_summary_

#         Args:
#             supply_type (Voltage): _description_
#         """
#         self._supply_type = supply_type
    
    
    
#     @property
#     def output_voltage(self):
#         """_summary_

#         Returns:
#             _type_: _description_
#         """
#         return self._output_voltage
    
#     @output_voltage.setter
#     def output_voltage(self, output_voltage: Voltage):
#         """_summary_

#         Args:
#             output_voltage (float): _description_
#         """
#         self._output_voltage = output_voltage
        
    
#     def add_component(self, component: Component):
#         """_summary_

#         Args:
#             component (CircuitBase): _description_
#         """
#         if(component.power_supply is not self):
#             raise ValueError('Component is associated with a different power supply.')
#         self.components.append(component)
    
#     def remove_component(self, component_name:str):
#         """_summary_

#         Args:
#             component_name (str): _description_
#         """
#         self._components = [comp for comp in self._components if comp.name != component_name]
    
    
    
#     def __str__(self) -> str:
#         """_summary_

#         Returns:
#             str: _description_
#         """
#         attrs = [f'{key}: {value}' for key, value in self.__dict__.items()]
#         return('Power Supply Settings:\n' + '\n'.join(attrs))

class BasePowerSupply(ABC):
    
    def __init__(self, name: str, nominal_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity) -> None:
        self._name = name
        self._nominal_voltage = nominal_voltage
        self._max_output_current = max_output_current
        self._components: List[List[Component,int]] = []
        self._total_current: ElectricCurrentQuantity = ElectricCurrentQuantity(0.0,'mA')
        self._total_power: PowerQuantity = PowerQuantity(0.0,'mW')
        self._total_components: int = 0
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self,new_name: str):
        self._name = new_name
    
    @property
    def total_components(self) -> int :
        cnt: int = 0
        for component_type in self.components:
            cnt += component_type[1]
        return cnt
    
    @property
    def components(self) -> List[List[Component,int]]:
        return self._components
    
    @property
    def nominal_voltage(self):
        return self._nominal_voltage

    @nominal_voltage.setter
    def nominal_voltage(self,new_nominal_voltage: VoltageQuantity):
        self._nominal_voltage = new_nominal_voltage
    
    @property
    def max_output_current(self):
        return self._max_output_current

    @max_output_current.setter
    def max_output_current(self,new_max_output_current: ElectricCurrentQuantity):
        self._max_output_current = new_max_output_current
    
    def add_component(self, component: Component, quantity: int = 1):
        self._components.append((component,quantity))
        self.compute_power_budget()
    
    def remove_component(self,index: int):
        if(len(self.components) > 0):
            self.components.pop(index)
            self.compute_power_budget()
        else:
            raise ValueError('Component index not found')
    
    def modify_component_quantity(self,index: int, new_qty: int):
        # Check if the index is valid
        if 0 <= index < len(self.components):
            if new_qty == 0:
                self.remove_component(index)
            else:
                # Update the quantity in the tuple
                component, _ = self.components[index]
                self.components[index] = (component, new_qty)
            self.compute_power_budget()
        else:
            raise IndexError("Component index out of range.")
        
    def compute_power_budget(self):
        normalized_current: float = 0
        normalized_power: float = 0
        normalized_voltage = VoltageQuantity.convert_to(self.nominal_voltage,'V').value
        for component_type in self.components:
            component: Component = component_type[0]
            component_qty: int = component_type[1]
            component_current_value: float = ElectricCurrentQuantity.convert_to(component.current,'mA').value
            normalized_current += component_current_value * component_qty
        
        normalized_power = normalized_current * normalized_voltage
        self._total_current.unit = 'mA'
        self._total_current.value = normalized_current
        self._total_power.unit = 'mW'
        self._total_power.value = normalized_power 
        
        
        
    @property
    def total_current(self) -> ElectricCurrentQuantity:
        return self._total_current

    @property
    def total_power(self) -> PowerQuantity:
        return self._total_power
    
    @abstractmethod
    def _restrict_instantiation(self):
        pass

class Battery(BasePowerSupply):
    def __init__(self, name: str,chemistry: str,cell_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity, capacity: ElectricChargeQuantity, subchemistry: str, cell_count: int = 1, ) -> None:
        if(cell_count <= 0):
            raise ValueError('Cell number must be a positive integer')
        if(cell_voltage.value < 0.0):
            raise ValueError('Cell voltage must be a positive floating-point value')
        if(capacity.value < 0.0):
            raise ValueError('Battery capacity must be a positive floating-point value')
        self._cell_count = cell_count
        self._capacity = capacity
        self._cell_voltage = cell_voltage
        self._chemistry = chemistry
        self._subchemistry = subchemistry
        nominal_voltage_value = cell_count * cell_voltage.value
        nominal_voltage_units = cell_voltage.unit
        nominal_voltage = VoltageQuantity(nominal_voltage_value,nominal_voltage_units)
        super().__init__(name,nominal_voltage, max_output_current)
        
    
    @property
    def cell_count(self) -> int:
        return self._cell_count

    @cell_count.setter
    def cell_count(self,new_cell_count: int):
        self._cell_count = new_cell_count
    
    @property
    def cell_voltage(self) -> VoltageQuantity:
        return self._cell_voltage

    @cell_voltage.setter
    def cell_voltage(self,new_cell_voltage: VoltageQuantity):
        self._cell_voltage = new_cell_voltage

    @property
    def capacity(self) -> ElectricChargeQuantity:
        return self._capacity

    @capacity.setter
    def capacity(self,new_capacity: ElectricChargeQuantity):
        self._capacity = new_capacity

    @abstractmethod
    def _restrict_instantiation(self):
        pass
    
    @property
    def chemistry(self) -> str:
        return self._chemistry

    @chemistry.setter
    def chemistry(self,new_chemistry: str):
        self._chemistry = new_chemistry
    
    @property
    def subchemistry(self) -> str:
        return self._subchemistry

    @subchemistry.setter
    def subchemistry(self,new_subchemistry: str):
        self._subchemistry = new_subchemistry
        
    def __str__(self) -> str:
        ret_str: str = (f'Battery name: {self.name}\n\t* Chemistry: {self.chemistry}(subchemistry: {self.subchemistry})\n\t* Nominal voltage = {self.nominal_voltage}\n\t* Cell voltage = {self.cell_voltage}\n\t' 
        f'* Cell count = {self.cell_count}\n\t* Capacity = {self.capacity}\n\t* Max. output current = {self.max_output_current}\n\t* Components associated:')
        for component in self.components:
            ret_str += f'\n\t\t- {component[0]} (x{component[1]})'
        ret_str += f'\n\t* Power budget:\n\t\tCurrent: {self.total_current}\n\t\tPower = {self.total_power}'
        return ret_str

class VoltageRegulator(BasePowerSupply):
    MAX_EFFICIENCY: float = 1.0
    MIN_EFFICIENCY: float = 0.0
    
    def __init__(self, name: str,nominal_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity, min_input_voltage: VoltageQuantity, max_input_voltage: VoltageQuantity ,efficiency: float):
        if(min_input_voltage > max_input_voltage):
            raise ValueError('Minimum input voltage must be less or equal than maximum input voltage.')
        if( efficiency < self.MIN_EFFICIENCY or efficiency > self.MAX_EFFICIENCY):
            raise ValueError(f'Efficiency must be between {self.MIN_EFFICIENCY} and {self.MAX_EFFICIENCY}')
        self._min_input_voltage = min_input_voltage
        self._max_input_voltage = max_input_voltage
        self._efficiency: float = efficiency
        super().__init__(name, nominal_voltage, max_output_current)
    
    @property
    def efficiency(self) -> float:
        return self._efficiency
    
    @efficiency.setter
    def efficiency(self,new_efficiency: float):
        self._efficiency = new_efficiency
    
    @property
    def min_input_voltage(self) -> VoltageQuantity:
        return self._min_input_voltage
    

    @min_input_voltage.setter
    def min_input_voltage(self,new_min_input_voltage: VoltageQuantity):
        self._min_input_voltage = new_min_input_voltage
        
    @property
    def max_input_voltage(self) -> VoltageQuantity:
        return self._max_input_voltage

    @max_input_voltage.setter
    def max_input_voltage(self,new_max_input_voltage: VoltageQuantity):
        self._max_input_voltage = new_max_input_voltage

    @abstractmethod
    def _restrict_instantiation(self):
        pass

class DCDCConverter(VoltageRegulator):
    
    @abstractmethod
    def _restrict_instantiation(self):
        pass
    
    def __init__(self, name: str, dcdc_type: str,nominal_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity, min_input_voltage: VoltageQuantity, max_input_voltage: VoltageQuantity ,efficiency: float):
        self._dcdc_type = dcdc_type
        super().__init__(name, nominal_voltage, max_output_current, min_input_voltage, max_input_voltage, efficiency)
    
    @property
    def dcdc_type(self) -> str:
        return self._dcdc_type

    def __str__(self):
        ret_str: str = f'{self.dcdc_type} converter name: {self.name}\n\t\n\t* Nominal voltage = {self.nominal_voltage}\n\t' \
        f'* Min. input voltage = {self._min_input_voltage}\n\t* Max. input voltage = {self._max_input_voltage}'\
            f'\n\t* Efficiency = {self._efficiency * 100.0}%'
        for component in self.components:
            ret_str += f'\n\t\t- {component[0]} (x{component[1]})'
        ret_str += f'\n\t* Power budget:\n\t\tCurrent: {self.total_current}\n\t\tPower = {self.total_power}'
        return ret_str

class BuckConverter(DCDCConverter):
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass
    
    def __init__(self, name: str, nominal_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity, min_input_voltage: VoltageQuantity, max_input_voltage: VoltageQuantity, efficiency: float = DCDCConverter.MAX_EFFICIENCY):
        if(nominal_voltage > min_input_voltage):
            raise ValueError('Nominal voltage must be lower than min. input voltage')
        dcdc_type: str = 'Buck'
        super().__init__(name,dcdc_type,nominal_voltage, max_output_current, min_input_voltage, max_input_voltage,efficiency)

class BoostConverter(DCDCConverter):
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass
    
    def __init__(self, name: str, nominal_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity, min_input_voltage: VoltageQuantity, max_input_voltage: VoltageQuantity, efficiency: float = DCDCConverter.MAX_EFFICIENCY):
        if(nominal_voltage < max_input_voltage):
            raise ValueError('Nominal voltage must be greater than max. input voltage')
        dcdc_type: str = 'Boost'
        super().__init__(name,dcdc_type,nominal_voltage, max_output_current, min_input_voltage, max_input_voltage,efficiency)

class BuckBoostConverter(DCDCConverter):
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass
    
    def __init__(self, name: str, nominal_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity, min_input_voltage: VoltageQuantity, max_input_voltage: VoltageQuantity, efficiency: float = DCDCConverter.MAX_EFFICIENCY):
        dcdc_type: str = 'Buck-Boost'
        super().__init__(name,dcdc_type,nominal_voltage, max_output_current, min_input_voltage, max_input_voltage,efficiency)

class LithiumBattery(Battery):
    LITHIUM_CELL_VOLTAGES = (  3.7 ,   3.6  ,   3.2   ,   3.7   ,  3.6   ,  0)
    LITHIUM_SUBCHEMISTRIES =   ('LiPo','Li-ion','LiFePO4','LiMn2O4','LiCoO2','Other')
    
    
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass
    
    def __init__(self, name: str, max_output_current: ElectricCurrentQuantity, capacity: ElectricChargeQuantity, cell_voltage: VoltageQuantity = None ,cell_count: int = 1, subchemistry: str = 'Other') -> None:
        if(subchemistry is None):
            subchemistry = self.LITHIUM_SUBCHEMISTRIES[0]
        elif (subchemistry not in self.LITHIUM_SUBCHEMISTRIES):
            raise ValueError(f'Invalid chemistry, must be in {self.LITHIUM_SUBCHEMISTRIES} range')
        if(cell_voltage is None):
            if(subchemistry == 'Other'):
                raise ValueError('Cell voltage must be provided if using custom chemistry')
        cell_voltage = cell_voltage if subchemistry == 'Other' else VoltageQuantity(self.LITHIUM_CELL_VOLTAGES[self.LITHIUM_SUBCHEMISTRIES.index(subchemistry)])
        super().__init__(name,chemistry='Lithium',cell_voltage=cell_voltage, max_output_current=max_output_current, capacity=capacity, subchemistry=subchemistry,cell_count=cell_count)

class LeadAcidBattery(Battery):
    
    LEAD_ACID_CELL_VOLTAGE = 2.0
    LEAD_ACID_SUBCHEMISTRY = 'Undefined'
    
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass  
    
    def __init__(self, name: str, max_output_current: ElectricCurrentQuantity, capacity: ElectricChargeQuantity, cell_count: int = 1) -> None:
        cell_voltage = VoltageQuantity(self.LEAD_ACID_CELL_VOLTAGE)
        super().__init__(name,chemistry='Lead-Acid',cell_voltage=cell_voltage, max_output_current=max_output_current, capacity=capacity, cell_count=cell_count, subchemistry=self.LEAD_ACID_SUBCHEMISTRY)

class LinearRegulator(VoltageRegulator):
    
    def __init__(self, name: str, nominal_voltage: VoltageQuantity, max_output_current: ElectricCurrentQuantity):
        super().__init__(name, nominal_voltage, max_output_current)



class PowerBudget:
    
    def __str__(self) -> str:
        return(f'{self.name}: {self.components}, {self.dc_power_supplies}')
    
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._components: List[List[Component,int]] = []
        self._dc_power_supplies: List[BasePowerSupply] = []
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name:str):
        self._name = new_name
        
    @property
    def dc_power_supplies(self):
        return self._dc_power_supplies
    
    @property
    def components(self):
        return self._components     
    
    def add_component(self, component: Component, quantity:int = 1):
        self._components.append((component,quantity))
    
    def add_power_supply(self, power_supply: BasePowerSupply):
        self._dc_power_supplies.append(power_supply)
    
    def remove_component(self, index: int):
        if index < 0 or index >= len(self._components):
            raise IndexError(f'Index {index} does not exist')
        self._components.pop(index)
    
    def remove_power_supply(self, index: int):
        if index < 0 or index >= len(self._dc_power_supplies):
            raise IndexError(f'Index {index} does not exist')
        self._dc_power_supplies.pop(index)
        



