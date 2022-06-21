import json 
from kafka import KafkaConsumer, TopicPartition
from setup_logger import fetch_log 

def read_queue(topic_name: str, partition: int, last_n_messages: int = 0) -> list:
    """Read messages from a Kafka queue.

    Args:
        topic_name: the name of Kafka's queue.
        partition: the number of the partition to read.
        last_n_message: how many messages read from the latest, if 0 make polling. default: 0
    """
    consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id = "my_horse_is_amazing"
    )
    topic = TopicPartition(topic = topic_name, partition = partition)
    consumer.assign([topic])
    
    last_offset = consumer.position(topic)

    consumer.seek( topic, consumer.position(topic) - last_n_messages ) # obtain the last n elements

    messages = []

    for message in consumer:
        print(json.loads(message.value))
        #cfetch_log.info(json.loads(message.value))
        messages.append( json.loads(message.value ) )

        if message.offset == last_offset - 1:
            break
    
    consumer.close()
    print("Consumer has ended")

    return messages


if __name__ == '__main__':
    messages = read_queue('TSLA_STOCK', 0, last_n_messages = 100 )
