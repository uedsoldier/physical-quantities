from modules.quantities.quantity import Quantity, BaseConversionManager

class Length(Quantity):
    def __init__(self, value: float, unit: str = 'm') -> None:
        super().__init__(value, unit)
        self.conversion_manager = LengthConversionManager()
    
    def convert_to(self, target_unit: str):
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Length(value=converted_value, unit=target_unit)
    
class LengthConversionManager(BaseConversionManager):
    def __init__(self):
        super().__init__('length')