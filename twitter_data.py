#TRYING TO MAKE CLASSES WORK

import os
import tweepy
from AbstractFetcher import Fetcher
from setup_logger import fetch_log 
from dotenv import load_dotenv # WHY DOES THIS NOT WORK HUH?
#import secretfile
load_dotenv(".env")

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
        for t in tweets[:10]:
            dic = {}
            dic['id'] = t.id
            dic['created_at'] = str(t.created_at)
            dic['text'] = t.full_text
            dic['retweet_count'] = t.retweet_count
            tweets_to_return.append(dic)
        return tweets_to_return

    def fetch(self) -> list: #possible to change this to list?
        '''returns list of dictionaries with the twitter data'''

        tweets = self._api.user_timeline(id=44196397, count=10, # 200 is the maximum allowed count
                                        include_rts = True,tweet_mode='extended')
        tweets_to_return = []
        for t in tweets[:10]:
            dic = {}
            dic['id'] = t.id
            dic['created_at'] = str(t.created_at)
            dic['text'] = t.full_text
            dic['retweet_count'] = t.retweet_count
            tweets_to_return.append(dic)
        return tweets_to_return
        

