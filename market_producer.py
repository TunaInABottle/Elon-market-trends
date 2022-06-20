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

########


def get_last_message(k_consumer: KafkaConsumer, which_topic: TopicPartition, last_offset: int) -> str:
    """
    TODO 

    Args:

    Returns:
    """
    # obtain last message
    k_consumer.seek( which_topic, last_offset - 1 ) 

    last_mex = None
    for message in k_consumer:
        last_mex = dict(json.loads(message.value)) #Trend.from_repr(dict(json.loads(message.value)))

        if message.offset == last_offset - 1:
            #exit the loop after obtaining the message
            break

    producer_log.debug(f"last message in topic: {last_mex}")

    return last_mex

########

if __name__ == '__main__':

    alphaCluster = FetcherClusterFactory.create("AlphaVantage", init_sources)

    markets =  alphaCluster.fetch_all()

    market_of_interest = 'CRYPTO_BTC'

    focus_market = markets[market_of_interest] #TODO API return from the latest to the oldest trend
    producer_log.debug(focus_market)
    producer_log.debug(focus_market.trend_list[0].to_repr())


    ########

    producer_log.debug("Initialising Kafka producer")
    k_producer = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        value_serializer = lambda x: json.dumps(x, indent=2).encode('utf-8')
    )

    #####

    #@TODO function to get last message in queue


    which_topic = TopicPartition(topic = market_of_interest, partition = 0)


    producer_log.debug("Initialising Kafka consumer")
    k_consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        #group_id = "amazo"
    )
    k_consumer.assign([which_topic])


    last_offset = k_consumer.position(which_topic)
    
    print(last_offset)
    if last_offset > 1:
        last_mex = get_last_message(k_consumer, which_topic, last_offset)
        k_consumer.close()
        

        #TODO go back on the API fetch until the trend equals the one in the last message

        last_trend = Trend.from_repr(last_mex)
        found_idx = False
        market_trends = focus_market.trend_list

        for idx, trend in enumerate(market_trends):
            if trend == last_trend:
                producer_log.info(f"last message found in API call at index {idx}: {trend.to_repr()}")
                found_idx = idx
                break

        if found_idx:
            producer_log.info(f"writing the rest of missing messages")
            producer_log.debug(f"{len(market_trends[-found_idx:])} - {market_trends[found_idx].to_repr()}")

            missing_trends = market_trends[-found_idx:]
        else:
            producer_log.info(f"No fetched message equals the last in the queue, writing all the elements")
            missing_trends = market_trends

        for trend in reversed(missing_trends): #as it usually start from the latest to the oldest
            producer_log.debug(f"{trend.to_repr()}")
            k_producer.send(market_of_interest, trend.to_repr())






    else: # no message in queue
        k_consumer.close()
        producer_log.info("No offset present, proceeding writing all the data")
        for trend in reversed(focus_market.trend_list):
            producer_log.debug(f"{trend}, position {k_consumer.position(which_topic)}")
            k_producer.send(market_of_interest, trend.to_repr())
            time.sleep(3)