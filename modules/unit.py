from typing import Dict

class Dimensions:
    def  __init__(self, dimensions: Dict[str,int] = None) -> None:
        self._dimensions: Dict[str,int] = dimensions or {}
    
    @property
    def dimensions(self) -> Dict[str,int]:
        return self._dimensions
    
    def __setitem__(self, key, value) -> None:
        """Set the exponent for a dimension, removing zero-exponent entries."""
        if value == 0:
            self.dimensions.pop(key, None)
        else:
            self.dimensions[key] = value
    
    def __getitem__(self, key) -> int:
        """Get the exponent for a dimension, defaulting to 0 if not present."""
        return self._dimensions.get(key, 0)
    
    def __str__(self) -> str:
        """Format dimensions for display, consolidating exponents."""
        parts = []
        for dim, exp in self.dimensions.items():
            if exp == 1:
                parts.append(dim)
            else:
                parts.append(f"{dim}^{exp}")
        return "*".join(parts) if parts else "dimensionless"
    
    def __mul__(self, other: "Dimensions") -> "Dimensions":
        """Multiply dimensions, adding exponents."""
        result = Dimensions()
        for dim in self._dimensions:
            result[dim] = self[dim] + other[dim]
        for dim in other._dimensions:
            if dim not in self._dimensions:
                result[dim] = other[dim]
        return result
    
    def __truediv__(self, other: "Dimensions") -> "Dimensions":
        """Divide dimensions, subtracting exponents."""
        result = Dimensions()
        for dim in self._dimensions:
            result[dim] = self[dim] - other[dim]
        for dim in other._dimensions:
            if dim not in self._dimensions:
                result[dim] = -other[dim]
        return result

class Unit:
    
    symbol_map = {
        'L': 'm',     # Length in meters
        'T': 's',     # Time in seconds
        'M': 'kg',    # Mass in kilograms
        'I': 'A',     # Electric current in amperes
        'Θ': 'K',     # Thermodynamic temperature in kelvins
        'N': 'mol',   # Amount of substance in moles
        'J': 'cd',    # Luminous intensity in candelas
    }
    
    def __init__(self, name: str, symbol: str, dimensions: Dimensions = None) -> None:
        self._name = name
        self._symbol = symbol
        self._dimensions = dimensions or {}
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def symbol(self) -> str:
        return self._symbol
    
    @property
    def dimensions(self) -> Dimensions:
        return self._dimensions
    
    
    def __str__(self):
        # Map each dimension to the appropriate unit symbol with exponents
        symbol_parts = {}
        for dim, exp in self.dimensions.dimensions.items():
            # Convert dimension labels to their corresponding symbols
            symbol = self.symbol_map.get(dim, dim)
            symbol_parts[symbol] = exp

        # Format the symbols with exponents
        formatted_symbol = []
        for symbol, exponent in symbol_parts.items():
            if exponent == 1:
                formatted_symbol.append(symbol)
            else:
                formatted_symbol.append(f"{symbol}^{exponent}")
        return "*".join(formatted_symbol) if formatted_symbol else self.symbol
    
    def __mul__(self, other: "Unit") -> "Unit":
        """Multiplying two units combines their dimensions."""
        if not isinstance(other, Unit):
            raise TypeError('Can only multiply by another Unit.')
        new_dimensions = self._dimensions * other._dimensions
        new_name: str = f'{self._name}*{other.name}'
        new_symbol: str = f'{self._symbol}*{other.symbol}'
        
        return Unit(new_name,new_symbol,new_dimensions)
    
    def __truediv__(self, other: "Unit") -> "Unit":
        """Dividing two units subtracts the dimensions of the divisor from the dividend."""
        if not isinstance(other, Unit):
            raise TypeError('Can only divide by another Unit.')
        new_dimensions = self._dimensions / other._dimensions
        new_name: str = f'{self._name}*{other.name}'
        new_symbol: str = f'{self._symbol}/{other.symbol}'
        
        return Unit(new_name,new_symbol,new_dimensions)
    
    def is_dimensionless(self) -> bool:
        return not bool(self.unit.dimension.dimensions)
    