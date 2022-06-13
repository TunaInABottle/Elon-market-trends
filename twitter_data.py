#TRYING TO MAKE CLASSES WORK

import os
import tweepy
import secretfile

#had to create a secretfile.py file to store the API keys and tokens because I couldn't get the environment variables to work when there already exists a .env folder, but I need a .env file to store the API keys and tokens.

class TwitterFetcher:

    '''Class to get fetch the twitter data from a given user id'''

    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.api_key_secret = os.getenv('API_KEY_SECRET')
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self.auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        self.api = tweepy.API(self.auth)
        self.client = tweepy.Client( bearer_token= self.bearer_token, 
                        consumer_key=self.api_key, 
                        consumer_secret=self.api_key_secret, 
                        access_token=self.access_token, 
                        access_token_secret=self.access_token_secret,
                        wait_on_rate_limit=True,
                        return_type=dict)
       

    def get_twitter_data(self, given_id) -> list:
        '''returns list of dictionaries with the twitter data'''

        tweets = self.api.user_timeline(id=given_id, count=10, # 200 is the maximum allowed count
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

