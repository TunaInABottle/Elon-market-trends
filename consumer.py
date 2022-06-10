

from kafka import KafkaConsumer, TopicPartition
consumer = KafkaConsumer(bootstrap_servers='localhost:9092')

print("assifning partition")
consumer.assign([TopicPartition('pizza', 2)])

print("Consuming message")
msg = next(consumer)

print(msg)