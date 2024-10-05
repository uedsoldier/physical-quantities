from modules.quantities.quantity import Quantity, BaseConversionManager

class Temperature(Quantity):
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
        units = self._conversions['units']

        if from_unit not in units:
            raise ValueError(f'Unknown from unit: {from_unit}')
        if to_unit not in units:
            raise ValueError(f'Unknown to unit: {to_unit}')

        # Handle temperature conversion using lambdas
        to_base = eval(units[from_unit]['to_base'])
        from_base = eval(units[to_unit]['from_base'])
        value_in_base = to_base(value)
        return from_base(value_in_base)