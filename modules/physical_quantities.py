import os
import json
from .utilities.json_utilities import json_to_dict, dict_to_json_string
from .conversion_managers import BaseConversionManager, TemperatureConversionManager
from functools import total_ordering

@total_ordering
class BaseQuantity:
    
    def _compare(self,other,method):
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
    
    def __init__(self, value: float, unit: str) -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str): _description_
        """
        self._value = value
        self._unit = unit
        # self._conversion_dict: dict = None
        
    
    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f'{self._value} [{self._unit}]'
    
    def to_dict(self) -> dict:
        return {
            'value': self._value,
            'unit': self._unit
        }
        
    def to_json_string(self) -> str:
        return dict_to_json_string(self.to_dict())
    
    @property
    def value(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._value
    
    @value.setter
    def value(self, new_value: float):
        """_summary_

        Args:
            new_value (float): _description_
        """
        self._value = new_value
    
    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self, new_unit: str):
        self._unit = new_unit
    
    def convert_to(self):
        raise NotImplementedError('Specific quantities must implement this method')

class Length(BaseQuantity):
    def __init__(self, value: float, unit: str = 'm') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('length')
    
    def convert_to(self, target_unit: str):
        if(self.unit == target_unit):
            return Length(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Length(value=converted_value, unit=target_unit)

class Mass(BaseQuantity):

    def __init__(self, value: float, unit: str = 'kg') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('mass')
    
    def convert_to(self, target_unit: str):
        if(self.unit == target_unit):
            return Mass(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Mass(converted_value, target_unit)
    
class Temperature(BaseQuantity):
    def __init__(self, value: float, unit: str = 'C') -> None:
        super().__init__(value, unit)
        self.conversion_manager = TemperatureConversionManager()
    
    def convert_to(self, target_unit: str):
        if(self.unit == target_unit):
            return Temperature(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Temperature(value=converted_value, unit=target_unit)
    
class Time(BaseQuantity):
    def __init__(self, value: float, unit: str = 's') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('time')
    
    def convert_to(self, target_unit: str):
        if(self.unit == target_unit):
            return Time(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Time(value=converted_value, unit=target_unit)
    
class Power(BaseQuantity):
    def __init__(self, value: float, unit: str = 'W') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('power')
    
    def convert_to(self, target_unit: str):
        if(self.unit == target_unit):
            return Power(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Power(value=converted_value, unit=target_unit)
    
class Frequency(BaseQuantity):
    def __init__(self, value: float, unit: str = 'Hz') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('frequency')
    
    def convert_to(self, target_unit: str):
        if(self.unit == target_unit):
            return Frequency(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Frequency(value=converted_value, unit=target_unit)

class Force(BaseQuantity):
    def __init__(self, value: float, unit: str = 'N') -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to 'N'.
        """
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('force')
    
    def convert_to(self, target_unit: str):
        """_summary_

        Args:
            target_unit (str): _description_

        Returns:
            _type_: _description_
        """
        if(self.unit == target_unit):
            return Force(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Force(value=converted_value, unit=target_unit)
    
class Energy(BaseQuantity):
    def __init__(self, value: float , unit: str = 'J') -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to 'J'.
        """
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('energy')
    
    def convert_to(self, target_unit: str):
        """_summary_

        Args:
            target_unit (str): _description_

        Returns:
            _type_: _description_
        """
        if(self.unit == target_unit):
            return Energy(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Energy(value=converted_value, unit=target_unit)
    
class Charge(BaseQuantity):
    def __init__(self, value: float , unit: str = 'C') -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to 'C'.
        """
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('charge')
    
    def convert_to(self, target_unit: str):
        """_summary_

        Args:
            target_unit (str): _description_

        Returns:
            _type_: _description_
        """
        if(self.unit == target_unit):
            return Charge(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Charge(value=converted_value, unit=target_unit)
    
class Voltage(BaseQuantity):
    def __init__(self, value: float, unit: str = 'V') -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to 'V'.
        """
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('voltage')
    
    def convert_to(self, target_unit: str):
        """_summary_

        Args:
            target_unit (str): _description_

        Returns:
            _type_: _description_
        """
        if(self.unit == target_unit):
            return Voltage(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Voltage(value=converted_value, unit=target_unit)

class Current(BaseQuantity):
    def __init__(self, value: float, unit: str = 'A') -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to 'A'.
        """
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('current')
    
    def convert_to(self, target_unit: str):
        """_summary_

        Args:
            target_unit (str): _description_

        Returns:
            _type_: _description_
        """
        if(self.unit == target_unit):
            return Current(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Current(value=converted_value, unit=target_unit)
    
class Resistance(BaseQuantity):
    def __init__(self, value: float, unit: str = 'ohm') -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to 'ohm'.
        """
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('resistance')
    
    def convert_to(self, target_unit: str):
        """_summary_

        Args:
            target_unit (str): _description_

        Returns:
            _type_: _description_
        """
        if(self.unit == target_unit):
            return Resistance(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Resistance(value=converted_value, unit=target_unit)
    
class Angle(BaseQuantity):
    def __init__(self, value: float, unit: str = 'deg') -> None:
        """_summary_

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to 'deg'.
        """
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('angle')
    
    def convert_to(self, target_unit: str):
        """_summary_

        Args:
            target_unit (str): _description_

        Returns:
            _type_: _description_
        """
        if(self.unit == target_unit):
            return Angle(self.value,self.unit)
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Angle(value=converted_value, unit=target_unit)
    
