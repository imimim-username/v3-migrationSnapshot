from dotenv import load_dotenv
import os

import requests

load_dotenv()

graphApiKey = os.getenv("GRAPH_API_KEY")
alchemyApiKey = os.getenv("ALCHEMY_API_KEY")


def getGraphBalances(multiplier):

    query = """
    {
        alchemistBalances(
            orderBy: account__id
            orderDirection: asc
            where: {shares_gt: "0"}
            first: 1000
            skip: 0
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

    graphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/GJ9CJ66TgbJnXcXGuZiSYAdGNkJBAwqMcKHEvfVmCkdG'

    queryResponse = requests.post(graphURL, json=data, headers=headers).json()

    return queryResponse

keepGoing = True
multiplier = 1

balances = []

while keepGoing:
    tempBalances = getGraphBalances(multiplier)['data']['alchemistBalances']
    balances.extend(tempBalances)
    
    thousandThing = len(tempBalances) % 1000
    print('Number of balances: ' + str(len(tempBalances)))

    if thousandThing > 0:
        keepGoing = False
    else:
        multiplier += 1