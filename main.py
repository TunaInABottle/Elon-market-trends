from FetcherClusterFactory import FetcherClusterFactory
from Market import Market, MarketType, Trend
from MessageData import MessageData
from setup_logger import fetch_log

fetch_log.info("New execution launched!")

with open('./config/AlphaVantageKey.txt') as f:
    alphavantage_key = f.read()

markets_of_interest = {
    "AlphaVantage": {
        "api_key": alphavantage_key,
        MarketType.STOCK: {
            "markets": ["IBM", "TSLA"]
        },
        MarketType.CRYPTO: { # full list of cryptos can be found here https://www.alphavantage.co/documentation/
            "markets": ["BTC", "DOGE"]
        }
    }
}


alphaCluster = FetcherClusterFactory.create("AlphaVantage", markets_of_interest)

markets =  alphaCluster.fetch_all()

print("printing market")
print(market)
print(market['STOCK IBM'])
print(market['STOCK IBM'].to_repr())
