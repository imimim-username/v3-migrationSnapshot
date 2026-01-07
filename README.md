# V3 Snap - User Balance Snapshot Tool

This repository contains scripts for taking snapshots of user balances across multiple blockchain networks (Mainnet, Optimism, and Arbitrum). There are two different methods implemented for retrieving balance data.

## Overview

The project provides two main approaches for snapshotting user balances:

1. **app.py** - Uses The Graph API to query subgraph data for balance information
2. **duneApp.py** - Uses Dune Analytics queries combined with RPC calls to fetch balance data

Both scripts generate CSV files with balance snapshots for Mainnet, Optimism, and Arbitrum networks.

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

## Scripts

- **app.py** - Main script using The Graph API method
- **duneApp.py** - Main script using Dune Analytics + RPC method
- **rpcCall.py** - Utility module for making RPC calls to blockchain networks
- **runDuneQuery.py** - Utility module for interacting with Dune Analytics API

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
