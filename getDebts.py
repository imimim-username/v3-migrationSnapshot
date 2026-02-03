#gets debts.
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from rpcCall import rpcCall  # (targetAddress, dataString, blockNumber, chain)

MAX_WORKERS = 10
PROGRESS_EVERY = 10
MAX_ROWS = None  # set to e.g. 5 for a quick test

startingFiles = {
    'eth': {
        'aleth': 'alEthValues-pivot-mainnet.csv',
        'alusd': 'alUsdValues-pivot-mainnet.csv'
    },
    'op': {
        'aleth': 'alEthValues-pivot-optimism.csv',
        'alusd': 'alUsdValues-pivot-optimism.csv'
    },
    'arb': {
        'aleth': 'alEthValues-pivot-arbitrum.csv',
        'alusd': 'alUsdValues-pivot-arbitrum.csv'
    }
}

alchemistAddresses = {
    'eth': {
        'aleth': '0x062Bf725dC4cDF947aa79Ca2aaCCD4F385b13b5c',
        'alusd': '0x5C6374a2ac4EBC38DeA0Fc1F8716e5Ea1AdD94dd'
    },
    'op': {
        'aleth': '0xe04Bb5B4de60FA2fBa69a93adE13A8B3B569d5B4',
        'alusd': '0x10294d57A419C8eb78C648372c5bAA27fD1484af'
    },
    'arb': {
        'aleth': '0x654e16a0b161b150F5d1C8a5ba6E7A7B7760703A',
        'alusd': '0xb46eE2E4165F629b4aBCE04B7Eb4237f951AC66F'
    }
}

def twos_complement(hex_value):
    # takes a hexadecimal string and returns the two's complement signed integer
    hex_digits = hex_value[2:] if hex_value.startswith('0x') else hex_value
    bits = len(hex_digits) * 4
    value = int(hex_value, 16)
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value


def fetch_debt(task):
    """Worker: takes (index, address, chain, vault), returns (index, debt). On RPC failure returns (index, None)."""
    index, address, chain, vault = task
    address_hex = address[2:] if address.startswith('0x') else address
    data_string = '0x5e5c06e2000000000000000000000000' + address_hex
    try:
        result = rpcCall(alchemistAddresses[chain][vault], data_string, 'latest', chain)
        debt = twos_complement(result[:66])
        return (index, debt)
    except Exception:
        return (index, None)


for chain, files in startingFiles.items():
    for vault, fileName in files.items():
        df = pd.read_csv(fileName)
        if 'debt' not in df.columns:
            df['debt'] = pd.NA

        rows = list(df.iterrows())
        if MAX_ROWS is not None:
            rows = rows[:MAX_ROWS]
        tasks = [(index, row['address'], chain, vault) for index, row in rows]
        total = len(tasks)

        print(f"Starting {chain}/{vault} ({total} rows)...")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(fetch_debt, t): t for t in tasks}
            completed = 0
            for future in as_completed(futures):
                index, debt = future.result()
                df.loc[index, 'debt'] = debt
                completed += 1
                if completed % PROGRESS_EVERY == 0 or completed == total:
                    pct = (100 * completed // total) if total else 0
                    print(f"[{chain}/{vault}] {completed} / {total} ({pct}%)")
        print(f"Done {chain}/{vault}.")

        newFileName = fileName.replace('pivot-', 'sum-and-debt-')
        df.to_csv(newFileName, index=False)
        print(f"Saved {newFileName}")
