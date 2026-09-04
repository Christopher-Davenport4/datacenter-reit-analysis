#pulling live data from yfinance
import asyncio
import yfinance as yf
import sqlalchemy
from dotenv import load_dotenv
import os

load_dotenv("../.env")

mysql_host = os.environ.get("MYSQL_HOST")
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
mysql_database = os.environ.get("MYSQL_DATABASE")


#the f goes in front to embed variables
engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}")

with engine.connect() as conn:
    print("Connection successful")

# define your message callback
def message_handler(message):   
    ticker = message["id"]
    price = message["price"]
    with engine.begin() as conn:
        conn.execute(
            sqlalchemy.text("UPDATE live_prices SET current_price = :price WHERE ticker = :ticker"),
            {"price": price, "ticker": ticker} #this defines what the variables in the line above mean
        )
    print("Received message:", message)

async def periodic_pull():
    while True:
     for ticker in ["EQIX", "DLR", "IRM"]:
            data = yf.download(ticker, period="1d")
            high = data["High", ticker].iloc[0]
            low = data["Low", ticker].iloc[0]
            with engine.begin() as conn:
             conn.execute(
              sqlalchemy.text("UPDATE live_prices SET current_high = :high, current_low = :low WHERE ticker = :ticker"),
                 {"high": high, "low": low, "ticker": ticker}
         )
     await asyncio.sleep(600) # sleep for 10 minutes (600 seconds) since the high and low only update periodically, we don't need to pull them as often as the current price


async def start():
    # =======================
    # With Context Manager
    # =======================
    async with yf.AsyncWebSocket() as ws:
        await ws.subscribe(["DLR", "EQIX", "IRM"])
        await asyncio.gather( # this function allows us to run both the websocket listener and the periodic pull at the same time
            ws.listen(message_handler),
            periodic_pull()
        )
    
    # # =======================
    # # Without Context Manager
    # # =======================
    # ws = yf.AsyncWebSocket()
    # await ws.subscribe(["DLR", "EQIX", "IRM"])
    # await ws.listen()

