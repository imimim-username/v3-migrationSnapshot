from dotenv import load_dotenv
import os

import requests

import pandas as pd

load_dotenv()

graphApiKey = os.getenv("GRAPH_API_KEY")
alchemyApiKey = os.getenv("ALCHEMY_API_KEY")


def getGraphBalances(multiplier, graphURL, yieldToken):

    thousand = str(multiplier * 1000)

    headers = {
        "Content-Type": "application/json"
    }

    query = """
    {
        alchemistBalances(
            orderBy: account__id
            orderDirection: asc
            where: {shares_gt: "10", yieldToken_: {id: \"""" + yieldToken + """\"}}
            first: 1000
            skip: """ + thousand + """
        ) {
            account {
            id
            }
            id
            shares
            underlyingValue
            yieldToken {
            id
            name
            symbol
            }
        }
    }
    """

    data = {
        "query" : query
    }

    
    queryResponse = requests.post(graphURL, json=data, headers=headers).json()

    return queryResponse

def buildBalances(url):

    
    balances = []

    headers = {
        "Content-Type": "application/json"
    }

    yieldTokenQuery = """
    {
        yieldTokens {
            id
            name
            symbol
        }
    }
    """

    data = {
        "query" : yieldTokenQuery
    }

    queryResponse = requests.post(url, json=data, headers=headers).json()

    yieldTokens = queryResponse['data']['yieldTokens']

    for yieldToken in yieldTokens:
        keepGoing = True
        multiplier = 0
        print('Getting balances for ' + yieldToken['name'] + '...')
        while keepGoing:
            tempBalances = getGraphBalances(multiplier, url, yieldToken['id'])['data']['alchemistBalances']
            
            for balance in tempBalances:
                tempThing = {
                    'address': balance['account']['id'],
                    'shares': balance['shares'],
                    'underlyingValue': balance['underlyingValue'],
                    'yieldToken': balance['yieldToken']['id'],
                    'yieldTokenName': balance['yieldToken']['name'],
                    'yieldTokenSymbol': balance['yieldToken']['symbol'],
                }
                balances.append(tempThing)
            
            thousandThing = len(tempBalances) % 1000
            print('Number of balances: ' + str(len(tempBalances)))

            if thousandThing > 0:
                keepGoing = False
            else:
                multiplier += 1

    return balances

mainnetGraphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/GJ9CJ66TgbJnXcXGuZiSYAdGNkJBAwqMcKHEvfVmCkdG'
print('Getting mainnet balances...')
balances = buildBalances(mainnetGraphURL)
print('Saving to CSV...')
df = pd.DataFrame(balances)
df.to_csv('MainnetBalances.csv', index=False)
print('Saved to CSV')

optimismGraphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/GYBJ8wsQFkSwcgCqhaxnz5RU2VbgedAkWUk2qx9gTnzr'
print('Getting optimism balances...')
balances = buildBalances(optimismGraphURL)
print('Saving to CSV...')
df = pd.DataFrame(balances)
df.to_csv('OptimismBalances.csv', index=False)
print('Saved to CSV')

arbitrumGraphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/Dgjyhh69XooHPd4JjvT3ik9FaGAR3w7sUSQyQ1YDakGp'
print('Getting arbitrum balances...')
balances = buildBalances(arbitrumGraphURL)
print('Saving to CSV...')
df = pd.DataFrame(balances)
df.to_csv('ArbitrumBalances.csv', index=False)
print('Saved to CSV')