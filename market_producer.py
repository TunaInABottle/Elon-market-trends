import typing
import time
from FetcherClusterFactory import FetcherClusterFactory
from Market import MarketType, Trend
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

def last_message_topic(which_topic: TopicPartition) -> typing.Tuple[str, int]:
    """
    TODO
    """
    producer_log.debug("Initialising Kafka consumer")
    consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest'#,
        #group_id = "piro"
    )
    consumer.assign([which_topic])

    last_offset = consumer.position(which_topic)
    last_mex = None

    if last_offset > 1:
        last_mex = get_last_message(consumer, which_topic, last_offset)
    
    consumer.close()
    return last_mex, last_offset

def write_list_in_queue(topic: str, obj_list: list) -> None:
    """
    TODO

    Args:
        obj_list: a list sorted from the most recent element to the oldest.
    """
    producer_log.debug("Initialising Kafka producer")
    producer = KafkaProducer(
        bootstrap_servers = ['localhost:9092'],
        value_serializer = lambda x: json.dumps(x, indent=2).encode('utf-8')
    )

    for element in reversed(obj_list):
        producer_log.debug(f"sending in \"{topic}\" message: {element.to_repr()}")
        producer.send(topic, element.to_repr())

    producer_log.info(f"Flushing and closing producer")
    producer.flush()
    producer.close()

def filter_duplicates(message: str, objType: MessageData, from_list: list, skip_latest: bool = True ) -> list:
    """
    TODO
    """
    last_queued_message = objType.from_repr(message)
    found_idx = None
    from_idx = None

    if skip_latest:
        from_idx = 1
    else:
        from_idx = 0


    for idx, elem in enumerate(from_list):
        if elem == last_queued_message:
            producer_log.info(f"last message found in API call at index {idx}: {elem.to_repr()}")
            found_idx = idx
            break

    if found_idx is not None:
        producer_log.info(f"writing the rest of missing messages")
        missing_elem = from_list[from_idx:found_idx] # skip most recent as it is still updating
    else:
        producer_log.info(f"No fetched message equals the last in the queue, writing all the elements")
        missing_elem = from_list[from_idx:] # skip most recent as it is still updating

    return missing_elem

########



if __name__ == '__main__':

    alphaCluster = FetcherClusterFactory.create("AlphaVantage", init_sources)

    markets =  alphaCluster.fetch_all()

    market_of_interest = 'CRYPTO_BTC'

    focus_market = markets[market_of_interest] #TODO API return from the latest to the oldest trend
    producer_log.debug(focus_market)
    producer_log.debug(focus_market.trend_list[0].to_repr())


    ########



    which_topic = TopicPartition(topic = market_of_interest, partition = 0)

    message, offset = last_message_topic(which_topic)

    fetched_trends = focus_market.trend_list

    if offset > 1:
        # Go back in market trends until it is found the trend equal the one in the queue

        missing_trends = filter_duplicates(message, Trend, fetched_trends)

                
    else: # no message in the topic's partition
        producer_log.info("No offset present, proceeding writing all the data")
        missing_trends = fetched_trends[1:] # skip most recent as it is still updating
        
    write_list_in_queue(market_of_interest, missing_trends)
