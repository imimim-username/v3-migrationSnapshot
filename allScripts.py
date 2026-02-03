#this script will run through the component scripts in sequence

import os
import time

script_one = 'duneApp.py'
script_two = 'sum.py'
script_three = 'getDebts.py'

start = time.perf_counter()

os.system(f'python {script_one}')
os.system(f'python {script_two}')
os.system(f'python {script_three}')

elapsed = time.perf_counter() - start
minutes, seconds = divmod(int(round(elapsed)), 60)
hours, minutes = divmod(minutes, 60)
if hours:
    print(f'\nFinished in {hours}h {minutes}m {seconds}s')
elif minutes:
    print(f'\nFinished in {minutes}m {seconds}s')
else:
    print(f'\nFinished in {seconds}s')