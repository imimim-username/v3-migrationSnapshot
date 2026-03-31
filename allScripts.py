#this script will run through the component scripts in sequence

import os
import time
from datetime import datetime

def ts():
    return datetime.now().strftime('%H:%M:%S')

script_one = 'duneApp.py'
script_two = 'sum.py'
script_three = 'getDebts.py'

start = time.perf_counter()

print(f'[{ts()}] ── Phase 1 of 3: {script_one} (Dune queries + RPC balance fetches) ──')
t1 = time.perf_counter()
os.system(f'python {script_one}')
print(f'[{ts()}] Phase 1 done in {int(time.perf_counter()-t1)}s')

print(f'\n[{ts()}] ── Phase 2 of 3: {script_two} (sum + normalize balances) ──')
t2 = time.perf_counter()
os.system(f'python {script_two}')
print(f'[{ts()}] Phase 2 done in {int(time.perf_counter()-t2)}s')

print(f'\n[{ts()}] ── Phase 3 of 3: {script_three} (fetch debts) ──')
t3 = time.perf_counter()
os.system(f'python {script_three}')
print(f'[{ts()}] Phase 3 done in {int(time.perf_counter()-t3)}s')

elapsed = time.perf_counter() - start
minutes, seconds = divmod(int(round(elapsed)), 60)
hours, minutes = divmod(minutes, 60)
if hours:
    print(f'\nFinished in {hours}h {minutes}m {seconds}s')
elif minutes:
    print(f'\nFinished in {minutes}m {seconds}s')
else:
    print(f'\nFinished in {seconds}s')