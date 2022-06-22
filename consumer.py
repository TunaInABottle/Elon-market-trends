import datetime
import json
import time
from kafka import KafkaConsumer, TopicPartition
from setup_logger import consumer_log 
from typing import Final

HOUR_MILLISEC: Final[int] =  60 * 60 * 1000

def read_queue(topic_name: str, partition: int, last_n_messages: int = 0) -> list:
    """Read messages from a Kafka queue.

    Args:
        topic_name: the name of Kafka's queue.
        partition: the number of the partition to read.
        last_n_message: how many messages read from the latest, if 0 it will poll. default: 0
    """
    consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id = "my_horse_is_amazing"
    )
    topic = TopicPartition(topic = topic_name, partition = partition)
    consumer.assign([topic])
    
    last_offset = consumer.end_offsets([topic])[topic]

    try:
        consumer.seek( topic, last_offset - last_n_messages ) # obtain the last n elements
    except AssertionError as ae:
        consumer_log.warning(f"Tried to access an offset that is larger than the queue, fetching all the messages in the queue")
        consumer.seek_to_beginning()

    messages = []

    for message in consumer:
        consumer_log.debug( f"reading from \"{message.topic}\" offset {message.offset} timestamp {datetime.datetime.fromtimestamp(message.timestamp / 1000) } value {json.loads(message.value)}")
        messages.append( json.loads(message.value ) )

        if message.offset == last_offset - 1:
            break
    
    consumer.close()
    print("Consumer has ended")

    return messages


def read_queue_by_ts(topic_name: str, partition: int, last_millisec: int = 0) -> list:
    """TODO
    """

    consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id = "my_horse_is_amazing"
    )
    topic = TopicPartition(topic = topic_name, partition = partition)
    consumer.assign([topic])
    
    last_offset = consumer.end_offsets([topic])[topic]

    consumer_log.debug(f"print everything before offset {last_offset}")


    offset = None
    try:
        now_ts_epoch = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        starting_ts = now_ts_epoch - last_millisec
        topic_ts_offset = consumer.offsets_for_times( {topic: starting_ts } )
        consumer_log.debug(f"ts: {datetime.datetime.utcfromtimestamp(starting_ts / 1000)} | read from {topic_ts_offset} | effective datetime {datetime.datetime.utcfromtimestamp(topic_ts_offset[topic].timestamp / 1000 )}")
        offset = topic_ts_offset[topic].offset
    except AssertionError as ae:
        consumer_log.warning(f"Tried to access an offset that is larger than the queue, fetching all the messages in the queue")
        offset = consumer.seek_to_beginning().position(topic)
    except AttributeError as ae:
        consumer_log.error(f"Tried to go before the beginning of the queue. {ae}")
        raise


    consumer.seek( topic, offset )

    messages = []

    for message in consumer:
        consumer_log.debug( f"reading from {message.topic} offset {message.offset} timestamp {datetime.datetime.utcfromtimestamp(message.timestamp / 1000) } value {json.loads(message.value)}")
        messages.append( json.loads(message.value ) )

        if message.offset == last_offset - 1:
            break
    
    consumer.close()
    print("Consumer has ended")

    return messages



if __name__ == '__main__':
    #messages = read_queue('CRYPTO_BTC', 0, last_n_messages = 20 )
    #consumer_log.debug( f"ara")
    
    read_queue_by_ts('CRYPTO_BTC', 0, 3 * HOUR_MILLISEC )
    
    print( datetime.datetime.utcnow() )

    print( datetime.datetime.utcfromtimestamp(  int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() )  ) )

    print( datetime.datetime.utcfromtimestamp(0 * HOUR_MILLISEC / 1000 ) )

    #messages = read_queue('CRYPTO_BTC', 0, last_n_messages = 0 )

    