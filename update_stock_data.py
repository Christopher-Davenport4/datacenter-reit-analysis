from dotenv import load_dotenv
load_dotenv()
import os
# from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load_to_sql, start_live_data


MYSQL_HOST = os.environ.get("MYSQL_HOST", 'localhost')
MYSQL_USER = os.environ.get("MYSQL_USER", 'root')
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", 'vivian123')
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", 'datacenter_reits')


def main():
   
    if MYSQL_HOST is None or MYSQL_USER is None or MYSQL_PASSWORD is None or MYSQL_DATABASE is None:
        raise ValueError("One or more MySQL environment variables are not set. Please check your .env file.")
    print(f"MySQL environment variables loaded successfully. Host: {MYSQL_HOST}, User: {MYSQL_USER}", flush=True)
    symbols = "EQIX, DLR, IRM"
    period = '1y'
    columns = {
            "Close": "adjusted_close",
            "High": "high",
            "Low": "low",
            "Open": "open",
            "Volume": "volume",
            "Date": "date",
            "Ticker": "ticker"
        }
    
    count = len(symbols)

    print("Starting the data ingestion process...", flush=True)
    # extracted_data = extract(symbols = symbols, period = period)
    print("Extraction complete. Transforming data...", flush=True)
    # transformed_data = transform(extracted_data, columns)
    print("Transformation complete. Loading data to SQL...", flush=True )
    # load_to_sql(transformed_data, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, count)
    print("Data loaded to SQL.")

    
    

if __name__ == "__main__":
    print("Starting the main function...", flush=True)
    main()