from shutil import which
import time
from FetcherClusterFactory import FetcherClusterFactory
from Market import Market, MarketType, Trend
from MessageData import MessageData
from setup_logger import producer_log
from dotenv import load_dotenv
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json
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
            "markets": ["BTC", "DOGE"]
        }
    },
    "Twitter": {
        "null": ""
    }
}

########


def get_last_message(k_consumer: KafkaConsumer, which_topic: TopicPartition, last_offset: int) -> str:
    # obtain last message
    k_consumer.seek( which_topic, last_offset - 1 ) 

    last_mex = None
    for message in k_consumer:
        last_mex = dict(json.loads(message.value)) #Trend.from_repr(dict(json.loads(message.value)))

        if message.offset == last_offset - 1:
            #exit the loop after obtaining the message
            break
    k_consumer.close()

    producer_log.debug(f"last message in topic: {last_mex}")

    return last_mex

########

if __name__ == '__main__':

    alphaCluster = FetcherClusterFactory.create("AlphaVantage", init_sources)

    markets =  alphaCluster.fetch_all()

    print("printing market")
    print(markets)

    focus_market = markets['STOCK_TSLA'] #TODO API return from the latest to the oldest trend
    producer_log.debug(focus_market)


    ########

    producer_log.debug("Initialising Kafka producer")
    k_producer = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        value_serializer = lambda x: json.dumps(x, indent=2).encode('utf-8')
    )

    #####

    #@TODO function to get last message in queue


    which_topic = TopicPartition(topic = 'TSLA_STOCK', partition = 0)


    producer_log.debug("Initialising Kafka consumer")
    k_consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id = "amazingo"
    )
    k_consumer.assign([which_topic])


    last_offset = k_consumer.position(which_topic)
    
    print(last_offset)
    if last_offset > 1:
        last_mex = get_last_message(which_topic, k_consumer, last_offset)
        
        #TODO go back on the API fetch until the trend equals the one in the last message
        producer_log.debug(f"Last message in queue {last_mex}")
    else:
        k_consumer.close()
        producer_log.info("No offset present, proceeding writing regularly")
        for trend in reversed(focus_market.trend_list):
            producer_log.debug(f"{trend}, position {k_consumer.position(which_topic)}")
            k_producer.send('TSLA_STOCK', trend.to_repr())
            time.sleep(3)