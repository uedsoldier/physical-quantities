from __future__ import annotations

from typing import Self

from physical_quantities.quantities import (
    ElectricCurrentQuantity,
    EnergyQuantity,
    PowerQuantity,
    TimeQuantity,
    VoltageQuantity,
)
from physical_quantities.units import ElectricCurrentUnits, PowerUnits, TimeUnits, VoltageUnits

from .supplies import BasePowerSupply


class Component:
    @classmethod
    def from_voltage_current(
        cls, name: str, voltage: VoltageQuantity, current: ElectricCurrentQuantity
    ) -> Self:
        return cls(name, voltage=voltage, current=current)

    @classmethod
    def from_voltage_power(cls, name: str, voltage: VoltageQuantity, power: PowerQuantity) -> Self:
        return cls(name, voltage=voltage, power=power)

    @classmethod
    def from_current_power(
        cls, name: str, current: ElectricCurrentQuantity, power: PowerQuantity
    ) -> Self:
        return cls(name, current=current, power=power)

    """_summary_
    """

    def __init__(
        self,
        name: str,
        voltage: VoltageQuantity | None = None,
        current: ElectricCurrentQuantity | None = None,
        power: PowerQuantity | None = None,
        power_supply: BasePowerSupply | None = None,
    ) -> None:
        self._name: str = name
        # Two of voltage/current/power are required below and the third is computed, so after
        # __init__ all three are set; power_supply is genuinely optional.
        self._voltage: VoltageQuantity = voltage  # type: ignore[assignment]
        self._current: ElectricCurrentQuantity = current  # type: ignore[assignment]
        self._power: PowerQuantity = power  # type: ignore[assignment]
        self._power_supply: BasePowerSupply | None = power_supply

        if voltage is not None and current is not None:
            self.compute_power()
        elif voltage is not None and power is not None:
            self.compute_current()
        elif current is not None and power is not None:
            self.compute_voltage()
        else:
            raise ValueError("At least two parameters (voltage, current, power) must be provided.")

    def energy_consumption(self, t: TimeQuantity) -> EnergyQuantity:
        return EnergyQuantity(
            self.power.convert_to(PowerUnits.WATT.value).value
            * t.convert_to(TimeUnits.SECOND.value).value
        )

    def compute_power(self) -> None:
        self.power = PowerQuantity(
            self.voltage.convert_to(VoltageUnits.VOLT.value).value
            * self.current.convert_to(ElectricCurrentUnits.AMPERE.value).value
        )

    def compute_current(self) -> None:
        self.current = ElectricCurrentQuantity(
            self.power.convert_to(PowerUnits.WATT.value).value
            / self.voltage.convert_to(VoltageUnits.VOLT.value).value
        )

    def compute_voltage(self) -> None:
        self.voltage = VoltageQuantity(
            self.power.convert_to(PowerUnits.WATT.value).value
            / self.current.convert_to(ElectricCurrentUnits.AMPERE.value).value
        )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Name must be a string")  # noqa: TRY004 (ValueError kept, like the other setters)
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
    def power_supply(self) -> BasePowerSupply | None:
        return self._power_supply

    @power_supply.setter
    def power_supply(self, new_power_supply: BasePowerSupply) -> None:
        if not isinstance(new_power_supply, BasePowerSupply):
            raise ValueError("new_power_supply must be a BasePowerSupply")  # noqa: TRY004
        self._power_supply = new_power_supply

    def __str__(self) -> str:
        return f"Component name: {self.name} V={self.voltage} I={self.current} P={self.power}"
