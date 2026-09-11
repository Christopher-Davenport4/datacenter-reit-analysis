import asyncio
from scripts.live_price_updater import sql_connection, start

#The following function is a wrapper around the start function from live_price_updater.py.
#  It first establishes a connection to the MySQL database using the provided credentials,
#  and then runs the start function to initiate the live price updater. This function is
#  designed to be called from update_stock_data.py, allowing for a seamless integration of 
#  the live price updater into the overall ETL pipeline.
def start_live_data(host, user, password, database):
    try:
        sql_connection(host, user, password, database)
        asyncio.run(start())
     
    except Exception as e:
        print(f"Error in start_live_data function: {e}", flush=True)
        return None