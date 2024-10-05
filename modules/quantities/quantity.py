import os
import json
from modules.utilities.json_utilities import json_to_dict
from decimal import Decimal, getcontext

class Quantity:
    def __init__(self, value: float, unit: str) -> None:
        self._value: float = value
        self._unit: str = unit
        self._conversion_dict: dict = None
    
    def __str__(self) -> str:
        return f'{self._value} [{self._unit}]'
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value: float):
        self._value = new_value
    
    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self, new_unit: str):
        self._unit = new_unit
        
        
    @property
    def conversion_dict(self):
        return self._conversion_dict
    
    @conversion_dict.setter
    def conversion_dict(self, new_dict: dict):
        self._conversion_dict = new_dict
    
    def convert_to(self):
        raise NotImplementedError('Specific quantities must implement this method')

class BaseConversionManager:
    
    def __init__(self, quantity_type: str):
        self.quantity_type = quantity_type
        filename: str = f'conversions/{self.quantity_type}_conversions.json'
        conversions_filepath: str = os.path.join(os.path.dirname(__file__), filename)
        try: 
            self._conversions = json_to_dict(conversions_filepath)
        except FileNotFoundError:
            raise Exception(f'File "{conversions_filepath}" does not exist')
        except json.JSONDecodeError:
            raise Exception(f'Error decoding JSON from file "{conversions_filepath}"')
        except Exception as e:
            raise Exception(f'An error occurred while loading "{filename}": {str(e)}')
            
    def convert(self, value: float, from_unit: str, to_unit: str):
        units = self._conversions['units']
        
        if(from_unit not in units):
            raise ValueError(f'Unknown from unit: {from_unit}')
        if(to_unit not in units):
            raise ValueError(f'Unknown to unit: {to_unit}')

        value_in_base = value * units[from_unit]    # Convert to base unit
        return value_in_base / units[to_unit]        # Convert to target unit
            
    
    
    