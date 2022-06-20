import typing
import time
from FetcherClusterFactory import FetcherClusterFactory
import kafkaCustomProducer
from Market import MarketType, Trend
from MessageData import MessageData
from setup_logger import producer_log
from dotenv import load_dotenv
import os
load_dotenv(".env")

producer_log.info("New execution launched!")

init_sources = {
    "AlphaVantage": {
        "api_key": os.getenv('ALPHAVANTAGE_API_KEY'),
        # MarketType.STOCK: {
        #     "markets": ["IBM", "TSLA"]
        # },
        MarketType.CRYPTO: { # full list of cryptos can be found here https://www.alphavantage.co/documentation/
            "markets": ["BTC", "DOGE"]
        }
    },
    "Twitter": {
        "null": ""
    }
}



if __name__ == '__main__':

    alphaCluster = FetcherClusterFactory.create("AlphaVantage", init_sources)

    markets =  alphaCluster.fetch_all()

    market_of_interest = 'CRYPTO_BTC'

    focus_market = markets[market_of_interest]
    producer_log.debug(focus_market)
    producer_log.debug(focus_market.trend_list[0].to_repr())


    kafkaCustomProducer.write_unique(topic = market_of_interest, read_partition = 0, list_elem = focus_market.trend_list, list_elem_type = Trend )
