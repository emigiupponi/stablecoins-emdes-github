# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: m1web3
#     language: python
#     name: python3
# ---

# %% [markdown]
# Import necessary libraries and set up the CoinMetrics API client using the API key from environment variables.

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from coinmetrics.api_client import CoinMetricsClient
from datetime import datetime, timedelta
import os

CM_KEY = os.getenv('CM_KEY', 'INSERT YOUR KEY HERE')
client = CoinMetricsClient(CM_KEY)

# %% [markdown]
# Fetch catalog data for spot and futures markets, and display the first few rows of the market catalog.

# %%
spot_catalog_df = client.catalog_exchange_asset_metrics_v2(metrics='volume_reported_spot_usd_1d').to_dataframe()
futures_catalog_df = client.catalog_exchange_asset_metrics_v2(metrics=['open_interest_reported_future_usd']).to_dataframe()
market_catalog_df = client.catalog_market_candles_v2().to_dataframe()
market_catalog_df.head()

# %% [markdown]
# Define fiat currency denominations to filter spot markets and exchange assets. Then, filter the catalog data accordingly.

# %%
# Define a list of fiat currency denominations to filter SPOT MARKETS
fiat_denom_strings_spot = [
    '-aud-', '-usd-', '-jpy-', '-gbp-', '-eur-', 
    '-cad-', '-ars-', '-brl-', '-ngn-', '-pln-', 
    '-ron-', '-rub-', '-zar-', '-try-', '-uah-', '-inr-'
]
spot_market_cg = market_catalog_df[market_catalog_df['market'].str.contains('|'.join(fiat_denom_strings_spot))]
market_spot_list = spot_market_cg.market.to_list()

# Define a list of fiat currency denominations to filter EXCHANGE ASSETS
fiat_denom_strings_assets = [
    '-aud$', '-usd$', '-jpy$', '-gbp$', '-eur$', 
    '-cad$', '-ars$', '-brl$', '-ngn$', '-pln$', 
    '-ron$', '-rub$', '-zar$', '-try$', '-uah$', '-inr$'
]
ea_spot_cg = spot_catalog_df[spot_catalog_df['exchange_asset'].str.contains('|'.join(fiat_denom_strings_assets))]
ea_asset_spot_list = ea_spot_cg.exchange_asset.to_list()
ea_futs_cg = futures_catalog_df[futures_catalog_df['exchange_asset'].str.contains('|'.join(fiat_denom_strings_assets))]
ea_asset_futs_list = ea_futs_cg.exchange_asset.to_list()

# %% [markdown]
# Fetch and process exchange asset metrics for futures, handling any errors during data fetching.

# %%
ea_futs_df = client.get_exchange_asset_metrics(
    exchange_assets=ea_asset_futs_list,
    metrics=['open_interest_reported_future_usd'],
    frequency='1d',
    start_time='2019-01-01',
    end_time='2024-04-19'
).parallel().to_dataframe()

error_assets = []
ea_spot_df_list = []
for asset in ea_asset_spot_list:
    try:
        data = client.get_exchange_asset_metrics(
            exchange_assets=asset,
            metrics='volume_reported_spot_usd_1d',
            frequency='1d',
            start_time='2019-01-01',
            end_time='2024-04-19'
        ).to_dataframe()
        ea_spot_df_list.append(data)
    except Exception as e:
        print(f"Error fetching data for asset: {asset}, Error: {e}")
        error_assets.append(asset)
ea_spot_df = pd.concat(ea_spot_df_list)

# %% [markdown]
# Generate pivot tables for spot and futures data, and save them as CSV files.

# %%
ea_spot_df.pivot_table(values="volume_reported_spot_usd_1d", index="time", columns="exchange_asset").to_csv("exchange_asset_spot_volume_usd_1d.csv")
ea_futs_df.pivot_table(values="open_interest_reported_future_usd", index="time", columns="exchange_asset").to_csv("exchange_asset_futures_open_interest_usd_1d.csv")

# %% [markdown]
# Fetch market candles data for spot markets, save the raw data, and generate a pivot table for market candles volume.

# %%
market_candles = client.get_market_candles(
    markets=market_spot_list,
    frequency='1d',
    start_time='2019-01-01',
    end_time='2024-04-19',
    page_size=10_000
).parallel().to_dataframe()
market_candles.to_csv("raw_market_candles_1d.csv")
market_candles.pivot_table(values="candle_usd_volume", index="time", columns="market").to_csv("market_candles_1d_volume_usd.csv")

# %% [markdown]
# Documentation and methodology for data processing and analysis are included as comments and markdown cells throughout the notebook.
