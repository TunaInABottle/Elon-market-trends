from FetcherClusterFactory import FetcherClusterFactory
from setup_logger import fetch_log

fetch_log.info("New execution launched!")

with open('stockkey.txt') as f:
    alphavantage_key = f.read()

markets_of_interest = {
    "AlphaVantage": {
        "api_key": alphavantage_key,
        "Stock": {
            "url_name": "TIME_SERIES",
            "markets": ["IBM"]
        },
        "Crypto": {
            "url_name": "CRYPTO",
            "markets": ["BTC", "DOGE"]
        }
    }
}




FetcherClusterFactory.create("AlphaVantage", markets_of_interest)