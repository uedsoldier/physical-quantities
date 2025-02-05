from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from .physical_quantities import ElectricCurrentQuantity, PowerQuantity, VoltageQuantity, TimeQuantity, EnergyQuantity, ElectricChargeQuantity
from .utilities.json_utilities import json_to_dict
from .unit import ElectricCurrentUnits, PowerUnits, VoltageUnits, TimeUnits, EnergyUnits, ElectricChargeUnits
import os
from .component import Component
from .power_supply import BasePowerSupply

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
        



