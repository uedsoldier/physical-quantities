from .physical_quantities import VoltageQuantity, ElectricCurrentQuantity, PowerQuantity, EnergyQuantity,TimeQuantity
from .unit import VoltageUnits, PowerUnits, ElectricCurrentUnits, EnergyUnits,TimeUnits
from .power_supply import BasePowerSupply
class Component:
    
    def __str__(self) -> str:
        return(f'{self.name}: {self.voltage}, {self.current}, {self.power}')
    
    @classmethod
    def from_voltage_current(cls, name: str, voltage: VoltageQuantity, current: ElectricCurrentQuantity):
        return cls(name, voltage=voltage, current=current)

    @classmethod
    def from_voltage_power(cls, name: str, voltage: VoltageQuantity, power: PowerQuantity):
        return cls(name, voltage=voltage, power=power)

    @classmethod
    def from_current_power(cls, name: str, current: ElectricCurrentQuantity, power: PowerQuantity):
        return cls(name, current=current, power=power)
    
    """_summary_
    """
    def __init__(self, name: str, voltage:VoltageQuantity = None, current:ElectricCurrentQuantity = None, power:PowerQuantity = None, power_supply: BasePowerSupply = None) -> None:
        self._name: str = name
        self._voltage: VoltageQuantity = voltage
        self._current: ElectricCurrentQuantity = current
        self._power: PowerQuantity = power
        self._power_supply: BasePowerSupply = power_supply
        
        if (voltage is not None and current is not None):
            self.compute_power()
        elif(voltage is not None and power is not None):
            self.compute_current()
        elif(current is not None and power is not None):
            self.compute_voltage()
        else:
            raise ValueError('At least two parameters (voltage, current, power) must be provided.')
        
        
    def energy_consumption(self, t: TimeQuantity) -> EnergyQuantity:
        return EnergyQuantity( self.power.convert_to(PowerUnits.WATT.value).value * t.convert_to(TimeUnits.SECOND.value).value )
    
    def compute_power(self):
        self.power =  PowerQuantity(self.voltage.convert_to(VoltageUnits.VOLT.value).value * self.current.convert_to(ElectricCurrentUnits.AMPERE.value).value )
    
    def compute_current(self):
        self.current = ElectricCurrentQuantity(self.power.convert_to(PowerUnits.WATT.value).value / self.voltage.convert_to(VoltageUnits.VOLT.value).value)
        
    def compute_voltage(self):
        self.voltage = VoltageQuantity(self.power.convert_to(PowerUnits.WATT.value).value / self.current.convert_to(ElectricCurrentUnits.AMPERE.value).value)
    
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @property
    def voltage(self) -> VoltageQuantity:
        return self._voltage

    @voltage.setter
    def voltage(self, value: VoltageQuantity) -> None:
        if not isinstance(value, VoltageQuantity) and value is not None:
            raise ValueError("Voltage must be of type Voltage")
        self._voltage = value

    @property
    def current(self) -> ElectricCurrentQuantity:
        return self._current

    @current.setter
    def current(self, value: ElectricCurrentQuantity) -> None:
        if not isinstance(value, ElectricCurrentQuantity) and value is not None:
            raise ValueError("Current must be of type Current")
        self._current = value

    @property
    def power(self) -> PowerQuantity:
        return self._power

    @power.setter
    def power(self, value: PowerQuantity) -> None:
        if not isinstance(value, PowerQuantity) and value is not None:
            raise ValueError("Power must be of type Power")
        self._power = value
    
    @property
    def power_supply(self) -> BasePowerSupply:
        return self.power_supply

    @power_supply.setter
    def power_supply(self, new_power_supply: BasePowerSupply) -> None:
        if not isinstance(new_power_supply, BasePowerSupply):
            raise ValueError("new_power_supply must be a BasePowerSupply")
        self._power_supply = new_power_supply
    
    def __str__(self) -> str:
        return f'Component name: {self.name} V={self.voltage} I={self.current} P={self.power}'
    
