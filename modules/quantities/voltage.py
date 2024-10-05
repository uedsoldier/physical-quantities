from modules.quantities.quantity import Quantity, BaseConversionManager

class Voltage(Quantity):
    def __init__(self, value: float, unit: str = 'V') -> None:
        super().__init__(value, unit)
        self.conversion_manager = VoltageConversionManager()
    
    def convert_to(self, target_unit: str):
        converted_value = self.conversion_manager.convert(self.value, self.unit, target_unit)
        return Voltage(value=converted_value, unit=target_unit)
    
class VoltageConversionManager(BaseConversionManager):
    def __init__(self):
        super().__init__('voltage')