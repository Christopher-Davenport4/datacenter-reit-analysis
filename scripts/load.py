import yfinance as yf
import pandas as pd
import asyncio
import sqlalchemy 
from scripts.live_price_updater import start


def load_to_sql(data, host, user, password, database, count):
    try:
        engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("TRUNCATE TABLE daily_prices;"))


            data.to_sql(name = 'daily_prices', con = conn, if_exists = 'append', index = False)


            checker = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM companies;")).scalar()

        if checker == count:
            print("Company data already exists in the database.", flush=True)
        else: 
            company_df = pd.DataFrame({ 
            "ticker": ['EQIX', 'IRM', 'DLR', 'APPL'],
            "company_name": ["Equinix", "Iron Mountain", 'Digital Reality Trust', 'Apple Inc.'],
            "sector": ["REIT", "REIT", "REIT", "Technology"],
            "exchange": ["NYSE", "NYSE", "NYSE"]
            })
            company_df.to_sql(name = 'companies', con = engine, if_exists = 'append', index = False)
    except Exception as e:
        print(f"Error in load function: {e}", flush=True)
        return None

def start_live_data():
    try:
        asyncio.run(start())
    except Exception as e:
        print(f"Error in start_live_data function: {e}", flush=True)
        return None
