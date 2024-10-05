from modules.electrical_quantitites import AC_Voltage
from modules.physical_quantities import Voltage, Frequency, Angle, BaseConversionManager
from math import pi 

voltage = Voltage(0.5,'kV')
frequency = Frequency(60)
phase = Angle(0.125*pi,'rad')

conversion_manager = BaseConversionManager('angle')

ac_voltage = AC_Voltage(voltage,frequency,phase)
ac_voltage._phase_angle.value = conversion_manager.convert(ac_voltage._phase_angle.value, phase.unit, 'deg')

conversion_manager = BaseConversionManager.change_quantity_type('voltage')
ac_voltage._rms_value.value = conversion_manager.convert(ac_voltage._rms_value.value, voltage.unit, 'mV')
ac_voltage._rms_value.unit = 'mV'

print(ac_voltage)