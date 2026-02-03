#gets debts.
import requests
import pandas as pd

from rpcCall import rpcCall #(targetAddress, dataString, blockNumber, chain)

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

for chain, files in startingFiles.items():
    for vault, fileName in files.items():
        df = pd.read_csv(fileName)
        print(df.head())

        counter = 0
        
        for index, row in df.iterrows():
            address = row['address'][2:]
            
            debt = int(rpcCall(alchemistAddresses[chain][vault], '0x5e5c06e2000000000000000000000000' + address, 'latest', chain)[:66], 16)
            print(debt)
            df.loc[index, "debt"] = debt
            counter += 1
            
            if counter >= 5:
                break

        newFileName = fileName.replace('pivot-', 'sum-and-debt-')
        df.to_csv(newFileName, index=False)
        print(f"Saved {newFileName}")