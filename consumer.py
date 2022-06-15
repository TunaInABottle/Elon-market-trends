

import json 
from kafka import KafkaConsumer
from setup_logger import fetch_log 

if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        'pizza',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    for message in consumer:
        print(json.loads(message.value))
        fetch_log.info(json.loads(message.value))