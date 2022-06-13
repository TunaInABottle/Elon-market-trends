import tweepy
import os
import secretfile

#had to create a secretfile.py file to store the API keys and tokens because I couldn't get the environment variables to work when there already exists a .env folder, but I need a .env file to store the API keys and tokens.


def initializate_twitter_client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.Client:
    return tweepy.Client( bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret,
                        wait_on_rate_limit=True,
                        return_type=dict)


def get_twitter_data() -> list:
    #setting environment variables
    API_KEY = os.getenv('API_KEY')
    API_KEY_SECRET = os.getenv('API_KEY_SECRET')
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    print(API_KEY)

    #authenticating
    #auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    api = tweepy.API(auth)

    client= initializate_twitter_client(BEARER_TOKEN, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    #testing with my own twitter id
    #given_id = 1161945605192790016
    given_id = 44196397
    tweets = api.user_timeline(id=given_id, count=10, # 200 is the maximum allowed count
                                include_rts = True,tweet_mode='extended')
    tweets_to_return = []

    #testing with first ten
    for t in tweets[:10]:
        dic = {}
        dic['id'] = t.id
        dic['created_at'] = str(t.created_at)
        dic['text'] = t.full_text
        dic['retweet_count'] = t.retweet_count
        tweets_to_return.append(dic)
    return tweets_to_return


    #all_followers = client.get_users_followers(id= given_id)

    #print(all_followers)

#print(get_twitter_data())
