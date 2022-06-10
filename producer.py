from kafka import KafkaProducer

print("Sending message")

producer = KafkaProducer(bootstrap_servers='localhost:9092')
for idx in range(20):
    print("message sent")

    producer.send('pizza', (idx).to_bytes(2, byteorder='big'))

