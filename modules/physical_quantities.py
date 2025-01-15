import os
import json

from modules.utilities.json_utilities import json_string_to_dict, dict_to_json_string
from modules.conversion_managers import BaseConversionManager, TemperatureConversionManager
from modules.unit import *
from functools import total_ordering

@total_ordering
class BaseQuantity:
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={self._value}, unit={repr(self._unit)})'

    def _assert_compatible(self, other: "BaseQuantity") -> None:
        """Check if two quantities are compatible for addition or subtraction."""
        if not isinstance(other, BaseQuantity):
            raise TypeError('Can only operate on another BaseQuantity.')
        if type(self) is not type(other):
            raise TypeError(f'Cannot operate on different quantity types: {type(self)} and {type(other)}')
        if not self.unit.is_compatible_with(other.unit):
            raise ValueError(f'Cannot operate on incompatible units: {self.unit} and {other.unit}')
    
    def __add__(self, other: "BaseQuantity") -> "BaseQuantity":
        self._assert_compatible(other)
        # Convert the other value to the same unit as self
        other_converted = other.convert_to(self.unit)
        new_value = self.value + other_converted.value
        return type(self)(new_value, self.unit)
    
    def __sub__(self, other: "BaseQuantity") -> "BaseQuantity":
        self._assert_compatible(other)
        # Convert the other value to the same unit as self
        other_converted = other.convert_to(self.unit)
        new_value = self.value - other_converted.value
        return type(self)(new_value, self.unit)
    
    def __truediv__(self, other: "BaseQuantity"):
        if not isinstance(other, BaseQuantity):
            return NotImplemented
        
        # Create a new unit by dividing the dimensions
        new_unit = self.unit / other.unit
        new_value = self.value / other.value
        
        # Return a new instance of the appropriate type
        return type(self)(new_value, new_unit)
    
    def __mul__(self, other: "BaseQuantity"):
        if not isinstance(other, BaseQuantity):
            return NotImplemented
        
        # Combine units and multiply values
        new_unit = self.unit * other.unit
        new_value = self.value * other.value
        
        # Return a new instance of the appropriate type
        return type(self)(new_value, new_unit)
    
    def _compare(self,other: "BaseQuantity",method):
        if not isinstance(other, BaseQuantity):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError(f'Cannot compare different quantity types: {type(self)} and {type(other)}')
        try:
            other_value_in_self_unit = other.convert_to(self.unit).value
        except ValueError:
            raise ValueError(f'Cannot compare incompatible units: {self.unit} and {other.unit}')

        return method(self.value, other_value_in_self_unit)
    
    def __eq__(self, other):
        return self._compare(other, lambda x, y: x == y)
        
    
    def __lt__(self, other) -> bool:
        return self._compare(other, lambda x, y: x < y)
    
    def __gt__(self, other) -> bool:
        return self._compare(other, lambda x, y: x > y)
    
    def __init__(self, value: float, unit: Unit, quantity_type: str) -> None:
        if type(self) is BaseQuantity:
            raise TypeError('BaseQuantity cannot be instantiated directly.')
        self._value = value
        self._unit = unit
        self._conversion_manager = BaseConversionManager(quantity_type)
        
    def __str__(self) -> str:
        return f'{self._value} [{self._unit}]'
    
    def to_dict(self):
        return {
            'value': self._value,
            'unit': str(self._unit)
        }
        
    def to_json_string(self) -> str:
        return dict_to_json_string(self.to_dict())
    
    # def from_json_string(self, json_string: str) -> "BaseQuantity":
    #     data = json_string_to_dict(json_string)
    #     value: float =data['value']
    #     unit_symbol: str = data['unit']
    #     unit = find_unit_by_symbol(unit_symbol)
    #     unit_type = find_name_by_symbol(unit_symbol)
    #     return BaseQuantity(value,unit,unit_type)
        
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, new_value: float) -> None:
        self._value = new_value
    
    @property
    def unit(self) -> Unit:
        return self._unit
    
    @unit.setter
    def unit(self, new_unit: Unit) -> None:
        self._unit = new_unit
    
    def convert_to(self, target_unit: Unit) -> "BaseQuantity":
        # Check if the units are the same
        if self.unit == target_unit:
            return type(self)(self.value, self.unit)  # Create a new instance of the same class
        # Check if the units are compatible
        if not self.unit.is_compatible_with(target_unit):
            raise ValueError(f'Cannot convert between incompatible units: {self.unit} and {target_unit}')

        # Perform the conversion using the conversion manager
        converted_value = self._conversion_manager.convert(self.value, self.unit, target_unit)

        # Return a new instance of the same class with the converted value and unit
        return type(self)(converted_value, target_unit)

class LengthQuantity(BaseQuantity):
    def __init__(self, value: float, unit: Unit = LengthUnits.METER.value) -> None:
        super().__init__(value, unit,'length')

class MassQuantity(BaseQuantity):

    def __init__(self, value: float,unit: Unit = MassUnits.KILOGRAM.value) -> None:
        super().__init__(value, unit,'mass')
    
class TemperatureQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = LengthUnits.METER.value) -> None:
        super().__init__(value, unit,'temperature')
        self._conversion_manager = TemperatureConversionManager()
    
    def convert_to(self, target_unit: Unit):
        if(self.unit == target_unit):
            return TemperatureQuantity(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return TemperatureQuantity(value=converted_value, unit=target_unit)
    
class TimeQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = TimeUnits.SECOND.value) -> None:
        super().__init__(value, unit,'time')
    
class PowerQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = PowerUnits.WATT.value) -> None:
        super().__init__(value, unit,'power')

class FrequencyQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = FrequencyUnits.HERTZ.value) -> None:
        super().__init__(value, unit,'frequency')

class ForceQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = ForceUnits.NEWTON.value) -> None:
        super().__init__(value, unit,'force')
    
class EnergyQuantity(BaseQuantity):
    def __init__(self, value: float ,unit: Unit = EnergyUnits.JOULE.value) -> None:
        super().__init__(value, unit,'energy')

    
class ElectricChargeQuantity(BaseQuantity):
    def __init__(self, value: float ,unit: Unit = ElectricChargeUnits.COULOMB.value) -> None:
        super().__init__(value, unit,'electric_charge')
    
class VoltageQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = VoltageUnits.VOLT.value) -> None:
        super().__init__(value, unit, 'voltage')

class ElectricCurrentQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = ElectricCurrentUnits.AMPERE.value) -> None:
        super().__init__(value, unit, 'electric_current')

    
class ResistanceQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = ResistanceUnits.OHM.value) -> None:
        super().__init__(value, unit,'resistance')

class AngleQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = AngleUnits.DEGREE.value) -> None:
        super().__init__(value, unit,'angle')


class VolumeQuantity(BaseQuantity):
    def __init__(self, value: float,unit: Unit = VolumeUnits.CUBIC_METER.value) -> None:
        super().__init__(value, unit, 'volume')

class MassFlowRateQuantity(BaseQuantity):
    def __init__(self, value: float, unit: Unit = MassFlowRateUnits.KILOGRAM_PER_SECOND.value) -> None:
        super().__init__(value, unit, 'mass_flow_rate')