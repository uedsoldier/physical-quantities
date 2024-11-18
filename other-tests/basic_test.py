import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from modules.physical_quantities import MassQuantity
from modules.physical_quantities import TimeQuantity
from modules.unit import *

m1 = MassQuantity(15,MassUnits.KILOGRAM.value)
m2 = MassQuantity(2,MassUnits.KILOGRAM.value)
print(f'Sum of same units: {m1} + {m2} = {m1+m2} ')

m1 = m1.convert_to(MassUnits.POUND.value)
m2 = m2.convert_to(MassUnits.POUND.value)

print(f'Sum of same units (after some conversion): {m1} + {m2} = {m1+m2} ')


m1 = MassQuantity(5,MassUnits.KILOGRAM.value)
m2 = MassQuantity(2,MassUnits.KILOGRAM.value)
print(f'Sub of same units: {m1} - {m2} = {m1-m2} ')

m1 = m1.convert_to(MassUnits.POUND.value)
m2 = m2.convert_to(MassUnits.POUND.value)

print(f'Sub of same units (after some conversion): {m1} - {m2} = {m1-m2} ')

t1 = TimeQuantity(30,TimeUnits.SECOND.value)




print(m1/t1)

print(repr(m1/t1))