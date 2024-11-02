import os
import json
from .utilities.json_utilities import json_to_dict, dict_to_json_string

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
