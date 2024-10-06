import subprocess
from termcolor import colored

tests = (
    'length','mass','temperature','force','time','energy','voltage','frequency', 'angle', 'area', 'volume'
)

for test in tests:
    test_path = f'.\\test_{test}_converter.py'
    print(colored(f'Running <<{test}>> test','cyan'))
    subprocess.run(f'python -m unittest -v {test_path}', shell=True)