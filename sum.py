#sum up the balances per user per chain per alchemist
#also normalize all balances to be 18 decimals

import pandas as pd
import numpy as np

def alEthUnderlyingBalances(inputDf):
    # returns a dataframe of aleth DFs that includes the underlying balances

    inputDf["shares"] = inputDf["shares"].map(int)
    inputDf["underlyingTokensPerShare"] = inputDf["underlyingTokensPerShare"].map(int)

    
    inputDf['underlyingValue'] = inputDf['shares'] * inputDf['underlyingTokensPerShare'] // 1e18

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

    inputDf["shares"] = inputDf["shares"].map(int) 
    inputDf["underlyingTokensPerShare"] = inputDf["underlyingTokensPerShare"].map(int) 

    six_list = sixDecimals.get(chain, []) 
    mask_6 = inputDf["yieldToken"].isin(six_list) 
    product = inputDf["shares"] * inputDf["underlyingTokensPerShare"] 
    divisor = np.where(mask_6, 10**6, 10**18) 
    inputDf["underlyingValue"] = product // divisor 

    mask_fix = mask_6 | (inputDf["yieldToken"] == weirdo)
    inputDf.loc[mask_fix, "underlyingValue"] = inputDf.loc[mask_fix, "underlyingValue"] * 10**12

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
    'mainnet': pd.read_csv(originFiles['mainnet']),
    'optimism': pd.read_csv(originFiles['optimism']),
    'arbitrum': pd.read_csv(originFiles['arbitrum']),
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

    fileName = 'alEthValues-' + chain + '.csv'
    print(f"Saving {fileName}...")
    alethPivotDf.to_csv(fileName, index=False)
    print(f"Saved {fileName}")

    alusdDf = normalizeAlusdBalances(alusdDf, chain)
    alusdPivotDf = alUsdFilterAndPivot(alusdDf)
    print(alusdPivotDf.head())

    
