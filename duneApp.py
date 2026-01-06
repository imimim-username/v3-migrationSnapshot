from dotenv import load_dotenv
import os
import requests
import pandas as pd

from runDuneQuery import updateQuery, getQuery #(inputID)
from rpcCall import rpcCall #(targetAddress, dataString, blockNumber, chain)

def getBalances(address, alchemist, vault, chain):
# example: {"jsonrpc":"2.0","id":7189484897142231,"method":"eth_call","params":[{"from":"0x0000000000000000000000000000000000000000","data":"0x4bd214450000000000000000000000002330eb2d92167c3b6b22690c03b508e0ca532980000000000000000000000000a258c4606ca8206d8aa700ce2143d7db854d168c","to":"0x062bf725dc4cdf947aa79ca2aaccd4f385b13b5c"},"latest"]}

    dataString = '0x4bd21445000000000000000000000000' + address[2:] + '000000000000000000000000' + vault[2:]
    blockNumber = 'latest'

    rpcData = rpcCall(alchemist, dataString, blockNumber, chain)
    #print(rpcData)
    balance = int(rpcData[:66], 16)
    
    return balance

mainnetInfo = {
    'queryID': 6475554, # dune query with all depositor addresses
    'alchemists': [ # the alchemists 
        {
            'name': 'alETH',
            'address': '0x062Bf725dC4cDF947aa79Ca2aaCCD4F385b13b5c',
            'vaults': [
                {
                    'name': 'yvWETH',
                    'address': '0xa258c4606ca8206d8aa700ce2143d7db854d168c'
                },
                {
                    'name': 'wstETH',
                    'address': '0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0'
                },
                {
                    'name': 'rETH',
                    'address': '0xae78736cd615f374d3085123a210448e74fc6393'
                },
                {
                    'name': 'aWETH',
                    'address': '0x61134511187a9a2df38d10dbe07ba2e8e5563967'
                },
                {
                    'name': 'vaETH',
                    'address': '0xd1c117319b3595fbc39b471ab1fd485629eb05f2'
                },
                {
                    'name': 'sfrxETH',
                    'address': '0xac3E018457B222d93114458476f3E3416Abbe38F'
                },
                {
                    'name': 'apxETH',
                    'address': '0x9Ba021B0a9b958B5E75cE9f6dff97C7eE52cb3E6'
                }
            ]
        },
        {
            'name': 'alUSD',
            'address': '0x5C6374a2ac4EBC38DeA0Fc1F8716e5Ea1AdD94dd',
            'vaults': [
                {
                    'name': 'yvDAI',
                    'address': '0xda816459f1ab5631232fe5e97a05bbbb94970c95'
                },
                {
                    'name': 'yvUSDC',
                    'address': '0xa354f35829ae975e850e23e9615b11da1b3dc4de'
                },
                {
                    'name': 'yvUSDT',
                    'address': '0x7da96a3891add058ada2e826306d812c638d87a7'
                },
                {
                    'name': 'aDAI',
                    'address': '0xce4a49d7ed99c7c8746b713ee2f0c9aa631688d8'
                },
                {
                    'name': 'aUSDT',
                    'address': '0xbc11de1f20e83f0a6889b8c7a7868e722694e315'
                },
                {
                    'name': 'yvUSDT',
                    'address': '0x3b27f92c0e212c671ea351827edf93db27cc0c65'
                },
                {
                    'name': 'vaUSDC',
                    'address': '0xa8b607aa09b6a2e306f93e74c282fb13f6a80452'
                },
                {
                    'name': 'vaDAI',
                    'address': '0x0538C8bAc84E95A9dF8aC10Aad17DbE81b9E36ee'
                },
                {
                    'name': 'vaFRAX',
                    'address': '0xc14900dFB1Aa54e7674e1eCf9ce02b3b35157ba5'
                },
                {
                    'name': 'aFRAX',
                    'address': '0x318334A6dD21d16A8442aB0b7204E81Aa3FB416E'
                }
            ]
        }
    ]
}

optimismInfo = {
    'queryID': 6475582, # dune query with all depositor addresses
    'alchemists': [ # the alchemists 
        {
            'name': 'alETH',
            'address': '0xe04Bb5B4de60FA2fBa69a93adE13A8B3B569d5B4',
            'vaults': [
                {
                    'name': 'aWETH',
                    'address': '0x337B4B933d60F40CB57DD19AE834Af103F049810'
                },
                {
                    'name': 'wstETH',
                    'address': '0x1F32b1c2345538c0c6f582fCB022739c4A194Ebb'
                },
                {
                    'name': 'ysWETH',
                    'address': '0xE62DDa84e579e6A37296bCFC74c97349D2C59ce3'
                }
            ]
        },
        {
            'name': 'alUSD',
            'address': '0x10294d57A419C8eb78C648372c5bAA27fD1484af',
            'vaults': [
                {
                    'name': 'aDAI',
                    'address': '0x43A502D7e947c8A2eBBaf7627E104Ddcc253aBc6'
                },
                {
                    'name': 'aUSDC',
                    'address': '0x4186Eb285b1efdf372AC5896a08C346c7E373cC4'
                },
                {
                    'name': 'aUSDT',
                    'address': '0x2680b58945A31602E4B6122C965c2849Eb76Dd3B'
                },
                {
                    'name': 'ysUSDC',
                    'address': '0x059Eaa296B18E0d954632c8242dDb4a271175EeD'
                },
                {
                    'name': 'ysDAI',
                    'address': '0x0A86aDbF58424EE2e304b395aF0697E850730eCD'
                }
            ]
        }
    ]
}

arbitrumInfo = {
    'queryID': 6475592, # dune query with all depositor addresses
    'alchemists': [ # the alchemists 
        {
            'name': 'alETH',
            'address': '0x654e16a0b161b150F5d1C8a5ba6E7A7B7760703A',
            'vaults': [
                {
                    'name': 'wstETH',
                    'address': '0x5979D7b546E38E414F7E9822514be443A4800529'
                },
                {
                    'name': 'farmdWETHV3',
                    'address': '0xf3b7994e4da53e04155057fd61dc501599d57877'
                }
            ]
        },
        {
            'name': 'alUSD',
            'address': '0xb46eE2E4165F629b4aBCE04B7Eb4237f951AC66F',
            'vaults': [
                {
                    'name': 'aUSDC',
                    'address': '0x248a431116c6f6FCD5Fe1097d16d0597E24100f5'
                }
            ]
        }
    ]
}

mainnetBalances = []
for alchemist in mainnetInfo['alchemists']:
    counter = 0
    print('Mainnet')
    print('Alchemist: ' + alchemist['name'])
    
    addresses = getQuery(mainnetInfo['queryID'])
    
    for vault in alchemist['vaults']:
        print('Vault: ' + vault['name'])    
        dataStr = '0x88e6f15a000000000000000000000000' + vault['address'][2:] 
        underlyingTokensPerShare = int(rpcCall(alchemist['address'], dataStr, 'latest', 'eth'), 16)
        print('Underlying Tokens Per Share: ' + str(underlyingTokensPerShare))

        dataStr = '0xa9aa5228000000000000000000000000' + vault['address'][2:]
        yieldTokensPerShare = int(rpcCall(alchemist['address'], dataStr, 'latest', 'eth'), 16)
        print('Yield Tokens Per Share: ' + str(yieldTokensPerShare))

        secondCounter = 0
        for address in addresses:
            balance = getBalances(address['address'], alchemist['address'], vault['address'], 'eth')
            print('Balance: ' + str(balance))
            
            if balance > 0:
                tempBalance = {
                    'address': address['address'],
                    'yieldToken': vault['name'],
                    'yieldTokenAddress': vault['address'],
                    'alchemist': alchemist['name'],
                    'alchemistAddress': alchemist['address'],
                    'shares': balance,
                    'underlyingTokensPerShare': underlyingTokensPerShare,
                    'yieldTokensPerShare': yieldTokensPerShare
                }
                mainnetBalances.append(tempBalance)
            secondCounter += 1

            if secondCounter >= 1:
                break

        counter += 1
        
        if counter >= 1:
            break
    print('--------------------------------')

print('Saving to CSV...')
df = pd.DataFrame(mainnetBalances)
df.to_csv('MainnetBalances-long_script.csv', index=False)
print('Saved to CSV')


optimismBalances = []
for alchemist in optimismInfo['alchemists']:
    counter = 0
    print('Optimism')
    print('Alchemist: ' + alchemist['name'])
    
    addresses = getQuery(optimismInfo['queryID'])
    
    for vault in alchemist['vaults']:
        print('Vault: ' + vault['name'])    
        dataStr = '0x88e6f15a000000000000000000000000' + vault['address'][2:] 
        underlyingTokensPerShare = int(rpcCall(alchemist['address'], dataStr, 'latest', 'op'), 16)
        print('Underlying Tokens Per Share: ' + str(underlyingTokensPerShare))

        dataStr = '0xa9aa5228000000000000000000000000' + vault['address'][2:]
        yieldTokensPerShare = int(rpcCall(alchemist['address'], dataStr, 'latest', 'op'), 16)
        print('Yield Tokens Per Share: ' + str(yieldTokensPerShare))

        secondCounter = 0
        for address in addresses:
            balance = getBalances(address['address'], alchemist['address'], vault['address'], 'op')
            print('Balance: ' + str(balance))

            if balance > 0:
                tempBalance = {
                    'address': address['address'],
                    'yieldToken': vault['name'],
                    'yieldTokenAddress': vault['address'],
                    'alchemist': alchemist['name'],
                    'alchemistAddress': alchemist['address'],
                    'shares': balance,
                    'underlyingTokensPerShare': underlyingTokensPerShare,
                    'yieldTokensPerShare': yieldTokensPerShare
                }
                optimismBalances.append(tempBalance)
            secondCounter += 1

            if secondCounter >= 1:
                break

        counter += 1
        
        if counter >= 1:
            break

    print('--------------------------------')

print('Saving to CSV...')
df = pd.DataFrame(optimismBalances)
df.to_csv('OptimismBalances-long_script.csv', index=False)
print('Saved to CSV')

#test = getBalances('0x2330eB2d92167c3b6B22690c03b508E0CA532980', '0x062Bf725dC4cDF947aa79Ca2aaCCD4F385b13b5c', '0xa258c4606ca8206d8aa700ce2143d7db854d168c', 'eth')

#print(test)