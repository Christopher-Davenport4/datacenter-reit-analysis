from itertools import count

import yfinance as yf
import pandas as pd
import asyncio
import sqlalchemy 
from scripts.live_price_updater import start


def load_to_sql(data, host, user, password, database, count):
    try:
        engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

        with engine.connect() as conn:
            company_df = pd.DataFrame({
                "ticker": ['EQIX', 'IRM', 'DLR', 'AAPL'],
                "company_name": ["Equinix", "Iron Mountain", 'Digital Reality Trust', 'Apple Inc.'],
                "sector": ["REIT", "REIT", "REIT", "Technology"],
                "exchange": ["NYSE", "NYSE", "NYSE", "NASDAQ"]
            })

            upsert_stmt = sqlalchemy.text("""
                INSERT INTO companies (ticker, company_name, sector, exchange)
                VALUES (:ticker, :company_name, :sector, :exchange)
                ON DUPLICATE KEY UPDATE
                    company_name = VALUES(company_name),
                    sector = VALUES(sector),
                    exchange = VALUES(exchange)
            """)
            conn.execute(upsert_stmt, company_df.to_dict(orient='records'))

            conn.execute(sqlalchemy.text("TRUNCATE TABLE daily_prices;"))
            data.to_sql(name='daily_prices', con=conn, if_exists='append', index=False)

            conn.commit()
    except Exception as e:
        print(f"Error in load function: {e}", flush=True)
        return None

def start_live_data():
    try:
        asyncio.run(start())
    except Exception as e:
        print(f"Error in start_live_data function: {e}", flush=True)
        return None
