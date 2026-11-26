import json
from functools import cache
from importlib.resources import files

from ._json import json_string_to_dict
from .units import Unit


@cache
def _load_table(quantity_type: str) -> dict:
    resource = files(__package__) / 'conversion_tables' / f'{quantity_type}.json'
    return json_string_to_dict(resource.read_text(encoding='utf-8'))


class BaseConversionManager:
    
    @classmethod
    def change_quantity_type(cls,quantity_type: str):
        return cls(quantity_type = quantity_type)
    
    def __str__(self) -> str:
        return f'Conversion manager type: {self._quantity_type}'
    
    def __init__(self, quantity_type: str):
        self._quantity_type = quantity_type
        try:
            self._conversion_table = _load_table(quantity_type)
        except FileNotFoundError:
            raise Exception(f'Conversion table "{quantity_type}" does not exist')
        except json.JSONDecodeError:
            raise Exception(f'Error decoding JSON from table "{quantity_type}"')
        except Exception as e:
            raise Exception(f'An error occurred while loading "{quantity_type}": {e}')

    def convert(self, value: float, from_unit: Unit, to_unit: Unit) -> float :
        if from_unit.symbol not in self._conversion_table:
            raise ValueError(f'Unknown from unit: {from_unit.symbol}')
        if to_unit.symbol not in self._conversion_table:
            raise ValueError(f'Unknown to unit: {to_unit.symbol}')
    
        # Convert to base unit (assumed to be defined in JSON with factor 1)
        value_in_base = value * self._conversion_table[from_unit.symbol]
        # Convert from base unit to target unit
        return value_in_base / self._conversion_table[to_unit.symbol]


class TemperatureConversionManager(BaseConversionManager):
    def __init__(self):
        super().__init__('temperature')
    
    def convert(self, value: float, from_unit: Unit, to_unit: Unit) -> float:
        if from_unit.symbol not in self._conversion_table.keys():
            raise ValueError(f'Unknown from unit: {from_unit.symbol}')
        if to_unit.symbol not in self._conversion_table.keys():
            raise ValueError(f'Unknown to unit: {to_unit.symbol}')

        # Handle temperature conversion using lambdas
        to_base = eval(self._conversion_table[from_unit.symbol]['to_base'])
        from_base = eval(self._conversion_table[to_unit.symbol]['from_base'])
        value_in_base = to_base(value)
        return from_base(value_in_base)
