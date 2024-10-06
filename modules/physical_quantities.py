import os
import json
from modules.json_utilities import json_to_dict

class BaseQuantity:
    
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

class BaseConversionManager:
    
    @classmethod
    def change_quantity_type(cls,quantity_type: str):
        return cls(quantity_type = quantity_type)
    
    def __str__(self) -> str:
        return f'Conversion manager type: {self.self._quantity_type}'
    
    def __init__(self, quantity_type: str):
        """_summary_

        Args:
            quantity_type (str): _description_

        Raises:
            Exception: _description_
            Exception: _description_
            Exception: _description_
        """
        self._quantity_type = quantity_type
        filename: str = f'../conversion_tables/{self._quantity_type}.json'
        conversions_filepath: str = os.path.join(os.path.dirname(__file__), filename)
        try: 
            self._conversion_table = json_to_dict(conversions_filepath)
        except FileNotFoundError:
            raise Exception(f'File "{conversions_filepath}" does not exist')
        except json.JSONDecodeError:
            raise Exception(f'Error decoding JSON from file "{conversions_filepath}"')
        except Exception as e:
            raise Exception(f'An error occurred while loading "{filename}": {str(e)}')
            
    def convert(self, value: float, from_unit: str, to_unit: str) -> float :
        if(from_unit not in self._conversion_table.keys()):
            raise ValueError(f'Unknown from unit: {from_unit}')
        if(to_unit not in self._conversion_table.keys()):
            raise ValueError(f'Unknown to unit: {to_unit}')
        
            
        value_in_base = value * self._conversion_table[from_unit]    # Convert to base unit
        return value_in_base / self._conversion_table[to_unit]        # Convert to target unit

class Length(BaseQuantity):
    def __init__(self, value: float, unit: str = 'm') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('length')
    
    def convert_to(self, target_unit: str):
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Length(value=converted_value, unit=target_unit)

class Mass(BaseQuantity):

    def __init__(self, value: float, unit: str = 'kg') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('mass')
    
    def convert_to(self, target_unit: str):
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Mass(converted_value, target_unit)
    
class Temperature(BaseQuantity):
    def __init__(self, value: float, unit: str = 'C') -> None:
        super().__init__(value, unit)
        self.conversion_manager = TemperatureConversionManager()
    
    def convert_to(self, target_unit: str):
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Temperature(value=converted_value, unit=target_unit)
    
class TemperatureConversionManager(BaseConversionManager):
    def __init__(self):
        super().__init__('temperature')
    
    def convert(self, value: float, from_unit: str, to_unit: str):
        if from_unit not in self._conversion_table.keys():
            raise ValueError(f'Unknown from unit: {from_unit}')
        if to_unit not in self._conversion_table.keys():
            raise ValueError(f'Unknown to unit: {to_unit}')

        # Handle temperature conversion using lambdas
        to_base = eval(self._conversion_table[from_unit]['to_base'])
        from_base = eval(self._conversion_table[to_unit]['from_base'])
        value_in_base = to_base(value)
        return from_base(value_in_base)

class Time(BaseQuantity):
    def __init__(self, value: float, unit: str = 's') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('time')
    
    def convert_to(self, target_unit: str):
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Time(value=converted_value, unit=target_unit)
    
class Power(BaseQuantity):
    def __init__(self, value: float, unit: str = 'W') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('power')
    
    def convert_to(self, target_unit: str):
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Power(value=converted_value, unit=target_unit)
    
class Frequency(BaseQuantity):
    def __init__(self, value: float, unit: str = 'Hz') -> None:
        super().__init__(value, unit)
        self.conversion_manager = BaseConversionManager('frequency')
    
    def convert_to(self, target_unit: str):
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
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Angle(value=converted_value, unit=target_unit)
    
