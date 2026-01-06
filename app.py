from dotenv import load_dotenv
import os

import requests

import pandas as pd

load_dotenv()

graphApiKey = os.getenv("GRAPH_API_KEY")
alchemyApiKey = os.getenv("ALCHEMY_API_KEY")


def getGraphBalances(multiplier, graphURL):

    thousand = str(multiplier * 1000)

    query = """
    {
        alchemistBalances(
            orderBy: account__id
            orderDirection: asc
            where: {shares_gt: "0"}
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

    headers = {
        "Content-Type": "application/json"
    }

    queryResponse = requests.post(graphURL, json=data, headers=headers).json()

    return queryResponse

keepGoing = True
multiplier = 1

balances = []

mainnetGraphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/GJ9CJ66TgbJnXcXGuZiSYAdGNkJBAwqMcKHEvfVmCkdG'

while keepGoing:
    tempBalances = getGraphBalances(multiplier, mainnetGraphURL)['data']['alchemistBalances']
    
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

print('Saving to CSV...')
df = pd.DataFrame(balances)
df.to_csv('MainnetBalances.csv', index=False)
print('Saved to CSV')