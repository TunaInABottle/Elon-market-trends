
from config.setup_logger import consumer_log 
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from consumer_utils import read_queue, read_queue_by_ts, HOUR_IN_MILLISEC
from pyspark.sql.types import TimestampType
import pyspark.sql.functions as F

def market_fluctuation(mrk_data, date_time, t_interval, offset = 0): # t_interval in hours, offset in minutes
    # print("in market fluct")
    # mrk_data.show()
    # print( date_time )
    
    filt_mrk = mrk_data.filter(
        F.col("datetime").between(
            date_time + F.expr(f"+ interval {offset} minutes"), #from
            date_time + F.expr(f"+ interval {t_interval} hours {offset} minutes"), #to
        )
    ).sort(mrk_data.datetime)

    #filt_mrk.show()
    
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

def get_market_data(sparksession, mkt_name):
    dataf = read_queue_by_ts(mkt_name, 0, 24 * 5 * HOUR_IN_MILLISEC )    
    s_market = sparksession.createDataFrame([(value['datetime'], value['open'], value['high'], value['low'], value['close'], value['volume']) for value in dataf[:-1]], ['datetime', 'open', 'high', 'low', 'close', 'volume'])


    # convert market fields to float
    for col_name in ["open", "high", "low", "close"]:
        s_market = s_market.withColumn(col_name, s_market[col_name].cast('float'))


    s_market = s_market.withColumn("datetime", 
                                  s_market["datetime"]
                                  .cast( TimestampType() ))

    return s_market

def get_tweet_data(sparksession):
    datat = read_queue_by_ts('TWEETS', 0, 48 * HOUR_IN_MILLISEC )

    s_tweet = sparksession.createDataFrame([(value['id'], value['datetime'], value['text'], value['retweets']) for value in datat[:-1]], ['id', 'datetime', 'text', 'retweets'])
    
    # convert datetime type from string to datetime
    s_tweet = s_tweet.withColumn("datetime", 
                                  s_tweet["datetime"]
                                  .cast( TimestampType() )
                    ).withColumn("row_idx",
                                 F.monotonically_increasing_id() )

    # s_tweet = s_tweet.filter(
    #         F.col("datetime").between(
    #             "2022-07-22 0:18:00", #from
    #             F.expr("current_timestamp"),
    #             #"2022-07-22 15:18:00" + F.expr("+ interval 7 hours"), #to
    #         )
    #         )

    return s_tweet



## first spark attempt using MLib pipeline
if __name__ == '__main__':

    spark = SparkSession \
        .builder \
        .appName("SparkModel1") \
        .config("spark.executor.memory", "8g") \
        .config('spark.sql.session.timeZone', 'UTC') \
        .getOrCreate() 
        #spark.executor.memory should define how much memory the process uses

    s_tweet = get_tweet_data(spark)

    consumer_log.info("computing BTC variation according to tweets")
    for market_name in ["CRYPTO_BTC", "CRYPTO_DOGE", "STOCK_TSLA"]:

        s_market = get_market_data(spark, market_name) 

        mkt_fluctuation = []

        # calculate for each entry the corresponding market variation
        for row in s_tweet.collect(): # rowwise operaion does not work with function variables outside dataframe
            mkt_fluctuation.append( (row["row_idx"], market_fluctuation(s_market, row["datetime"], 3, 30)) )

        market_variation = spark.createDataFrame([(value[0], float(value[1])) for value in mkt_fluctuation[:-1]], ['row_idx', f'{market_name.lower()}_var'])

        s_tweet = s_tweet.join(market_variation, on = "row_idx")


    s_tweet.show()

    ### LM training ###

    # Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features").setNumFeatures(150)
    lin_mod1 =  LinearRegression(featuresCol="features", labelCol="retweets", regParam = 0.01) # https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.regression.LinearRegression.html
    
    #lin_mod2 =  LinearRegression(featuresCol="features", labelCol="crypto_btc_var", regParam = 0.01) # https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.regression.LinearRegression.html
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lin_mod1])

    # # Fit the pipeline to training documents.
    model = pipeline.fit(s_tweet)