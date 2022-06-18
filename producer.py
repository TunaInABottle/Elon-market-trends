
import time
import json
from datetime import datetime
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
    Tweets= twitterFetcher.fetch(given_id)

    for tweet in Tweets.tweets:
        fetch_log.info(f'Producing message @ {datetime.now()} | Message = {str(tweet.to_repr())}')
        print(f'Producing message @ {datetime.now()} | Message = {str(tweet.to_repr())}')
        producer.send('pizza', tweet.to_repr())
        # Sleep for 3 seconds
        time.sleep(3)

