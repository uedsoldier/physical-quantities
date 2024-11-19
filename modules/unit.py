from typing import Dict
from enum import Enum

class Dimensions:
    def  __init__(self, dimensions_dict: Dict[str,int] = None) -> None:
        self._dimensions_dict: Dict[str,int] = dimensions_dict or {}
    
    def is_dimensionless(self) -> bool:
        """Check if the dimensions are dimensionless (empty dictionary)."""
        return all( dim == 0 for dim in self._dimensions_dict.values())
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dimensions):
            return False
        return self._dimensions_dict == other._dimensions_dict

    def __pow__(self, exponent: float | int) -> "Dimensions":
        """Raise each dimension's exponent to the power of a constant exponent."""
    
        # Ensure the exponent is a numeric value (either int or float)
        if not isinstance(exponent, (int, float)):
            raise TypeError(f"Exponent must be a numeric value, got {type(exponent)}.")
        
        # Apply exponentiation to each dimension's exponent
        new_dimensions = {}
        for key, value in self._dimensions_dict.items():
            new_dimensions[key] = value * exponent  # Multiply the exponent by the constant exponent
        
        return Dimensions(new_dimensions)
    
    def __str__(self) -> str:
        """Format dimensions for display, consolidating exponents."""
        parts = []
        for dim, exp in self._dimensions_dict.items():
            if exp == 1:
                parts.append(dim)
            else:
                parts.append(f"{dim}^{exp}")
        return "*".join(parts) if parts else "dimensionless"
    
    def __mul__(self, other: "Dimensions") -> "Dimensions":
        """Multiply two Dimensions objects, combining their exponents."""
        if not isinstance(other, Dimensions):
            raise TypeError("Can only multiply with another Dimensions instance.")
        
        new_dimensions = self._dimensions_dict.copy()  # Start with the current dimensions
        
        for key, value in other._dimensions_dict.items():
            # Add the exponents of matching dimension symbols
            new_dimensions[key] = new_dimensions.get(key, 0) + value
        # Remove zero exponents
        new_dimensions = {k: v for k, v in new_dimensions.items() if v != 0}
        return Dimensions(new_dimensions)
    
    def __truediv__(self, other: "Dimensions") -> "Dimensions":
        """Divide two Dimensions objects, subtracting the exponents."""
        if not isinstance(other, Dimensions):
            raise TypeError("Can only divide with another Dimensions instance.")
        
        new_dimensions = self._dimensions_dict.copy()  # Start with the current dimensions
        
        for key, value in other._dimensions_dict.items():
            # Subtract the exponents of matching dimension symbols
            new_dimensions[key] = new_dimensions.get(key, 0) - value
        # Remove zero exponents
        new_dimensions = {k: v for k, v in new_dimensions.items() if v != 0}
        return Dimensions(new_dimensions)
    
        
    
    def __repr__(self):
        return f'{self._dimensions_dict}'
    
    def validate_dimension(self, expected: "Dimensions") -> bool:
        """Validate if the current Dimensions match the expected Dimensions."""
        return self._dimensions_dict == expected._dimensions_dict
        
    
    # @property
    # def dimensions_dict(self) -> Dict[str,int]:
    #     return self._dimensions_dict
    
    # def __setitem__(self, key, value) -> None:
    #     """Set the exponent for a dimension, removing zero-exponent entries."""
    #     if value == 0:
    #         self.dimensions.pop(key, None)
    #     else:
    #         self.dimensions[key] = value
    
    # def __getitem__(self, key) -> int:
    #     """Get the exponent for a dimension, defaulting to 0 if not present."""
    #     return self._dimensions_dict.get(key, 0)
    
    
    
    def _combine_dimensions(self, other: "Dimensions") -> "Dimensions":
        """Combine the dimensions of this object with another Dimensions object."""
        combined_dict = self._dimensions_dict.copy()

        for dim, exp in other._dimensions_dict.items():
            if dim in combined_dict:
                combined_dict[dim] += exp  # Add exponents if dimension exists
            else:
                combined_dict[dim] = exp  # Otherwise, just add the new dimension

        return Dimensions(combined_dict)
    
    def _divide_dimensions(self, other: "Dimensions") -> "Dimensions":
        """Divide the dimensions of this object by another Dimensions object."""
        combined_dict = self._dimensions_dict.copy()

        for dim, exp in other._dimensions_dict.items():
            if dim in combined_dict:
                combined_dict[dim] -= exp  # Subtract exponents if dimension exists
            else:
                combined_dict[dim] = -exp  # Otherwise, add the negative exponent for division

        return Dimensions(combined_dict)

LENGTH_DIMENSIONS = Dimensions({'L':1})
TIME_DIMENSIONS = Dimensions({'T': 1})
MASS_DIMENSIONS = Dimensions({'M': 1})
TEMPERATURE_DIMENSIONS = Dimensions({'Θ': 1})
ELECTRIC_CURRENT_DIMENSIONS = Dimensions({'I': 1})
AMOUNT_SUBSTANCE_DIMENSIONS = Dimensions({'N': 1})
LUMINOUS_INTENSITY_DIMENSIONS = Dimensions({'J': 1})
FORCE_DIMENSIONS=Dimensions({'M': 1, 'L': 1, 'T': -2})
PRESSURE_DIMENSIONS=Dimensions({'M': 1, 'L': -1, 'T': -2})
ENERGY_DIMENSIONS=Dimensions({'L': 2, 'M': 1, 'T': -2})
POWER_DIMENSIONS=Dimensions({'M': 1, 'L': 2, 'T': -3})
VOLTAGE_DIMENSIONS=Dimensions({'M': 1, 'L': 2, 'T': -3, 'I': -1})
FREQUENCY_DIMENSIONS=Dimensions({'T': -1})
ANGULAR_VELOCITY_DIMENSIONS = Dimensions({'T': -1})
ELECTRIC_CHARGE_DIMENSIONS=Dimensions({'T': 1, 'I': 1})
MAGNETIC_FLUX_DIMENSIONS=Dimensions({'M': 1, 'L': 2, 'T': -2, 'I': -1})
MAGNETIC_FIELD_DIMENSIONS=Dimensions({'M': 1, 'L': -1, 'T': -2, 'I': -1})
INDUCTANCE_DIMENSIONS=Dimensions({'M': 1, 'L': 2, 'T': -2, 'I': -2})
CAPACITANCE_DIMENSIONS=Dimensions({'L': -2, 'M': -1, 'T': 4, 'I': 2})
RESISTANCE_DIMENSIONS=Dimensions({'M': 1, 'L': 2, 'T': -3, 'I': -2})
CONDUCTANCE_DIMENSIONS=Dimensions({'M': -1, 'L': -2, 'T': 3, 'I': 2})
ILLUMINATION_DIMENSIONS= Dimensions({'L': 2, 'M': -1, 'T': -3})
ANGLE_DIMENSIONS=Dimensions({'': 1})
AREA_DIMENSIONS=Dimensions({'L': 2})
VOLUME_DIMENSIONS=Dimensions({'L': 3})
FLOW_RATE_DIMENSIONS=Dimensions({'L': 3, 'T': -1})
MASS_FLOW_RATE_DIMENSIONS=Dimensions({'M': 1, 'T': -1})
SPEED_DIMENSIONS=Dimensions({'L': 1, 'T': -1})
ACCELERATION_DIMENSIONS = Dimensions({'L': 1, 'T': -2})
THERMAL_CONDUCTIVITY_DIMENSIONS = Dimensions({'M':1,'L':1,'T':-3,'Θ':-1})
THERMAL_RESISTANCE_DIMENSIONS = Dimensions({'M': -1, 'L': -1, 'T': 3, 'Θ': 1})

# TODO More dimensions...

ALL_DIMENSIONS = (
    LENGTH_DIMENSIONS,
    TIME_DIMENSIONS,
    MASS_DIMENSIONS,
    TEMPERATURE_DIMENSIONS,
    ELECTRIC_CURRENT_DIMENSIONS,
    AMOUNT_SUBSTANCE_DIMENSIONS,
    LUMINOUS_INTENSITY_DIMENSIONS,
    FORCE_DIMENSIONS,
    PRESSURE_DIMENSIONS,
    ENERGY_DIMENSIONS,
    POWER_DIMENSIONS,
    VOLTAGE_DIMENSIONS,
    FREQUENCY_DIMENSIONS,
    ANGULAR_VELOCITY_DIMENSIONS,
    ELECTRIC_CHARGE_DIMENSIONS,
    MAGNETIC_FLUX_DIMENSIONS,
    MAGNETIC_FIELD_DIMENSIONS,
    INDUCTANCE_DIMENSIONS,
    CAPACITANCE_DIMENSIONS,
    RESISTANCE_DIMENSIONS,
    CONDUCTANCE_DIMENSIONS,
    ILLUMINATION_DIMENSIONS,
    ANGLE_DIMENSIONS,
    AREA_DIMENSIONS,
    VOLUME_DIMENSIONS,
    FLOW_RATE_DIMENSIONS,
    MASS_FLOW_RATE_DIMENSIONS,
    SPEED_DIMENSIONS,
    ACCELERATION_DIMENSIONS,
    THERMAL_CONDUCTIVITY_DIMENSIONS,
    THERMAL_RESISTANCE_DIMENSIONS,
    # TODO More dimensions...
)

class Unit:

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
    
    
    def is_compatible_with(self, other: "Unit") -> bool:
        """Check if this unit is compatible with another unit."""
        if not isinstance(other, Unit):
            raise TypeError('Can only check compatibility with another Unit.')
        return self.dimensions == other.dimensions
    
    def __repr__(self) -> str:
        """Return a more detailed representation of the unit."""
        return f"Unit(name={self._name}, symbol={self._symbol}, dimensions={self._dimensions._dimensions_dict})"
    
    def __str__(self):
        # Define a symbol map for each dimension (optional)
        _symbol_map = {
            'M': 'kg',  # mass
            'L': 'm',   # length
            'T': 's',   # time
            'A': 'A',   # electric current
            'K': 'K',   # temperature
            'mol': 'mol',  # amount of substance
            'cd': 'cd'  # luminous intensity
        }

        # Map each dimension to the appropriate unit symbol with exponents
        symbol_parts = {}
        for dim, exp in self.dimensions._dimensions_dict.items():  # Corrected to dimensions_dict
            # Convert dimension labels to their corresponding symbols using the symbol_map
            symbol = _symbol_map.get(dim, dim)  # Default to dimension name if no map is found
            if exp == 1:
                symbol_parts[symbol] = ''
            elif exp == -1:
                symbol_parts[symbol] = '^(-1)'
            else:
                symbol_parts[symbol] = f'^{exp}'
        
        # Combine all dimension symbols into a string representation
        dimension_str = "*".join([f"{key}{value}" for key, value in symbol_parts.items()])
        return f"{dimension_str}"    # f"{self._name}: {dimension_str}"
    
    def __mul__(self, other: "Unit") -> "Unit":
        """Multiplying two units combines their dimensions."""
        if not isinstance(other, Unit):
            raise TypeError('Can only multiply by another Unit.')

        # Use the combine_dimensions method to combine the dimensions
        new_dimensions = self._dimensions._combine_dimensions(other._dimensions)
        new_name = f'{self._name}*{other._name}'
        new_symbol = f'{self._symbol}*{other._symbol}'
        
        return Unit(new_name, new_symbol, new_dimensions)
            
    def __truediv__(self, other: "Unit") -> "Unit":
        """Dividing two units combines their dimensions with subtracted exponents."""
        if not isinstance(other, Unit):
            raise TypeError('Can only divide by another Unit.')

        # Use the divide_dimensions method to divide the dimensions
        new_dimensions = self._dimensions._divide_dimensions(other._dimensions)
        new_name = f'{self._name}/{other._name}'
        new_symbol = f'{self._symbol}/{other._symbol}'
        
        return Unit(new_name, new_symbol, new_dimensions)

    def is_dimensionless(self) -> bool:
        """Check if the unit is dimensionless."""
        return self._dimensions.is_dimensionless()

# Unit definition

# Length Unit
class LengthUnits(Enum):
    METER = Unit('meter', 'm', LENGTH_DIMENSIONS)          
    MICROMETER = Unit('micrometer', 'μm', LENGTH_DIMENSIONS)
    NANOMETER = Unit('nanometer', 'nm', LENGTH_DIMENSIONS)
    CENTIMETER = Unit('centimeter', 'cm', LENGTH_DIMENSIONS)
    MILLIMETER = Unit('millimeter', 'mm', LENGTH_DIMENSIONS)
    KILOMETER = Unit('kilometer', 'km', LENGTH_DIMENSIONS)
    INCH = Unit('inch', 'in', LENGTH_DIMENSIONS)
    FOOT = Unit('foot', 'ft', LENGTH_DIMENSIONS)
    YARD = Unit('yard', 'yd', LENGTH_DIMENSIONS)
    MILE = Unit('mile', 'mile', LENGTH_DIMENSIONS)

# Time Unit
class TimeUnits(Enum):
    SECOND = Unit('second', 's', TIME_DIMENSIONS)          
    MILLISECOND = Unit('millisecond', 'ms', TIME_DIMENSIONS)
    MICROSECOND = Unit('microsecond', 'μs', TIME_DIMENSIONS)
    NANOSECOND = Unit('nanosecond', 'ns', TIME_DIMENSIONS)
    MINUTE = Unit('minute', 'min', TIME_DIMENSIONS)
    HOUR = Unit('hour', 'hour', TIME_DIMENSIONS)
    DAY = Unit('day', 'day', TIME_DIMENSIONS)
    WEEK = Unit('week', 'week', TIME_DIMENSIONS)
    MONTH = Unit('month', 'month', TIME_DIMENSIONS)
    YEAR = Unit('year', 'year', TIME_DIMENSIONS)

# Define MassUnits Enum with explicit unit assignment
class MassUnits(Enum):
    KILOGRAM = Unit('kilogram', 'kg', MASS_DIMENSIONS)
    GRAM = Unit('gram', 'g', MASS_DIMENSIONS)
    MILLIGRAM = Unit('milligram', 'mg', MASS_DIMENSIONS)
    MICROGRAM = Unit('microgram', 'μg', MASS_DIMENSIONS)
    NANOGRAM = Unit('nanogram', 'ng', MASS_DIMENSIONS)
    POUND = Unit('pound', 'lb', MASS_DIMENSIONS)
    OUNCE = Unit('ounce', 'oz', MASS_DIMENSIONS)
    

# Temperature Unit
class TemperatureUnits(Enum):
    KELVIN = Unit('kelvin', 'K', TEMPERATURE_DIMENSIONS)
    CELSIUS = Unit('celsius', '°C', TEMPERATURE_DIMENSIONS)
    FAHRENHEIT = Unit('fahrenheit', '°F', TEMPERATURE_DIMENSIONS)

# Electric Current Unit
class ElectricCurrentUnits(Enum):
    AMPERE = Unit('ampere', 'A', ELECTRIC_CURRENT_DIMENSIONS)          
    NANOAMPERE = Unit('nanoampere', 'nA', ELECTRIC_CURRENT_DIMENSIONS)
    MICROAMPERE = Unit('microampere', 'μA', ELECTRIC_CURRENT_DIMENSIONS)
    MILLIAMPERE = Unit('milliampere', 'mA', ELECTRIC_CURRENT_DIMENSIONS)
    KILOAMPERE = Unit('kiloampere', 'kA', ELECTRIC_CURRENT_DIMENSIONS)


# Amount of Substance Unit
class AmountSubstanceUnits(Enum):
    MOLE = Unit('mole', 'mol', AMOUNT_SUBSTANCE_DIMENSIONS)

# Luminous Intensity Unit
class LuminousIntensityUnits(Enum):
    # Define the units for luminous intensity
    CANDELA = Unit('candela', 'cd', LUMINOUS_INTENSITY_DIMENSIONS)
    MILLICANDELA = Unit('millicandela', 'mcd', LUMINOUS_INTENSITY_DIMENSIONS)
    MICROCANDELA = Unit('microcandela', 'μcd', LUMINOUS_INTENSITY_DIMENSIONS)
    NANOCANDELA = Unit('nanocandela', 'ncd', LUMINOUS_INTENSITY_DIMENSIONS)
    KILOCANDELA = Unit('kilocandela', 'kcd', LUMINOUS_INTENSITY_DIMENSIONS)
    MEGACANDELA = Unit('megacandela', 'Mcd', LUMINOUS_INTENSITY_DIMENSIONS)
    GIGACANDELA = Unit('gigacandela', 'Gcd', LUMINOUS_INTENSITY_DIMENSIONS)

# Force Unit
class ForceUnits(Enum):
    NEWTON = Unit('newton', 'N', FORCE_DIMENSIONS)          
    KILONEWTON = Unit('kilonewton', 'kN', FORCE_DIMENSIONS)
    KILOGRAM_FORCE = Unit('kilogram force', 'kgf', FORCE_DIMENSIONS)
    GRAM_FORCE = Unit('gram force', 'gf', FORCE_DIMENSIONS)
    POUND_FORCE = Unit('pound force', 'lbf', FORCE_DIMENSIONS)
    OUNCE_FORCE = Unit('ounce force', 'ozf', FORCE_DIMENSIONS)

# Pressure Unit
class PressureUnits(Enum):
    PASCAL = Unit('pascal', 'Pa', PRESSURE_DIMENSIONS)          
    KILOPASCAL = Unit('kilopascal', 'kPa', PRESSURE_DIMENSIONS)
    MEGAPASCAL = Unit('megapascal', 'MPa', PRESSURE_DIMENSIONS)
    GIGAPASCAL = Unit('gigapascal', 'GPa', PRESSURE_DIMENSIONS)
    BAR = Unit('bar', 'bar', PRESSURE_DIMENSIONS)
    MILLIBAR = Unit('millibar', 'mbar', PRESSURE_DIMENSIONS)
    ATMOSPHERE = Unit('atmosphere', 'atm', PRESSURE_DIMENSIONS)
    MILLIMETER_OF_MERCURY = Unit('millimeter of mercury', 'mmHg', PRESSURE_DIMENSIONS)
    INCH_OF_MERCURY = Unit('inch of mercury', 'inHg', PRESSURE_DIMENSIONS)
    POUND_SQUARE_INCH = Unit('pound per square inch', 'psi', PRESSURE_DIMENSIONS)
    KILOGRAM_FORCE_PER_CENTIMETER_SQUARED = Unit('kilogram force per centimeter squared', 'kgf/cm²', PRESSURE_DIMENSIONS)

# Energy Unit
class EnergyUnits(Enum):
    JOULE = Unit('joule', 'J', ENERGY_DIMENSIONS)          
    NANOJOULE = Unit('nanojoule', 'nJ', ENERGY_DIMENSIONS)
    MICROJOULE = Unit('microjoule', 'μJ', ENERGY_DIMENSIONS)
    MILLIJOULE = Unit('millijoule', 'mJ', ENERGY_DIMENSIONS)
    KILOJOULE = Unit('kilojoule', 'kJ', ENERGY_DIMENSIONS)
    MEGAJOULE = Unit('megajoule', 'MJ', ENERGY_DIMENSIONS)
    GIGAJOULE = Unit('gigajoule', 'GJ', ENERGY_DIMENSIONS)
    TERAJOULE = Unit('terajoule', 'TJ', ENERGY_DIMENSIONS)
    CALORIE = Unit('calorie', 'cal', ENERGY_DIMENSIONS)
    KILOCALORIE = Unit('kilocalorie', 'kcal', ENERGY_DIMENSIONS)
    WATT_HOUR = Unit('watt hour', 'Wh', ENERGY_DIMENSIONS)
    KILOWATT_HOUR = Unit('kilowatt hour', 'kWh', ENERGY_DIMENSIONS)
    BRITISH_THERMAL_UNIT = Unit('British thermal unit', 'BTU', ENERGY_DIMENSIONS)
    ELECTRON_VOLT = Unit('electron volt', 'eV', ENERGY_DIMENSIONS)
    FOOT_POUND = Unit('foot-pound', 'lb-ft', ENERGY_DIMENSIONS)

# Power Unit
class PowerUnits(Enum):
    WATT = Unit('watt', 'W', POWER_DIMENSIONS)          
    NANOWATT = Unit('nanowatt', 'nW', POWER_DIMENSIONS)
    MICROWATT = Unit('microwatt', 'μW', POWER_DIMENSIONS)
    MILLIWATT = Unit('milliwatt', 'mW', POWER_DIMENSIONS)
    KILOWATT = Unit('kilowatt', 'kW', POWER_DIMENSIONS)
    MEGAWATT = Unit('megawatt', 'MW', POWER_DIMENSIONS)
    GIGAWATT = Unit('gigawatt', 'GW', POWER_DIMENSIONS)
    TERAWATT = Unit('terawatt', 'TW', POWER_DIMENSIONS)
    HORSEPOWER = Unit('horsepower', 'hp', POWER_DIMENSIONS)
    BTU_PER_HOUR = Unit('BTU per hour', 'BTU/h', POWER_DIMENSIONS)
    KILOCALORIE_PER_HOUR = Unit('kilocalorie per hour', 'kcal/h', POWER_DIMENSIONS)
    FOOT_POUND_PER_SECOND = Unit('foot-pound per second', 'lb-ft/s', POWER_DIMENSIONS)
    REFRIGERATION_TON = Unit('refrigeration ton', 'RT', POWER_DIMENSIONS)
    VOLT_AMPERE = Unit('volt ampere', 'VA', POWER_DIMENSIONS)
    VOLT_AMPERE_REACTIVE = Unit('volt ampere reactive', 'VAR', POWER_DIMENSIONS)
    KILOVOLT_AMPERE_REACTIVE = Unit('kilovolt ampere reactive', 'kVAR', POWER_DIMENSIONS)
    MEGAVOLT_AMPERE_REACTIVE = Unit('megavolt ampere reactive', 'MVAR', POWER_DIMENSIONS)

# Voltage (Electrical Potential) Unit
class VoltageUnits(Enum):
    VOLT = Unit('volt', 'V', VOLTAGE_DIMENSIONS)          
    NANOVOLT = Unit('nanovolt', 'nV', VOLTAGE_DIMENSIONS)
    MICROVOLT = Unit('microvolt', 'μV', VOLTAGE_DIMENSIONS)
    MILLIVOLT = Unit('millivolt', 'mV', VOLTAGE_DIMENSIONS)
    KILOVOLT = Unit('kilovolt', 'kV', VOLTAGE_DIMENSIONS)

# Frequency and Angular velocity Unit
class FrequencyUnits(Enum):
    HERTZ = Unit('hertz', 'Hz', FREQUENCY_DIMENSIONS)          
    KILOHERTZ = Unit('kilohertz', 'kHz', FREQUENCY_DIMENSIONS)
    MEGAHERTZ = Unit('megahertz', 'MHz', FREQUENCY_DIMENSIONS)
    GIGAHERTZ = Unit('gigahertz', 'GHz', FREQUENCY_DIMENSIONS)

    REV_PER_MINUTE = Unit('revolutions per minute', 'rpm', ANGULAR_VELOCITY_DIMENSIONS)
    RAD_PER_SECOND = Unit('radian per second', 'rad/s', ANGULAR_VELOCITY_DIMENSIONS)
    DEG_PER_SECOND = Unit('degree per second', '°/s', ANGULAR_VELOCITY_DIMENSIONS)
    REV_PER_SECOND = Unit('revolution per second', 'rps', ANGULAR_VELOCITY_DIMENSIONS)

# Electric Charge Unit
class ElectricChargeUnits(Enum):
    COULOMB = Unit('coulomb', 'C', ELECTRIC_CHARGE_DIMENSIONS)          
    NANOCOULOMB = Unit('nanocoulomb', 'nC', ELECTRIC_CHARGE_DIMENSIONS)
    MICROCOULOMB = Unit('microcoulomb', 'μC', ELECTRIC_CHARGE_DIMENSIONS)
    MILLICOULOMB = Unit('millicoulomb', 'mC', ELECTRIC_CHARGE_DIMENSIONS)
    KILOCOULOMB = Unit('kilocoulomb', 'kC', ELECTRIC_CHARGE_DIMENSIONS)
    MEGACOULOMB = Unit('megacoulomb', 'MC', ELECTRIC_CHARGE_DIMENSIONS)
    ELEMENTARY_CHARGE = Unit('elementary charge', 'e', ELECTRIC_CHARGE_DIMENSIONS)
    AMPERE_HOUR = Unit('ampere hour', 'Ah', ELECTRIC_CHARGE_DIMENSIONS)
    MILLIAMPERE_HOUR = Unit('milliampere hour', 'mAh', ELECTRIC_CHARGE_DIMENSIONS)
    MICROAMPERE_HOUR = Unit('microampere hour', 'μAh', ELECTRIC_CHARGE_DIMENSIONS)

# Magnetic Flux Unit
class MagneticFluxUnits(Enum):
    WEBER = Unit('weber', 'Wb', MAGNETIC_FLUX_DIMENSIONS)
    MILLIWEBER = Unit('milliweber', 'mWb', MAGNETIC_FLUX_DIMENSIONS)
    MICROWEBER = Unit('microweber', 'μWb', MAGNETIC_FLUX_DIMENSIONS)
    KILOWEBER = Unit('kiloweber', 'kWb', MAGNETIC_FLUX_DIMENSIONS)
    MEGAWEBER = Unit('megaweber', 'MWb', MAGNETIC_FLUX_DIMENSIONS)

# Magnetic Field Unit
class MagneticFieldUnits(Enum):
    TESLA = Unit('tesla', 'T', MAGNETIC_FIELD_DIMENSIONS)
    GAUSS = Unit('gauss', 'G', MAGNETIC_FIELD_DIMENSIONS)
    MILLIGAUSS = Unit('milligauss', 'mG', MAGNETIC_FIELD_DIMENSIONS)
    MICROGAUSS = Unit('microgauss', 'μG', MAGNETIC_FIELD_DIMENSIONS)
    KILOTESLA = Unit('kilotesla', 'kT', MAGNETIC_FIELD_DIMENSIONS)
    MEGATESLA = Unit('megatesla', 'MT', MAGNETIC_FIELD_DIMENSIONS)

# Inductance Units
class InductanceUnits(Enum):
    HENRY = Unit('henry', 'H', INDUCTANCE_DIMENSIONS)
    MILLIHENRY = Unit('millihenry', 'mH', INDUCTANCE_DIMENSIONS)
    MICROHENRY = Unit('microhenry', 'μH', INDUCTANCE_DIMENSIONS)
    NANOHENRY = Unit('nanohenry', 'nH', INDUCTANCE_DIMENSIONS)
    PICOHENRY = Unit('picohenry', 'pH', INDUCTANCE_DIMENSIONS)

# Capacitance Unit
class CapacitanceUnits(Enum): 
    FARAD = Unit('farad', 'F', CAPACITANCE_DIMENSIONS)          
    MILLIFARAD = Unit('millifarad', 'mF', CAPACITANCE_DIMENSIONS)
    MICROFARAD = Unit('microfarad', 'μF', CAPACITANCE_DIMENSIONS)
    NANOFARAD = Unit('nanofarad', 'nF', CAPACITANCE_DIMENSIONS)
    PICOFARAD = Unit('picofarad', 'pF', CAPACITANCE_DIMENSIONS)

# Electrical Resistance Unit
class ResistanceUnits(Enum):
    OHM = Unit('ohm', 'Ω', RESISTANCE_DIMENSIONS)          
    MILLIOHM = Unit('milliohm', 'mΩ', RESISTANCE_DIMENSIONS)
    MICROOHM = Unit('microohm', 'μΩ', RESISTANCE_DIMENSIONS)
    KILOHM = Unit('kilohm', 'kΩ', RESISTANCE_DIMENSIONS)
    MEGAOHM = Unit('megaohm', 'MΩ', RESISTANCE_DIMENSIONS)
    GIGOHM = Unit('gigohm', 'GΩ', RESISTANCE_DIMENSIONS)


# Electrical Conductance Unit
class ConductanceUnits(Enum):
    SIEMENS = Unit('siemens', 'S', CONDUCTANCE_DIMENSIONS)
    MILLI_SIEMENS = Unit('milli siemens', 'mS', CONDUCTANCE_DIMENSIONS)
    KILO_SIEMENS = Unit('kilo siemens', 'kS', CONDUCTANCE_DIMENSIONS)
    MEGA_SIEMENS = Unit('mega siemens', 'MS', CONDUCTANCE_DIMENSIONS)
    GIGA_SIEMENS = Unit('giga siemens', 'GS', CONDUCTANCE_DIMENSIONS)

# Illumination Unit (Luminous Flux/Area)
class IlluminationUnits(Enum):
    
    LUX = Unit('lux', 'lx',ILLUMINATION_DIMENSIONS)
    FOOT_CANDLE = Unit('foot-candle', 'fc',ILLUMINATION_DIMENSIONS)
    MILLILUX = Unit('millilux', 'mlx',ILLUMINATION_DIMENSIONS)
    MICROLUX = Unit('microlux', 'μlx',ILLUMINATION_DIMENSIONS)
    KILOLUX = Unit('kilolux', 'klx',ILLUMINATION_DIMENSIONS)
    MEGALUX = Unit('megalux', 'mlx',ILLUMINATION_DIMENSIONS)

# Angle Unit
class AngleUnits(Enum):
    DEGREE = Unit('degree', '°', ANGLE_DIMENSIONS)     # Degrees
    RADIAN = Unit('radian', 'rad', ANGLE_DIMENSIONS)    # Radians
    GRADIAN = Unit('gradian', 'gon', ANGLE_DIMENSIONS)  # Gradians
    ARC_MINUTE = Unit('arcminute', "'", ANGLE_DIMENSIONS)  # Arcminutes (1/60 of a degree)
    ARC_SECOND = Unit('arcsecond', '″', ANGLE_DIMENSIONS)  # Arcseconds (1/3600 of a degree)

# Area Unit
class AreaUnits(Enum):
    SQUARE_METER = Unit('square meter', 'm²', AREA_DIMENSIONS)          
    SQUARE_CENTIMETER = Unit('square centimeter', 'cm²', AREA_DIMENSIONS)
    SQUARE_DECIMETER = Unit('square decimeter', 'dm²', AREA_DIMENSIONS)
    SQUARE_MILLIMETER = Unit('square millimeter', 'mm²', AREA_DIMENSIONS)
    SQUARE_KILOMETER = Unit('square kilometer', 'km²', AREA_DIMENSIONS)
    SQUARE_INCH = Unit('square inch', 'in²', AREA_DIMENSIONS)
    SQUARE_FOOT = Unit('square foot', 'ft²', AREA_DIMENSIONS)
    SQUARE_YARD = Unit('square yard', 'yd²', AREA_DIMENSIONS)
    SQUARE_MILE = Unit('square mile', 'mile²', AREA_DIMENSIONS)
    ACRE = Unit('acre', 'acre', AREA_DIMENSIONS)
    HECTARE = Unit('hectare', 'ha', AREA_DIMENSIONS)

# Volume Unit
class VolumeUnits(Enum):
    CUBIC_METER = Unit('cubic meter', 'm³', VOLUME_DIMENSIONS)
    CUBIC_CENTIMETER = Unit('cubic centimeter', 'cm³', VOLUME_DIMENSIONS)
    CUBIC_DECIMETER = Unit('cubic decimeter', 'dm³', VOLUME_DIMENSIONS)
    CUBIC_MILLIMETER = Unit('cubic millimeter', 'mm³', VOLUME_DIMENSIONS)
    CUBIC_KILOMETER = Unit('cubic kilometer', 'km³', VOLUME_DIMENSIONS)
    LITER = Unit('liter', 'l', VOLUME_DIMENSIONS)
    MILLILITER = Unit('milliliter', 'ml', VOLUME_DIMENSIONS)
    CUBIC_FOOT = Unit('cubic foot', 'ft³', VOLUME_DIMENSIONS)
    CUBIC_INCH = Unit('cubic inch', 'in³', VOLUME_DIMENSIONS)
    CUBIC_YARD = Unit('cubic yard', 'yd³', VOLUME_DIMENSIONS)
    GALLON_US = Unit('gallon (US)', 'gal (US)', VOLUME_DIMENSIONS)
    GALLON_UK = Unit('gallon (UK)', 'gal (UK)', VOLUME_DIMENSIONS)

# Flow Rate Unit (Volume/Time)
class FlowRateUnits(Enum):
    CUBIC_METER_PER_SECOND = Unit('cubic meter per second', 'm³/s', FLOW_RATE_DIMENSIONS)
    LITER_PER_SECOND = Unit('liter per second', 'L/s', FLOW_RATE_DIMENSIONS)
    GALLON_PER_MINUTE = Unit('gallon per minute', 'gal/min', FLOW_RATE_DIMENSIONS)
    MILLILITER_PER_SECOND = Unit('milliliter per second', 'ml/s', FLOW_RATE_DIMENSIONS)
    CUBIC_CENTIMETER_PER_SECOND = Unit('cubic centimeter per second', 'cm³/s', FLOW_RATE_DIMENSIONS)
    CUBIC_INCH_PER_SECOND = Unit('cubic inch per second', 'in³/s', FLOW_RATE_DIMENSIONS)
    CUBIC_KILOMETER_PER_SECOND = Unit('cubic kilometer per second', 'km³/s', FLOW_RATE_DIMENSIONS)
    CUBIC_METER_PER_HOUR = Unit('cubic meter per hour', 'm³/h', FLOW_RATE_DIMENSIONS)
    CUBIC_METER_PER_MINUTE = Unit('cubic meter per minute', 'm³/min', FLOW_RATE_DIMENSIONS)

# Mass Flow Rate Unit (Mass/Time)
class MassFlowRateUnits(Enum):
    KILOGRAM_PER_SECOND = Unit('kilogram per second', 'kg/s', MASS_FLOW_RATE_DIMENSIONS)
    GRAM_PER_SECOND = Unit('gram per second', 'g/s', MASS_FLOW_RATE_DIMENSIONS)
    TON_PER_SECOND = Unit('ton per second', 'ton/s', MASS_FLOW_RATE_DIMENSIONS)
    MILLIGRAM_PER_SECOND = Unit('milligram per second', 'mg/s', MASS_FLOW_RATE_DIMENSIONS)
    MICROGRAM_PER_SECOND = Unit('microgram per second', 'μg/s', MASS_FLOW_RATE_DIMENSIONS)
    NANOGRAM_PER_SECOND = Unit('nanogram per second', 'ng/s', MASS_FLOW_RATE_DIMENSIONS)
    KILOGRAM_PER_HOUR = Unit('kilogram per hour', 'kg/h', MASS_FLOW_RATE_DIMENSIONS)
    TON_PER_HOUR = Unit('ton per hour', 'ton/h', MASS_FLOW_RATE_DIMENSIONS)
    POUND_PER_SECOND = Unit('pound per second', 'lb/s', MASS_FLOW_RATE_DIMENSIONS)
    OUNCE_PER_SECOND = Unit('ounce per second', 'oz/s', MASS_FLOW_RATE_DIMENSIONS)
    KILOGRAM_PER_MINUTE = Unit('kilogram per minute', 'kg/min', MASS_FLOW_RATE_DIMENSIONS)
    GRAM_PER_MINUTE = Unit('gram per minute', 'g/min', MASS_FLOW_RATE_DIMENSIONS)
    MILLIGRAM_PER_MINUTE = Unit('milligram per minute', 'mg/min', MASS_FLOW_RATE_DIMENSIONS)
    POUND_PER_MINUTE = Unit('pound per minute', 'lb/min', MASS_FLOW_RATE_DIMENSIONS)
    OUNCE_PER_MINUTE = Unit('ounce per minute', 'oz/min', MASS_FLOW_RATE_DIMENSIONS)

# Speed Unit (Distance/Time)
class SpeedUnits(Enum):
    METER_PER_SECOND = Unit('meter per second', 'm/s', SPEED_DIMENSIONS)
    KILOMETER_PER_HOUR = Unit('kilometer per hour', 'km/h', SPEED_DIMENSIONS)
    MILE_PER_HOUR = Unit('mile per hour', 'mph', SPEED_DIMENSIONS)
    KNOT = Unit('knot', 'kn', SPEED_DIMENSIONS)
    MILLIMETER_PER_SECOND = Unit('millimeter per second', 'mm/s', SPEED_DIMENSIONS)
    CENTIMETER_PER_SECOND = Unit('centimeter per second', 'cm/s', SPEED_DIMENSIONS)
    MICROMETER_PER_SECOND = Unit('micrometer per second', 'μm/s', SPEED_DIMENSIONS)
    KILOMETER_PER_SECOND = Unit('kilometer per second', 'km/s', SPEED_DIMENSIONS)
    MILE_PER_SECOND = Unit('mile per second', 'mi/s', SPEED_DIMENSIONS)

# Acceleration Unit (Distance/Time^2)
class AccelerationUnits(Enum):
    METER_PER_SECOND_SQUARED = Unit('meter per second squared', 'm/s²', ACCELERATION_DIMENSIONS)
    KILOMETER_PER_HOUR_SQUARED = Unit('kilometer per hour squared', 'km/h²', ACCELERATION_DIMENSIONS)
    MILE_PER_HOUR_SQUARED = Unit('mile per hour squared', 'mph²', ACCELERATION_DIMENSIONS)
    CENTIMETER_PER_SECOND_SQUARED = Unit('centimeter per second squared', 'cm/s²', ACCELERATION_DIMENSIONS)
    MILLIMETER_PER_SECOND_SQUARED = Unit('millimeter per second squared', 'mm/s²', ACCELERATION_DIMENSIONS)
    G_FORCE = Unit('g-force', 'g', ACCELERATION_DIMENSIONS)  # Assuming 1 g = 9.80665 m/s² for context

# Thermal conductivity Unit
class ThermalConductivityUnits(Enum):
    WATT_PER_METER_KELVIN = Unit('watt per meter kelvin', 'W/m·K', THERMAL_CONDUCTIVITY_DIMENSIONS)
    MILLIWATT_PER_METER_KELVIN = Unit('milliwatt per meter kelvin', 'mW/m·K', THERMAL_CONDUCTIVITY_DIMENSIONS)
    KILOWATT_PER_METER_KELVIN = Unit('kilowatt per meter kelvin', 'kW/m·K', THERMAL_CONDUCTIVITY_DIMENSIONS)
    BTU_PER_HOUR_FOOT_FAHRENHEIT = Unit('BTU per hour foot fahrenheit', 'BTU/h·ft·°F', THERMAL_CONDUCTIVITY_DIMENSIONS)
    CALORIE_PER_SECOND_CENTIMETER_CELSIUS = Unit('calorie per second centimeter celsius', 'cal/s·cm·°C', THERMAL_CONDUCTIVITY_DIMENSIONS)
    WATT_PER_CENTIMETER_CELSIUS = Unit('watt per centimeter celsius', 'W/cm·°C', THERMAL_CONDUCTIVITY_DIMENSIONS)

# Thermal Resistance Unit
class ThermalResistanceUnits(Enum):
    KELVIN_PER_WATT = Unit('kelvin per watt', 'K/W', THERMAL_RESISTANCE_DIMENSIONS)
    MILLIKELVIN_PER_WATT = Unit('millikelvin per watt', 'mK/W', THERMAL_RESISTANCE_DIMENSIONS)
    MICROKELVIN_PER_WATT = Unit('microkelvin per watt', 'μK/W', THERMAL_RESISTANCE_DIMENSIONS)
    KILOKELVIN_PER_WATT = Unit('kilokelvin per watt', 'kK/W', THERMAL_RESISTANCE_DIMENSIONS)
    MEGAKELVIN_PER_WATT = Unit('megakelvin per watt', 'MK/W', THERMAL_RESISTANCE_DIMENSIONS)
    GIGAKELVIN_PER_WATT = Unit('gigakelvin per watt', 'GK/W', THERMAL_RESISTANCE_DIMENSIONS)

# Mock Unit (for testing/mock)
class MockUnits(Enum):
    MOCK_UNIT=Unit('mock unit','mock',None)
    
if __name__=='__main__':
    test_unit = MassUnits.KILOGRAM.value  # Now this will give you the Unit object
    print(repr(test_unit))
    print(test_unit)  # Should print the string representation of the Unit object