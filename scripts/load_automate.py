from itertools import count
import yfinance as yf
import pandas as pd
import asyncio
import sqlalchemy 
from scripts.live_price_updater import start




def start_live_data():
    try:
        asyncio.run(start())
    except Exception as e:
        print(f"Error in start_live_data function: {e}", flush=True)
        return None
