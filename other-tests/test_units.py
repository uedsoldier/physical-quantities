
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from modules.unit import Unit, Dimensions, MassUnits, LengthUnits, TimeUnits, ForceUnits, EnergyUnits

meter = Unit("meter", "m", Dimensions({"L": 1}))
second = Unit("second", "s", Dimensions({"T": 1}))
kilogram = Unit("kilogram", "kg", Dimensions({"M": 1}))
area = meter * meter
volume = meter * meter * meter
length_4 = volume * meter

newton = Unit("Newton", "N", Dimensions({"M": 1, "L": 1, "T": -2}))  # 1 N = 1 kg * m/s^2
pascal = Unit('Pascal','Pa',Dimensions({"M": 1, "L": -1, "T": -2}))

print(f'Raw kgm/s^2: {(kilogram*meter)/(second*second)}')
print(f'Newton: {newton}')
print(repr(newton))

print(f'Raw kg/(m*s^2): {kilogram/(meter*second*second)}')
print(f'Pascal: {pascal}')
print(repr(pascal))

print(f'Area: {area}')
print(repr(area))
print(f'Volume: {volume}')
print(repr(volume))

print(f'Length^4: {length_4}')

test_mass = MassUnits.KILOGRAM.value
test_length = LengthUnits.METER.value
test_time = TimeUnits.SECOND.value
test_force = ForceUnits.NEWTON.value
print(test_mass)

print('------------------------------')
print('Types checking')
print(type(kilogram))
print(type(test_mass))

print(type(meter))
print(type(test_length))

print('------------------------------')

print(kilogram*kilogram)
print(test_mass*test_mass)

print(meter*meter)
print(test_length*test_length)
print(test_time*test_time)
print(test_force*test_force)


print((test_mass * test_length) / (test_time * test_time))

test_work = ForceUnits.POUND_FORCE.value * LengthUnits.FOOT.value
print(test_work )
print(repr(test_work))

print(repr(EnergyUnits.FOOT_POUND))