from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from .physical_quantities import ElectricCurrentQuantity, PowerQuantity, VoltageQuantity, TimeQuantity, EnergyQuantity, ElectricChargeQuantity
from .component import Component


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


