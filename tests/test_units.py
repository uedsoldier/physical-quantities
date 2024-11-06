
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.unit import Unit, Dimensions

meter = Unit("meter", "m", Dimensions({"L": 1}))
second = Unit("second", "s", Dimensions({"T": 1}))
kilogram = Unit("kilogram", "kg", Dimensions({"M": 1}))
area = meter * meter
volume = meter * meter * meter

newton = Unit("Newton", "N", Dimensions({"M": 1, "L": 1, "T": -2}))  # 1 N = 1 kg * m/s^2
pascal = Unit('Pascal','Pa',Dimensions({"M": 1, "L": -1, "T": -2}))

print(f'Raw kgm/s^2: {(kilogram*meter)/(second*second)}')
print(f'Newton: {newton}')

print(f'Raw kg/(m*s^2): {kilogram/(meter*second*second)}')
print(f'Pascal: {pascal}')

print(f'Area: {area}')
print(f'Volume: {volume}')