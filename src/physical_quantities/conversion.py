import json
from functools import cache
from importlib.resources import files
from typing import Self

from ._json import json_string_to_dict
from .units import Unit


@cache
def _load_table(quantity_type: str) -> dict:
    resource = files(__package__) / 'conversion_tables' / f'{quantity_type}.json'
    return json_string_to_dict(resource.read_text(encoding='utf-8'))


class ConversionTableError(Exception):
    """A conversion table could not be found or loaded."""


class BaseConversionManager:

    @classmethod
    def change_quantity_type(cls, quantity_type: str) -> Self:
        return cls(quantity_type=quantity_type)

    def __str__(self) -> str:
        return f'Conversion manager type: {self._quantity_type}'

    def __init__(self, quantity_type: str):
        self._quantity_type = quantity_type
        try:
            self._conversion_table = _load_table(quantity_type)
        except FileNotFoundError as e:
            raise ConversionTableError(f'Conversion table "{quantity_type}" does not exist') from e
        except json.JSONDecodeError as e:
            raise ConversionTableError(f'Error decoding JSON from table "{quantity_type}"') from e

    def _check_units(self, from_unit: Unit, to_unit: Unit) -> None:
        if from_unit.symbol not in self._conversion_table:
            raise ValueError(f'Unknown from unit: {from_unit.symbol}')
        if to_unit.symbol not in self._conversion_table:
            raise ValueError(f'Unknown to unit: {to_unit.symbol}')

    def convert(self, value: float, from_unit: Unit, to_unit: Unit) -> float:
        self._check_units(from_unit, to_unit)
        # Convert to base unit (defined in the JSON table with factor 1), then to the target.
        value_in_base = value * self._conversion_table[from_unit.symbol]
        return value_in_base / self._conversion_table[to_unit.symbol]


class TemperatureConversionManager(BaseConversionManager):
    """Affine conversions, with kelvin as base.

    Each table entry is ``{"pre_offset", "num", "den", "post_offset"}`` such that
    ``kelvin = (x + pre_offset) * num / den + post_offset``.
    """

    def __init__(self) -> None:
        super().__init__('temperature')

    def convert(self, value: float, from_unit: Unit, to_unit: Unit) -> float:
        self._check_units(from_unit, to_unit)
        src = self._conversion_table[from_unit.symbol]
        dst = self._conversion_table[to_unit.symbol]
        kelvin = (value + src['pre_offset']) * src['num'] / src['den'] + src['post_offset']
        return (kelvin - dst['post_offset']) * dst['den'] / dst['num'] - dst['pre_offset']
