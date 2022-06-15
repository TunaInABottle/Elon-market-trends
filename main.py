from FetcherClusterFactory import FetcherClusterFactory
from AlphavantageAPI import AlphavantageFetcherCluster
from Market import MarketType, Trend
from setup_logger import fetch_log
import json

fetch_log.info("New execution launched!")

with open('./config/AlphaVantageKey.txt') as f:
    alphavantage_key = f.read()

markets_of_interest = {
    "AlphaVantage": {
        "api_key": alphavantage_key,
        MarketType.STOCK: {
            "url_name": "TIME_SERIES",
            "markets": ["IBM"]
        },
        MarketType.CRYPTO: { # full list of cryptos can be found here https://www.alphavantage.co/documentation/
            "url_name": "CRYPTO",
            "markets": ["BTC", "DOGE"]
        }
    }
}


alphaCluster = FetcherClusterFactory.create("AlphaVantage", markets_of_interest)

market =  alphaCluster.fetch_all()

print("printing market")
print(market)