from modules.physical_quantities import Mass
from modules.physical_quantities import Time

m1 = Mass(15,'kg')
print(m1)

m1 = m1.convert_to('lb')
t1 = Time(30,'s')

print(t1)

print(m1.value/t1.value)