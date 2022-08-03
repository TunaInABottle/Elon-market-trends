import time
import json
from datetime import datetime
import twitter_data
from kafka import KafkaProducer
import kafkaCustomProducer
from time import sleep

#from setup_logger import fetch_log 

# Kafka Producer
# producer = KafkaProducer(
#     bootstrap_servers = ['localhost:9092'],
#     value_serializer = lambda x: json.dumps(x).encode('utf-8')
# )

twitterFetcher = twitter_data.TwitterFetcher()
given_id = 44196397 #Elon Musk

if __name__ == '__main__':
    print("twitter_producer executed")
    break_time = 10 * 60
    # Infinite loop - runs until you kill the program
    while True:
        elon_tweets = twitterFetcher.fetch(given_id)
        #updated to custom Producer class
        kafkaCustomProducer.write_unique(topic = 'TWEETS', read_partition = 0, list_elem = elon_tweets.tweets, list_elem_type = twitter_data.Tweet, skip_latest=False )

        print(f"twitter_fetcher: sleeping for {break_time} seconds")
        time.sleep( break_time )

    # for tweet in elon_tweets.tweets:
    #     #fetch_log.info(f'Producing message @ {datetime.now()} | Message = {str(tweet.to_repr())}')
    #     print(f'Producing message @ {datetime.now()} | Message = {str(tweet.to_repr())}')
    #     producer.send('pizza', tweet.to_repr())
    #     # Sleep for 3 seconds
    #     time.sleep(3)


        