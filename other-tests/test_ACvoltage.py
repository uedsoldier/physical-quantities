import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from core.electrical_quantitites import AC_Voltage
from core.physical_quantities import VoltageQuantity, FrequencyQuantity, AngleQuantity, BaseConversionManager
from math import pi 

voltage = VoltageQuantity(0.5,'kV')
frequency = FrequencyQuantity(60)
phase = AngleQuantity(0.125*pi,'rad')

conversion_manager = BaseConversionManager('angle')

ac_voltage = AC_Voltage(voltage,frequency,phase)
ac_voltage._phase_angle.value = conversion_manager.convert(ac_voltage._phase_angle.value, phase.unit, 'deg')

conversion_manager = BaseConversionManager.change_quantity_type('voltage')
ac_voltage._rms_value.value = conversion_manager.convert(ac_voltage._rms_value.value, voltage.unit, 'mV')
ac_voltage._rms_value.unit = 'mV'

print(ac_voltage)