from FetcherClusterFactory import FetcherClusterFactory
import kafkaCustomProducer
from Market import MarketType, Trend
from config.setup_logger import producer_log
from dotenv import load_dotenv
import os
load_dotenv(".env")

producer_log.info("New execution launched!")

init_sources = {
    "AlphaVantage": {
        "api_key": os.getenv('ALPHAVANTAGE_API_KEY'),
        MarketType.STOCK: {
            "markets": ["IBM", "TSLA"]
        },
        MarketType.CRYPTO: { # full list of cryptos can be found here https://www.alphavantage.co/documentation/
            "markets": ["BTC", "DOGE", "ETH", "ETC"]
        }
    },
    "Twitter": {
        "null": ""
    }
}



if __name__ == '__main__':

    print("horray")

    alphaCluster = FetcherClusterFactory.create("AlphaVantage", init_sources)

    markets =  alphaCluster.fetch_all()


    for market_name, market_obj in markets.items():
        producer_log.debug(f"First trend in the market \"{market_name}\": {market_obj.trend_list[0].to_repr()}")

        kafkaCustomProducer.write_unique(topic = market_name, read_partition = 0, list_elem = market_obj.trend_list, list_elem_type = Trend )
