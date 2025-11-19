import unittest
from core.physical_quantities import BaseConversionManager
from core.unit import ResistanceUnits
from .base_converter_test import BaseConversionTest


class TestElectricalResistanceConverter(BaseConversionTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager("electrical_resistance")

    standard_unit = ResistanceUnits.OHM.value
    
    test_cases = [
            # Ohms to Milliohms
            (1.0, ResistanceUnits.OHM.value, ResistanceUnits.MILLIOHM.value, 1e3, 6),  
            # 1 Ω = 1000 mΩ
            # Milliohms to Ohms
            ( 1e3, ResistanceUnits.MILLIOHM.value, ResistanceUnits.OHM.value, 1.0, 6),  # 1000 mΩ = 1 Ω
            # Ohms to Microohms
            ( 1, ResistanceUnits.OHM.value, ResistanceUnits.MICROOHM.value, 1e6, 6),  # 1 Ω = 1,000,000 μΩ
            # Microohms to Ohms
            ( 1e6, ResistanceUnits.MICROOHM.value, ResistanceUnits.OHM.value, 1.0, 6),  # 1,000,000 μΩ = 1 Ω
            # Ohms to Kiloohms
            ( 1, ResistanceUnits.OHM.value, ResistanceUnits.KILOHM.value, 1e-3, 6),  # 1 Ω = 0.001 kΩ
            # Kiloohms to Ohms
            ( 1.0, ResistanceUnits.KILOHM.value, ResistanceUnits.OHM.value, 1e3, 6 ),  # 1kΩ = 1000  Ω
            # Ohms to Megaohms
            ( 1, ResistanceUnits.OHM.value, ResistanceUnits.MEGAOHM.value, 1e-6, 6 ),  # 1 Ω = 0.000001 MΩ
            # Megaohms to Ohms
            ( 1.0, ResistanceUnits.MEGAOHM.value, ResistanceUnits.OHM.value, 1.0e6, 6 ),  # 1 MΩ = 1,000,000 Ω
            # Ohms to Gigaohms
            ( 1e9, ResistanceUnits.OHM.value, ResistanceUnits.GIGOHM.value, 1, 6 ),  # 1 Ω = 0.000000001 GΩ
            # Gigaohms to Ohms
            ( 1, ResistanceUnits.GIGOHM.value, ResistanceUnits.OHM.value, 1.0e9, 6 ),  # 1 GΩ = 1,000,000,000 Ω
        ]

if __name__ == "__main__":
    unittest.main()
