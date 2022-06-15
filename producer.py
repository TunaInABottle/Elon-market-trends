
import time
import json
import random
from datetime import datetime
from data_generator import generate_message
import twitter_data
from kafka import KafkaProducer
from setup_logger import fetch_log 

# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

twitterFetcher = twitter_data.TwitterFetcher()
given_id = 44196397 #Elon Musk

if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    
    for tweet in twitterFetcher.get_twitter_data(given_id):
        tweet_message = tweet
        fetch_log.info(f'Producing message @ {datetime.now()} | Message = {str(tweet_message)}')
        print(f'Producing message @ {datetime.now()} | Message = {str(tweet_message)}')
        producer.send('pizza', tweet_message)
        # Sleep for 3 seconds
        time.sleep(3)

