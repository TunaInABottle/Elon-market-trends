from shutil import which
import time
from FetcherClusterFactory import FetcherClusterFactory
from Market import Market, MarketType, Trend
from MessageData import MessageData
from setup_logger import fetch_log
from dotenv import load_dotenv
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json
import os
load_dotenv(".env")

fetch_log.info("New execution launched!")

init_sources = {
    "AlphaVantage": {
        "api_key": os.getenv('ALPHAVANTAGE_API_KEY'),
        MarketType.STOCK: {
            "markets": ["IBM", "TSLA"]
        },
        MarketType.CRYPTO: { # full list of cryptos can be found here https://www.alphavantage.co/documentation/
            "markets": ["BTC", "DOGE"]
        }
    },
    "Twitter": {
        "null": ""
    }
}

########


if __name__ == '__main__':

    alphaCluster = FetcherClusterFactory.create("AlphaVantage", init_sources)

    markets =  alphaCluster.fetch_all()

    print("printing market")
    print(markets)

    focus_market = markets['STOCK_TSLA'] #TODO API return from the latest to the oldest trend
    fetch_log.debug(focus_market)


    ########

    fetch_log.debug("Initialising Kafka producer")
    k_producer = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        value_serializer = lambda x: json.dumps(x, indent=2).encode('utf-8')
    )

    #####

    #@TODO function to get last message in queue


    which_topic = TopicPartition(topic = 'TSLA_STOCK', partition = 0)


    fetch_log.debug("Initialising Kafka consumer")
    k_consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id = "amazingo"
    )
    k_consumer.assign([which_topic])


    last_offset = k_consumer.position(which_topic)
    
    print(last_offset)
    if last_offset > 1:
        k_consumer.seek( which_topic, last_offset - 1 ) # obtain last message

        last_mex = None

        for message in k_consumer:
            print( dict(json.loads(message.value)) )
            last_mex = Trend.from_repr(dict(json.loads(message.value)))


            if message.offset == last_offset - 1:
                break
        k_consumer.close()
        
        #TODO go back on the API fetch until the trend equals the one in the last message
        fetch_log.debug(f"Last message in queue {last_mex}")
    else:
        k_consumer.close()
        fetch_log.info("No offset present, proceeding writing regularly")
        for trend in reversed(focus_market.trend_list):
            fetch_log.debug(f"{trend}, position {k_consumer.position(which_topic)}")
            k_producer.send('TSLA_STOCK', trend.to_repr())
            time.sleep(3)