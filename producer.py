
import time
import json
import random
from datetime import datetime
from data_generator import generate_message
import twitter_data
from kafka import KafkaProducer

# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    #print(twitter_data.get_twitter_data())
    for tweet in twitter_data.get_twitter_data():
        tweet_message = tweet
        print(f'Producing message @ {datetime.now()} | Message = {str(tweet_message)}')
        producer.send('pizza', tweet_message)
        # Sleep for 3 seconds
        time.sleep(3)

    # while True:
    #     # Generate a message
    #     dummy_message = generate_message()
    #     #dummy_message = {'user_id': 1, 'recipient_id': 2, 'message': 'Hello World!'}
        
    #     # Send it to our 'brezel' topic
    #     print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
    #     producer.send('pizza', dummy_message)
        
    #     # Sleep for a random number of seconds
    #     time_to_sleep = random.randint(1, 11)
    #     time.sleep(time_to_sleep)