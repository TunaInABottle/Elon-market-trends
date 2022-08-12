
from curses import raw
import os
from MessageData import MessageData
import tweepy
from AbstractFetcher import Fetcher
from dotenv import load_dotenv
load_dotenv(".env")
import datetime
import dateutil.parser as parser

class Tweet(MessageData):
    """Class for new tweets."""
    def __init__(self, id: str, datetime: datetime, text: str, retweets: int) -> None:
        self.id = id
        self.datetime = datetime#.isoformat()
        self.text = text
        self.retweets = retweets

    def to_repr(self) -> dict:
        return {
            "id": self.id,
            "datetime": str(self.datetime), 
            "text": self.text, 
            "retweets": self.retweets
            }

    @staticmethod
    def from_repr(raw_data: dict) -> 'Tweet':
        return Tweet(
            raw_data["id"],
            parser.parse(raw_data["datetime"]),
            raw_data["text"],
            raw_data["retweets"]
        )

    def __eq__(self, other: 'Tweet') -> bool:
        if isinstance(other, Tweet):
            return (self.id == other.id)
        return False
    
class TweetBuilder:
    """Builder for instantiating new tweets."""
    @staticmethod
    def from_tweepy_repr(raw_data: dict) -> Tweet:
        """Make a new Tweet object.

        Args:
            raw_data: a dictionary coming from a call to Twitter API, needed to instantiate an object.

        Returns:
            An instantiated object.
        """
        return Tweet(
            raw_data.id,
            raw_data.created_at,
            raw_data.full_text,
            raw_data.retweet_count
        )

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
       

    def fetch(self, given_id) -> TweetFeed:
        '''returns list of dictionaries with the twitter data'''

        tweets = self._api.user_timeline(id=given_id, count=100, # 200 is the maximum allowed count
                                        include_rts = True, tweet_mode='extended')

        #Instantiate the empty class that collects the tweet in here
        NewTweets = TweetFeed()

        for tweet in tweets:
            NewTweets.add( TweetBuilder.from_tweepy_repr( tweet ) )
        return NewTweets
        

