from dotenv import load_dotenv
load_dotenv()

import argparse
import os
from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load_to_sql
from scripts.load_automate import start_live_data


MYSQL_HOST = os.environ.get("MYSQL_HOST", 'localhost')
MYSQL_USER = os.environ.get("MYSQL_USER", 'root')
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", 'vivian123')
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", 'datacenter_reits')

SYMBOLS = "EQIX, DLR, IRM"
PERIOD = '1y'
COLUMN_MAP = {
    "Close": "adjusted_close",
    "High": "high",
    "Low": "low",
    "Open": "open",
    "Volume": "volume",
    "Date": "date",
    "Ticker": "ticker"
}


def parse_args():
    parser = argparse.ArgumentParser(description="Run the daily stock data ETL pipeline.")
    parser.add_argument(
        '--live',
        action='store_true',
        help='Also start the live price updater after the batch ETL finishes.'
    )
    return parser.parse_args()


def main(run_live):
    if MYSQL_HOST is None or MYSQL_USER is None or MYSQL_PASSWORD is None or MYSQL_DATABASE is None:
        raise ValueError("One or more MySQL environment variables are not set. Please check your .env file.")
    print(f"MySQL environment variables loaded successfully. Host: {MYSQL_HOST}, User: {MYSQL_USER}", flush=True)

    count = len(SYMBOLS.split(','))

    print("Starting the data ingestion process...", flush=True)
    extracted_data = extract(symbols=SYMBOLS, period=PERIOD)

    print("Extraction complete. Transforming data...", flush=True)
    transformed_data = transform(extracted_data, COLUMN_MAP)

    print("Transformation complete. Loading data to SQL...", flush=True)
    load_to_sql(transformed_data, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, count)
    print("Data loaded to SQL.", flush=True)

    if run_live:
        print("Starting live price updater...", flush=True)
        start_live_data()


if __name__ == "__main__":
    args = parse_args()
    print("Starting the main function...", flush=True)
    main(run_live=args.live)