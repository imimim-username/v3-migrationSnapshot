# V3 Snap - User Balance Snapshot Tool

This repository contains scripts for taking snapshots of user balances across multiple blockchain networks (Mainnet, Optimism, and Arbitrum). There are two different methods implemented for retrieving balance data.

## Overview

The project provides two main approaches for snapshotting user balances:

1. **app.py** - Uses The Graph API to query subgraph data for balance information
2. **duneApp.py** - Uses Dune Analytics queries combined with RPC calls to fetch balance data

Both scripts generate CSV files with balance snapshots for Mainnet, Optimism, and Arbitrum networks.

**End-to-end pipeline:** **allScripts.py** runs the full Dune-based pipeline by executing three component scripts in sequence: `duneApp.py` → `sum.py` → `getDebts.py`. Each script consumes the outputs of the previous one (see [Pipeline (allScripts.py)](#pipeline-allscriptspy) and [Scripts](#scripts) below).

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

You'll need to set up environment variables. Create a `.env` file in the project root with the following variables:

- `GRAPH_API_KEY` - Your The Graph API key (required for `app.py`)
- `ALCHEMY_API_KEY` - Your Alchemy API key (required for both scripts)

For `duneApp.py`, you'll also need a `dune.env` file with:
- Dune API credentials (configured for the `dune-client` library)

## Usage

### Method 1: Using The Graph API (app.py)

This script queries The Graph subgraphs to retrieve balance data:

```bash
python app.py
```

This will generate:
- `MainnetBalances.csv`
- `OptimismBalances.csv`
- `ArbitrumBalances.csv`

### Method 2: Using Dune Analytics + RPC Calls (duneApp.py)

This script uses Dune Analytics queries to get depositor addresses, then makes RPC calls to fetch balances:

```bash
python duneApp.py
```
When this is ready for prod, please see the comments throughout to comment and uncomment the relevant lines so as to execute the Dune queries to get the most recent results.

This will generate:
- `MainnetBalances-long_script.csv`
- `OptimismBalances-long_script.csv`
- `ArbitrumBalances-long_script.csv`

### Pipeline (allScripts.py)

To run the full Dune-based pipeline in one go (balances → aggregation → debt lookup), use:

```bash
python allScripts.py
```

This runs the following scripts **in sequence** (each step uses the previous step’s outputs):

1. **duneApp.py** – Fetches balances via Dune + RPC; writes `MainnetBalances-long_script.csv`, `OptimismBalances-long_script.csv`, `ArbitrumBalances-long_script.csv`.
2. **sum.py** – Reads those CSVs, normalizes and aggregates by address/alchemist; writes `alEthValues-pivot-{mainnet,optimism,arbitrum}.csv` and `alUsdValues-pivot-{mainnet,optimism,arbitrum}.csv`.
3. **getDebts.py** – Reads the pivot CSVs, fetches debt per address via RPC, and writes `alEthValues-sum-and-debt-{mainnet,optimism,arbitrum}.csv` and `alUsdValues-sum-and-debt-{mainnet,optimism,arbitrum}.csv`.

## Scripts

- **allScripts.py** – Runs the full pipeline by executing `duneApp.py` → `sum.py` → `getDebts.py` in order. Use this for a single command that produces the final sum-and-debt CSVs.
- **app.py** – Standalone script using The Graph API (writes `MainnetBalances.csv`, etc.; not part of the allScripts pipeline).
- **duneApp.py** – Fetches depositor addresses from Dune, then RPC balance data per vault; writes the `*-long_script.csv` balance files for Mainnet, Optimism, and Arbitrum.
- **sum.py** – Reads the `*-long_script.csv` files, computes underlying balances (alETH/alUSD), filters by minimum value, and outputs pivot CSVs (`alEthValues-pivot-*.csv`, `alUsdValues-pivot-*.csv`) per chain.
- **getDebts.py** – Reads the pivot CSVs, fetches each address’s debt from the alchemist contracts via RPC, and saves the result as `*-sum-and-debt-*.csv` (same names with `sum-and-debt` instead of `pivot`).
- **rpcCall.py** – Utility module for making RPC calls to blockchain networks.
- **runDuneQuery.py** – Utility module for interacting with the Dune Analytics API.

## Output

Both scripts generate CSV files containing:
- User addresses
- Balance information (shares, underlying values)
- Yield token details
- Network-specific data

## Notes

- The scripts include rate limiting delays to prevent API throttling
- Error handling is implemented for network requests and data processing
- The Dune method requires pre-configured Dune queries with specific query IDs
