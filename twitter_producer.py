import time
import twitter_data
import kafkaCustomProducer
from config.setup_logger import producer_log

producer_log.info("New execution launched!")
twitterFetcher = twitter_data.TwitterFetcher()
given_id = 44196397 #Elon Musk

if __name__ == '__main__':
    print("twitter_producer executed")
    break_time = 10 * 60 #10 minutes
    # Infinite loop - fetches Tweets until you kill the program
    while True:
        elon_tweets = twitterFetcher.fetch(given_id)
        #using to custom Producer class
        kafkaCustomProducer.write_unique(topic = 'TWEETS', read_partition = 0, list_elem = elon_tweets.tweets, list_elem_type = twitter_data.Tweet, skip_latest=False )

        print(f"twitter_fetcher: sleeping for {break_time} seconds")
        time.sleep( break_time )