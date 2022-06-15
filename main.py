from FetcherClusterFactory import FetcherClusterFactory
from Market import MarketType
from setup_logger import fetch_log

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
            "markets": ["BTC", "DOGE", "PUSA"]
        }
    }
}


alphaCluster = FetcherClusterFactory.create("AlphaVantage", markets_of_interest)

market =  alphaCluster.fetch_all()

print("printing market")
print(market)
print(market['STOCK IBM'])