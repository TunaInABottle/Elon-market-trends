import json 
from kafka import KafkaConsumer, TopicPartition
from setup_logger import fetch_log 

def read_queue(topic: TopicPartition, last_n_messages = 0):
    # Kafka Consumer 
    consumer = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id = "my_horse_is_amazing"
    )
    consumer.assign([topic])
    
    last_offset = consumer.position(topic)

    consumer.seek( topic, consumer.position(topic) - last_n_messages ) # obtain the last n elements

    for message in consumer:
        print(json.loads(message.value))
        #cfetch_log.info(json.loads(message.value))

        if message.offset == last_offset - 1:
            break

    print("Consumer has ended")


if __name__ == '__main__':
    read_queue(TopicPartition(topic = 'TSLA_STOCK', partition = 0), last_n_messages=0)


    # # Kafka Consumer 
    # consumer = KafkaConsumer(
    #     bootstrap_servers='localhost:9092',
    #     auto_offset_reset='earliest',
    #     group_id = "my_horse_is_amazing"
    # )

    # topic = TopicPartition(topic = 'TSLA_STOCK', partition = 0)
    # consumer.assign([topic])

    # last_offset = consumer.position(topic)
    
    # print(last_offset)
    # #consumer.seek( topic, last_offset - 100 ) # obtain the last 100 elements

    # for message in consumer:
    #     print(json.loads(message.value))
    #     #cfetch_log.info(json.loads(message.value))

    #     if message.offset == last_offset - 1:
    #         break

    # print("Consumer has ended")