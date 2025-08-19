# StockData Library

A Python library for fetching, storing, and using stock price data with automatic local caching by symbol and interval.

## Features
- Uses Yahoo Finance
- Saves data locally under `csv/<symbol>/<interval>.csv`
- Only fetches from the internet if local data is incomplete
- Verbose console logging to indicate whether data is local or remote

## Installation

```bash
pip install -e .
