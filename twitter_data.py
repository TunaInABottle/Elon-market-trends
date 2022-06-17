#TRYING TO MAKE CLASSES WORK

import os
from MessageData import MessageData
import tweepy
from AbstractFetcher import Fetcher
from setup_logger import fetch_log 
from dotenv import load_dotenv # WHY DOES THIS NOT WORK HUH?
#import secretfile
load_dotenv(".env")

class Tweet(MessageData):
    def __init__(self, twitter_dict: dict) -> None:
        self.id = twitter_dict.id
        self.creation_time = str(twitter_dict.created_at)
        self.text = twitter_dict.full_text
        self.retweets = twitter_dict.retweet_count

    def to_repr(self) -> dict:
        pass

    @staticmethod
    def from_repr(raw_data: dict) -> 'Tweet':
        pass
    

class TweetFeed():
    ''' Class containing the twitter Data'''
    def __init__(self):
        self.tweets = []
    
    def add(self, tweet):
        self.tweets.append(tweet)


class TwitterFetcher(Fetcher):
    '''Class to get fetch the twitter data from a given user id'''

    def __init__(self):
        self._api_key = os.getenv('API_KEY')
        self._api_key_secret = os.getenv('API_KEY_SECRET')
        self._bearer_token = os.getenv('BEARER_TOKEN')
        self._access_token = os.getenv('ACCESS_TOKEN')
        self._access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self._auth = tweepy.OAuthHandler(self._api_key, self._api_key_secret)
        self._api = tweepy.API(self._auth)
        self.client = tweepy.Client( bearer_token= self._bearer_token, 
                        consumer_key=self._api_key, 
                        consumer_secret=self._api_key_secret, 
                        access_token=self._access_token, 
                        access_token_secret=self._access_token_secret,
                        wait_on_rate_limit=True,
                        return_type=dict)
       

    def get_twitter_data(self, given_id) -> list:
        '''returns list of dictionaries with the twitter data'''

        tweets = self._api.user_timeline(id=given_id, count=10, # 200 is the maximum allowed count
                                        include_rts = True,tweet_mode='extended')
        tweets_to_return = []
        for tweet in tweets[:10]:
            dic = {}
            dic['id'] = tweet.id
            dic['created_at'] = str(tweet.created_at)
            dic['text'] = tweet.full_text
            dic['retweet_count'] = tweet.retweet_count
            tweets_to_return.append(dic)
        return tweets_to_return

    def fetch(self) -> TweetFeed:
        '''returns list of dictionaries with the twitter data'''

        tweets = self._api.user_timeline(id=44196397, count=10, # 200 is the maximum allowed count
                                        include_rts = True, tweet_mode='extended')

        #Instantiate the empty class that collects the tweet in here
        NewTweets= TweetFeed()

        for tweet in tweets[:10]:
            NewTweets.add( Tweet( tweet ) )
        return NewTweets
        

