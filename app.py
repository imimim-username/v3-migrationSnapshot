from dotenv import load_dotenv
import os
import time

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

    try:
        response = requests.post(graphURL, json=data, headers=headers, timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        queryResponse = response.json()
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error fetching balances (multiplier {multiplier}): {e}")
        return {'data': {'alchemistBalances': []}, 'errors': [{'message': str(e)}]}
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return {'data': {'alchemistBalances': []}, 'errors': [{'message': 'Invalid JSON response'}]}
    
    # Check for GraphQL errors
    if 'errors' in queryResponse:
        print(f"GraphQL Error (multiplier {multiplier}): {queryResponse['errors']}")
        return {'data': {'alchemistBalances': []}, 'errors': queryResponse['errors']}
    
    # Check if 'data' key exists
    if 'data' not in queryResponse:
        print(f"Unexpected response structure (multiplier {multiplier}): {queryResponse}")
        return {'data': {'alchemistBalances': []}, 'errors': [{'message': 'Missing data key in response'}]}
    
    # Ensure alchemistBalances key exists
    if 'alchemistBalances' not in queryResponse['data']:
        print(f"Missing alchemistBalances in response (multiplier {multiplier})")
        return {'data': {'alchemistBalances': []}, 'errors': [{'message': 'Missing alchemistBalances key'}]}

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

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        queryResponse = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching yield tokens: {e}")
        return balances
    except ValueError as e:
        print(f"JSON decode error when fetching yield tokens: {e}")
        return balances
    
    # Check for GraphQL errors
    if 'errors' in queryResponse:
        print(f"GraphQL Error fetching yield tokens: {queryResponse['errors']}")
        return balances
    
    # Check if 'data' key exists
    if 'data' not in queryResponse or 'yieldTokens' not in queryResponse['data']:
        print(f"Error: Could not fetch yield tokens. Response: {queryResponse}")
        return balances

    yieldTokens = queryResponse['data']['yieldTokens']

    for yieldToken in yieldTokens:
        keepGoing = True
        multiplier = 0
        print('Getting balances for ' + yieldToken['name'] + '...')
        while keepGoing:
            response = getGraphBalances(multiplier, url, yieldToken['id'])
            
            # Check if we got a valid response
            if 'data' not in response or 'alchemistBalances' not in response['data']:
                print(f"Error fetching balances for {yieldToken['name']}, stopping pagination for this token")
                if 'errors' in response:
                    print(f"Errors: {response['errors']}")
                keepGoing = False
                break
            
            tempBalances = response['data']['alchemistBalances']
            
            # If we got an empty result, we're done
            if len(tempBalances) == 0:
                print(f"No more balances for {yieldToken['name']}")
                keepGoing = False
                break
            
            try:
                for balance in tempBalances:
                    # Validate required fields exist
                    if 'account' not in balance or 'yieldToken' not in balance:
                        print(f"Warning: Skipping invalid balance record: {balance}")
                        continue
                    
                    tempThing = {
                        'address': balance['account']['id'],
                        'shares': balance['shares'],
                        'underlyingValue': balance['underlyingValue'],
                        'yieldToken': balance['yieldToken']['id'],
                        'yieldTokenName': balance['yieldToken']['name'],
                        'yieldTokenSymbol': balance['yieldToken']['symbol'],
                    }
                    balances.append(tempThing)
            except KeyError as e:
                print(f"Error processing balance data: Missing key {e}")
                print(f"Balance record: {balance}")
                keepGoing = False
                break
            
            thousandThing = len(tempBalances) % 1000
            print('Number of balances: ' + str(len(tempBalances)))

            if thousandThing > 0:
                keepGoing = False
            else:
                multiplier += 1
                # Add a small delay to prevent rate limiting
                time.sleep(0.5)

    return balances

""" 
mainnetGraphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/GJ9CJ66TgbJnXcXGuZiSYAdGNkJBAwqMcKHEvfVmCkdG'
print('Getting mainnet balances...')
try:
    balances = buildBalances(mainnetGraphURL)
    print(f'Retrieved {len(balances)} total balances')
    print('Saving to CSV...')
    df = pd.DataFrame(balances)
    df.to_csv('MainnetBalances.csv', index=False)
    print('Saved to CSV')
except Exception as e:
    print(f"Error processing mainnet balances: {e}")
    import traceback
    traceback.print_exc()

optimismGraphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/GYBJ8wsQFkSwcgCqhaxnz5RU2VbgedAkWUk2qx9gTnzr'
print('Getting optimism balances...')
try:
    balances = buildBalances(optimismGraphURL)
    print(f'Retrieved {len(balances)} total balances')
    print('Saving to CSV...')
    df = pd.DataFrame(balances)
    df.to_csv('OptimismBalances.csv', index=False)
    print('Saved to CSV')
except Exception as e:
    print(f"Error processing optimism balances: {e}")
    import traceback
    traceback.print_exc()
"""

arbitrumGraphURL = 'https://gateway-arbitrum.network.thegraph.com/api/' + graphApiKey + '/subgraphs/id/Dgjyhh69XooHPd4JjvT3ik9FaGAR3w7sUSQyQ1YDakGp'
print('Getting arbitrum balances...')
try:
    balances = buildBalances(arbitrumGraphURL)
    print(f'Retrieved {len(balances)} total balances')
    print('Saving to CSV...')
    df = pd.DataFrame(balances)
    df.to_csv('ArbitrumBalances.csv', index=False)
    print('Saved to CSV')
except Exception as e:
    print(f"Error processing arbitrum balances: {e}")
    import traceback
    traceback.print_exc()