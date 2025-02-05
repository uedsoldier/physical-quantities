import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.physical_quantities import VoltageQuantity, ElectricCurrentQuantity, PowerQuantity
from modules.unit import VoltageUnits, ElectricCurrentUnits, PowerUnits

class ComponentsTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass
    
    def test_