# %%
import yfinance as yf
import pandas as pd
import sqlalchemy 
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# %%
load_dotenv("../.env")

MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")


#the f goes in front to embed variables
# Creates the engine, a reusable blueprint for connecting to MySQL.
# This does not open a connection itself, it just stores the driver,
# credentials, host, and database name.
engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")

engine.connect()

# os.getcwd()

# %%
tickers = yf.Tickers('EQIX DLR IRM')

# pulling a trailing 12 month window of daily OHLCV data for all three tickers at once
# since this runs automatically once a day, the window is going to shift forward every time it runs
# so the database is always going to hold the most recent 12 months, not a fixed start date
raw_data = yf.download("EQIX DLR IRM", period = '1y')

# raw_data.head()


# The table intially started in a multilayered column format. The following code adjusts it to row format to match the format of the MYSQL databases
raw_pivot = raw_data.stack([0,1])
raw_pivot = raw_pivot.unstack(1)
raw_pivot = raw_pivot.reset_index([0,1])
raw_pivot.columns.name = None

#renaming the columns to match the sql schema
raw_pivot = raw_pivot.rename(columns={
    "Close": "adjusted_close",
    "High": "high",
    "Low": "low",
    "Open": "open",
    "Volume": "volume",
    "Date": "date",
    "Ticker": "ticker"
})
raw_pivot["volume"] = raw_pivot["volume"].astype(int)

# grouping by ticker so that the shift doesn't pull the previous ticker's last close
# into the next ticker's first row
raw_pivot['previous_return'] = raw_pivot.groupby('ticker')['adjusted_close'].shift(1)
raw_pivot['daily_return'] = (raw_pivot['adjusted_close'] - raw_pivot['previous_return']) / raw_pivot['previous_return']
raw_pivot = raw_pivot.drop(columns=['previous_return'])


# This code deletest the data from daily prices and uploads the updated data to the table
# truncating first is necessary because this script runs automatically once a day
# without it, every run would just append a new trailing year on top of what is already there
# and the table would fill up with duplicates over time
with engine.begin() as conn:
    conn.execute(sqlalchemy.text("TRUNCATE TABLE daily_prices;"))
    raw_pivot.to_sql(name = 'daily_prices', con = conn, if_exists = 'append', index = False)

# %%
# The following code checks to see if the companies table has already been written to.
# If it has, the code will not write to the table again. If it has not, it will write to the table.
# scalar() pulls the single raw count value out of the query result instead of
# returning the full result object, since COUNT(*) always returns exactly one row and one column.
with engine.begin() as conn:
    checker = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM companies;")).scalar()

if checker == 3:
    print("Company data already exists in the database.")
else: 
    company_df = pd.DataFrame({ 
    "ticker": ['EQIX', 'IRM', 'DLR'],
    "company_name": ["Equinix", "Iron Mountain", 'Digital Reality Trust'],
    "sector": ["REIT", "REIT", "REIT"],
    "exchange": ["NYSE", "NYSE", "NYSE"]
    })
    company_df.to_sql(name = 'companies', con = engine, if_exists = 'append', index = False)




