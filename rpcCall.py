def rpcCall (targetAddress, dataString, blockNumber, chain):

    import requests
    import json
    from dotenv import load_dotenv
    import os

    
    alchemy_key = os.getenv("ALCHEMY_API_KEY")

    match chain:
        case 'eth':
            apiString = 'https://eth-mainnet.g.alchemy.com/v2/' + alchemy_key
        case 'op':
            apiString = 'https://opt-mainnet.g.alchemy.com/v2/' + alchemy_key
        case 'arb':
            apiString = 'https://arb-mainnet.g.alchemy.com/v2/' + alchemy_key
        case 'lin':
            apiString = 'https://linea-mainnet.g.alchemy.com/v2/' + alchemy_key

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": targetAddress,
                "data": dataString
            },
            blockNumber
        ]
    }

    rpcData = requests.post(apiString, headers=headers, data=json.dumps(payload)).json()

    return rpcData['result']

