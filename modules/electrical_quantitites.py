from modules.physical_quantities import Current, Voltage, Frequency, Angle, BaseConversionManager
from math import isclose, sqrt, pi

ABS_TOLERANCE_FROM_ZERO: float = 1e-6
SQRT_2: float = 1.4142135623730950488


def normalize_phase(phase_angle: Angle):
    """
    Normalize phase angle to be in the -180 to 180 degrees range
    Args:
        phase_angle (Angle): _description_
    """
    original_unit: str = phase_angle.unit
    conversion_manager = BaseConversionManager('angle')
    phase_angle_rad = conversion_manager.convert(phase_angle.value, original_unit, 'rad')
    # Normalize phase to be within the range of -pi to pi radians
    while(phase_angle_rad <= -pi):
        phase_angle_rad += 2*pi
    while(phase_angle_rad > pi):
        phase_angle_rad -= 2*pi
    phase_angle.value = conversion_manager.convert(phase_angle_rad, 'rad', original_unit)
    
class AC_Voltage():
    def __init__(self, rms_value: Voltage, frequency: Frequency, phase_angle: Angle = 0) -> None:
        """AC voltage object
        Args:
            rms_value (Voltage): Root mean square equivalent value
            frequency (Frequency): Frequency of the AC wave
            phase_angle (Angle, optional): Phase angle. Defaults to 0.

        Raises:
            ValueError: _description_
        """
        if(frequency.value < 0.0 or isclose(frequency.value,0.0,abs_tol=ABS_TOLERANCE_FROM_ZERO,rel_tol=0)):
            raise ValueError('Frequency must be positive and different from zero (0)')
        self._rms_value = rms_value
        self._amplitude: Voltage = Voltage(rms_value.value * SQRT_2, rms_value.unit)
        self._frequency = frequency
        normalize_phase(phase_angle)
        self._phase_angle = phase_angle
        
    def __str__(self) -> str:
        return f'{self._rms_value} RMS @ {self._frequency} ϕ = {self._phase_angle}'