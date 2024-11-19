import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','../../modules')))

import subprocess
from termcolor import colored

tests = (
    "length",
    "mass",
    "temperature",
    "force",
    "time",
    "energy",
    "voltage",
    "frequency",
    "angle",
    "area",
    "volume",
    "pressure",
    "luminous_intensity",
    "speed",
    "mass_flow_rate",
    "electrical_resistance",
    "thermal_conductivity",
    "thermal_resistance",
)

for test in tests:
    test_path = f".\\test_{test}_converter.py"
    print(colored(f"Running <<{test}>> test", "cyan"))
    subprocess.run(f"python -m unittest -v {test_path}", shell=True)
