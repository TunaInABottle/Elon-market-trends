
import datetime
from time import sleep
from typing import List
#from config.setup_logger import consumer_log 
from pyspark.sql import SparkSession, dataframe
from kafkaCustomProducer import last_message_in_topic
from kafka import TopicPartition
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from consumer_utils import read_queue, read_queue_by_ts, HOUR_IN_MILLISEC
from pyspark.sql.types import TimestampType
import pyspark.sql.functions as F

def market_fluctuation(mrk_data: dataframe.DataFrame, date_time: datetime, t_interval: int, offset: int = 0) -> float: # t_interval in hours, offset in minutes
    
    filt_mrk = mrk_data.filter(
        F.col("datetime").between(
            date_time + F.expr(f"+ interval {offset} minutes"), #from
            date_time + F.expr(f"+ interval {t_interval} hours {offset} minutes"), #to
        )
    )
    
    if filt_mrk.count() == 0:
        return 0

    # obtain the largest fluctuation
    variation1 = ( filt_mrk.first()["high"] - filt_mrk.tail(1)[0]["low"] ) / filt_mrk.first()["open"]
    variation2 = ( filt_mrk.first()["low"] - filt_mrk.tail(1)[0]["high"] ) / filt_mrk.first()["open"]
    max_fluctuation = max( abs(variation1) , abs(variation2) )
    # needed in order to return the value with highest variation (distance from 0)
    if max_fluctuation == abs(variation1):
        return variation1
    else:
        return variation2

def get_spark_market_data(sparksession: SparkSession, mkt_name: str, hours_ago: int) -> dataframe.DataFrame:
    """
    TODO
    """
    dataf = read_queue_by_ts(mkt_name, 0, hours_ago * HOUR_IN_MILLISEC )    
    s_market = sparksession.createDataFrame([(value['datetime'], value['open'], value['high'], value['low'], value['close'], value['volume']) for value in dataf[:-1]], ['datetime', 'open', 'high', 'low', 'close', 'volume'])


    # convert market fields to float
    for col_name in ["open", "high", "low", "close"]:
        s_market = s_market.withColumn(col_name, s_market[col_name].cast('float'))

    s_market = s_market.withColumn("datetime", 
                                  s_market["datetime"]
                                  .cast( TimestampType() ))
    return s_market

def get_spark_tweet_data(sparksession: SparkSession, hours_ago: int) -> dataframe.DataFrame: 
    """
    TODO
    """
    data = reversed(read_queue_by_ts('TWEETS', 0, hours_ago * HOUR_IN_MILLISEC )) # reverse is used so that dates are written decrescently

    s_tweet = spark_tweet_list(sparksession, data)

    # processing for the model
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    s_tweet = tokenizer.transform(s_tweet)
    hashingTF = HashingTF(inputCol="words", outputCol="features").setNumFeatures(150)
    s_tweet = hashingTF.transform(s_tweet)
    return s_tweet

def spark_tweet_list(sparksession: SparkSession, data: List[str]) -> dataframe.DataFrame:
    """
    TODO
    """
    s_tweet = sparksession.createDataFrame([(value['id'], value['datetime'], value['text'], value['retweets']) for value in data],
                                           ['id', 'datetime', 'text', 'retweets'])
    
    # convert datetime type from string to datetime
    s_tweet = s_tweet.withColumn("datetime", 
                                  s_tweet["datetime"]
                                  .cast( TimestampType() )
                    ).withColumn("row_idx",
                                 F.monotonically_increasing_id() 
                    )#.sort(s_tweet["id"].desc()) # not like arranging dates? You sus
    return s_tweet

def predict_market_by_last_tweet(spark: SparkSession, s_tweet: dataframe.DataFrame, s_market: dataframe.DataFrame, market_col_name: str) -> float:
    mkt_fluctuation = []

    # calculate for each entry the corresponding market variation
    for row in s_tweet.collect(): # rowwise operation does not work with function variables outside dataframe
        mkt_fluctuation.append( (row["row_idx"], market_fluctuation(s_market, row["datetime"], 3, 30)) )

    market_variation = spark.createDataFrame([(value[0], float(value[1])) for value in mkt_fluctuation], ['row_idx', market_col_name])

    s_tweet = s_tweet.join(market_variation, on = "row_idx", how = "left")

    train_data = spark.createDataFrame(s_tweet.tail(s_tweet.count()-1), s_tweet.schema)
    test_data = spark.createDataFrame(s_tweet.take(1))

    ss = LinearRegression(featuresCol='features', labelCol = market_col_name, regParam = 0.01)
    ss = ss.fit(train_data)
    pred = ss.evaluate(test_data)
        
    market_prediction_trend = pred.predictions.first()["prediction"]
    return market_prediction_trend

def predict():
    spark = SparkSession \
        .builder \
        .appName("SparkModel_one") \
        .config("spark.executor.memory", "8g") \
        .config('spark.sql.session.timeZone', 'UTC') \
        .getOrCreate() 

    hour_offset = 3 * 24 # 3 days
    markets = ["CRYPTO_BTC", "CRYPTO_DOGE", "STOCK_TSLA"]

    s_tweet = get_spark_tweet_data(spark, hour_offset)

    market_fluct_dict = {}
    for market in markets:
        #consumer_log.info("computing {market_name} variation according to tweets")

        market_col_name = market.lower()
        s_market = get_spark_market_data(spark, market, hour_offset) 

        market_fluct_dict[market_col_name] = predict_market_by_last_tweet(spark, s_tweet, s_market, market_col_name )

    return market_fluct_dict





if __name__ == '__main__':
    last_tweet = last_message_in_topic(TopicPartition("TWEETS", 0))
    sleep_time = 30 * 60 # 30 minutes
    while True:
        print("Model ready to execute")
        if last_tweet != last_message_in_topic(TopicPartition("TWEETS", 0)):
            print("New tweet! Computing prediction...")
            predictions = predict()
            print(predictions)
            last_tweet = last_message_in_topic(TopicPartition("TWEETS", 0))
        else:
            print("No new tweet detected")
        print(f"Returning to sleep for {sleep_time} seconds")
        sleep( sleep_time )
    

