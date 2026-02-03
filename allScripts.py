#this script will run through the component scripts in sequence

import os

script_one = 'duneApp.py'
script_two = 'sum.py'
script_three = 'getDebts.py'

os.system(f'python {script_one}')
os.system(f'python {script_two}')
os.system(f'python {script_three}')