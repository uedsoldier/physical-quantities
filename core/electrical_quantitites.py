from math import isclose, pi, remainder, tau

from .physical_quantities import AngleQuantity, FrequencyQuantity, VoltageQuantity
from .unit import AngleUnits

ABS_TOLERANCE_FROM_ZERO: float = 1e-6
SQRT_2: float = 1.4142135623730950488


def normalize_phase(phase_angle: AngleQuantity) -> AngleQuantity:
    """Normalize a phase angle to the (-180°, 180°] range.

    The input is not modified: a new quantity expressed in the original unit is returned.

    Args:
        phase_angle: Phase angle in any angle unit.

    Returns:
        A new AngleQuantity in the same unit as the input, within (-π, π] radians.
    """
    original_unit = phase_angle.unit
    radians = phase_angle.convert_to(AngleUnits.RADIAN.value).value
    # remainder() maps to [-π, π]; shift -π to π so the range is half-open on the left.
    normalized = remainder(radians, tau)
    if normalized <= -pi:
        normalized += tau
    normalized_angle = AngleQuantity(normalized, AngleUnits.RADIAN.value)
    return normalized_angle.convert_to(original_unit)


class AC_Voltage:
    def __init__(
        self,
        rms_value: VoltageQuantity,
        frequency: FrequencyQuantity,
        phase_angle: AngleQuantity | None = None,
    ) -> None:
        """AC voltage object.

        Args:
            rms_value: Root mean square equivalent value.
            frequency: Frequency of the AC wave.
            phase_angle: Phase angle. Defaults to 0°.

        Raises:
            ValueError: If the frequency is not strictly positive.
        """
        if frequency.value < 0.0 or isclose(
            frequency.value, 0.0, abs_tol=ABS_TOLERANCE_FROM_ZERO, rel_tol=0
        ):
            raise ValueError("Frequency must be positive and different from zero (0)")
        if phase_angle is None:
            phase_angle = AngleQuantity(0)
        self._rms_value = rms_value
        self._amplitude: VoltageQuantity = VoltageQuantity(
            rms_value.value * SQRT_2, rms_value.unit
        )
        self._frequency = frequency
        self._phase_angle = normalize_phase(phase_angle)

    def __str__(self) -> str:
        return f"{self._rms_value} RMS @ {self._frequency} ϕ = {self._phase_angle}"
