import unittest

from physical_quantities.conversion import BaseConversionManager
from physical_quantities.units import FlowRateUnits
from .base_converter_test import BaseConversionTest


class TestFlowRateConverter(BaseConversionTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.conversion_manager = BaseConversionManager("flow_rate")

    standard_unit = FlowRateUnits.CUBIC_METER_PER_SECOND.value

    test_cases = [
        (1, FlowRateUnits.CUBIC_METER_PER_SECOND.value, FlowRateUnits.LITER_PER_SECOND.value, 1000, 6),
        (1, FlowRateUnits.LITER_PER_SECOND.value, FlowRateUnits.MILLILITER_PER_SECOND.value, 1000, 6),
        (1, FlowRateUnits.CUBIC_CENTIMETER_PER_SECOND.value, FlowRateUnits.MILLILITER_PER_SECOND.value, 1, 6),
        (3600, FlowRateUnits.CUBIC_METER_PER_HOUR.value, FlowRateUnits.CUBIC_METER_PER_SECOND.value, 1, 6),
        (60, FlowRateUnits.CUBIC_METER_PER_MINUTE.value, FlowRateUnits.CUBIC_METER_PER_SECOND.value, 1, 6),
        (1, FlowRateUnits.CUBIC_METER_PER_HOUR.value, FlowRateUnits.LITER_PER_SECOND.value, 0.2777777778, 6),
        # 1 US gal/min = 3.785411784 L / 60 s
        (1, FlowRateUnits.GALLON_PER_MINUTE.value, FlowRateUnits.LITER_PER_SECOND.value, 0.0630901964, 6),
    ]


if __name__ == "__main__":
    unittest.main()
