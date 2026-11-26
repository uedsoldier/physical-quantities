from __future__ import annotations

from .components import Component
from .supplies import BasePowerSupply


class PowerBudget:
    def __str__(self) -> str:
        return f"{self.name}: {self.components}, {self.dc_power_supplies}"

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._components: list[tuple[Component, int]] = []
        self._dc_power_supplies: list[BasePowerSupply] = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def dc_power_supplies(self) -> list[BasePowerSupply]:
        return self._dc_power_supplies

    @property
    def components(self) -> list[tuple[Component, int]]:
        return self._components

    def add_component(self, component: Component, quantity: int = 1) -> None:
        self._components.append((component, quantity))

    def add_power_supply(self, power_supply: BasePowerSupply) -> None:
        self._dc_power_supplies.append(power_supply)

    def remove_component(self, index: int) -> None:
        if index < 0 or index >= len(self._components):
            raise IndexError(f"Index {index} does not exist")
        self._components.pop(index)

    def remove_power_supply(self, index: int) -> None:
        if index < 0 or index >= len(self._dc_power_supplies):
            raise IndexError(f"Index {index} does not exist")
        self._dc_power_supplies.pop(index)
