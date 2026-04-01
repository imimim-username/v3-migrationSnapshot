#sum up the balances per user per chain per alchemist
#also normalize all balances to be 18 decimals

import pandas as pd


def parse_int_columns(inputDf, columns):
    for col in columns:
        if col in inputDf.columns:
            inputDf[col] = inputDf[col].map(lambda x: int(str(x)))
    return inputDf


def stringify_int_columns(inputDf, columns):
    for col in columns:
        if col in inputDf.columns:
            inputDf[col] = inputDf[col].map(lambda x: str(int(x)))
    return inputDf

def alEthUnderlyingBalances(inputDf):
    # returns a dataframe of aleth DFs that includes the underlying balances

    parse_int_columns(inputDf, ["shares", "underlyingTokensPerShare"])
    inputDf["underlyingValue"] = (inputDf["shares"] * inputDf["underlyingTokensPerShare"]).map(lambda x: x // 10**18)

    """
    pivotDf = (
    inputDf
        .groupby("address", as_index=False)["underlyingValue"]
        .sum()
    )
    return pivotDf
    """

    return inputDf

def alEthFilterAndPivot(inputDf):
    # filters out low underlyingValue balances from aleth DFs and then creates a pivot table that sums underlying value by address

    lowValue = 100000000000000
    inputDf = inputDf[inputDf['underlyingValue'] >= lowValue]
    
    pivotDf = (
        inputDf
            .groupby("address", as_index=False)["underlyingValue"]
            .sum()
    )
    
    return pivotDf

def normalizeAlusdBalances(inputDf, chain): 
    # normalizes all balances to be 18 decimals 

    sixDecimals = { 
        'mainnet': ['yvUSDC', 'yvUSDT', 'aUSDC', 'aUSDT'], 
        'optimism': ['aUSDC', 'aUSDT', 'ysUSDC'], 
        'arbitrum': ['aUSDC'] 
    } 
    weirdo = 'vaUSDC' 

    parse_int_columns(inputDf, ["shares", "underlyingTokensPerShare"])

    six_list = sixDecimals.get(chain, []) 
    six_set = set(six_list)
    product = inputDf["shares"] * inputDf["underlyingTokensPerShare"]
    divisors = inputDf["yieldToken"].map(lambda token: 10**6 if token in six_set else 10**18)
    inputDf["underlyingValue"] = [p // d for p, d in zip(product, divisors)]

    mask_fix = inputDf["yieldToken"].isin(six_set | {weirdo})
    inputDf.loc[mask_fix, "underlyingValue"] = inputDf.loc[mask_fix, "underlyingValue"].map(lambda x: x * 10**12)

    return inputDf

def alUsdFilterAndPivot(inputDf):
    # filters out low underlyingValue balances from alUSD DFs and then creates a pivot table that sums underlying value by address

    lowValue = 10000000000000000
    inputDf = inputDf[inputDf['underlyingValue'] >= lowValue]
    
    pivotDf = (
        inputDf
        .groupby("address", as_index=False)["underlyingValue"]
        .sum()
    )
    
    return pivotDf

originFiles = {
    'mainnet': 'MainnetBalances-long_script.csv',
    'optimism': 'OptimismBalances-long_script.csv',
    'arbitrum': 'ArbitrumBalances-long_script.csv',
}

originDataFrames = {
    'mainnet': pd.read_csv(originFiles['mainnet'], dtype={'shares': 'string', 'underlyingTokensPerShare': 'string', 'yieldTokensPerShare': 'string'}),
    'optimism': pd.read_csv(originFiles['optimism'], dtype={'shares': 'string', 'underlyingTokensPerShare': 'string', 'yieldTokensPerShare': 'string'}),
    'arbitrum': pd.read_csv(originFiles['arbitrum'], dtype={'shares': 'string', 'underlyingTokensPerShare': 'string', 'yieldTokensPerShare': 'string'}),
}



for chain, df in originDataFrames.items():
    '''
    print(f"Processing {chain} data...")
    print(df.head())
    print(df.columns)
    print(df.shape)
    print(df.info())
    print(df.describe())
    print(df.head())
    print(df.columns)
    print(df.shape)
    print(df.info())
    print(df.describe())
    '''
    alethDf = df[df['alchemist'] == 'alETH'].copy()
    alusdDf = df[df['alchemist'] == 'alUSD'].copy()

    alethDf = alEthUnderlyingBalances(alethDf)
    alethPivotDf = alEthFilterAndPivot(alethDf)
    print(alethPivotDf.head())

    fileName = 'alEthValues-pivot-' + chain + '.csv'
    print(f"Saving {fileName}...")
    stringify_int_columns(alethPivotDf, ["underlyingValue"])
    alethPivotDf.to_csv(fileName, index=False)
    print(f"Saved {fileName}")

    alusdDf = normalizeAlusdBalances(alusdDf, chain)
    alusdPivotDf = alUsdFilterAndPivot(alusdDf)
    print(alusdPivotDf.head())

    fileName = 'alUsdValues-pivot-' + chain + '.csv'
    print(f"Saving {fileName}...")
    stringify_int_columns(alusdPivotDf, ["underlyingValue"])
    alusdPivotDf.to_csv(fileName, index=False)
    print(f"Saved {fileName}")
    
