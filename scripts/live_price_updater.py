# pulling live data from yfinance and uploading it into a mysql database
import asyncio
import yfinance as yf
import sqlalchemy
# from dotenv import load_dotenv
# import os

# load_dotenv("../.env")

# mysql_host = os.environ.get("MYSQL_HOST")
# mysql_user = os.environ.get("MYSQL_USER")
# mysql_password = os.environ.get("MYSQL_PASSWORD")
# mysql_database = os.environ.get("MYSQL_DATABASE")

engine = None

# This function creates a connection to the MySQL database using the provided credentials. 
# It initializes the global `engine` variable for use in other functions. This is used to 
# prevent reduncancy in the code by having only update_stock_data.py hold the credientials
# for the MySQL database.
def sql_connection(host, user, password, database):
    global engine
    engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    with engine.connect() as conn:
        print("Connection successful")


# The following function servers as a message handler for the YFinance Websocket connection. It receives
# the message data passed from the start function as a dictionary, extracts the ticker and price information,
# and updates the corresponding record in the live_prices table of the MySQL database.
def live_price_handler(message):   
    ticker = message["id"]
    price = message["price"]
    with engine.begin() as conn:
        conn.execute(
            sqlalchemy.text("UPDATE live_prices SET current_price = :price WHERE ticker = :ticker"),
            {"price": price, "ticker": ticker} #this defines what the variables in the line above mean
        )
    print("Received message:", message)

# The following function is an asynchronous function that periodically pulls the high and low prices for
# the specified tickers from YFinance. It updates the corresponding records in the live_prices table of the 
# MySQL database every 10 minutes (600 seconds). This function runs concurrently with the WebSocket listener
# to ensure that both current prices and high/low prices are updated in real-time.
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


# The following function is the main entry point for the live price updater. It establishes a WebSocket connection 
# to YFinance, subscribes to the specified tickers, and concurrently runs both the WebSocket listener (which handles 
# incoming price updates) and the periodic pull function (which updates high and low prices). This ensures that the 
# live_prices table in the MySQL database is kept up-to-date with real-time price information.
async def start():
    async with yf.AsyncWebSocket() as ws:
        await ws.subscribe(["DLR", "EQIX", "IRM"])
        await asyncio.gather( # this function allows us to run both the websocket listener and the periodic pull at the same time
            ws.listen(live_price_handler),
            periodic_pull()
        )
    

