from FetcherClusterFactory import FetcherClusterFactory
from AlphavantageAPI import AlphavantageFetcherCluster
from Market import Market
from setup_logger import fetch_log

fetch_log.info("New execution launched!")

with open('./config/AlphaVantageKey.txt') as f:
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


alphaCluster = FetcherClusterFactory.create("AlphaVantage", markets_of_interest)

market =  alphaCluster.fetch_all()

movem = market['TIME_SERIES IBM']['Time Series (5min)']['2022-06-13 19:50:00']

print( movem )


print( market['TIME_SERIES IBM']['Time Series (5min)']['2022-06-13 19:50:00'] )

the_mar = Market.from_alphaVantage_repr(movem, '2022-06-13 19:50:00', 'STOCK IBM')

print( the_mar.to_repr() )