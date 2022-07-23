
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



## first spark attempt using MLib pipeline
if __name__ == '__main__':
    dataf =  read_queue_by_ts('CRYPTO_BTC', 0, 24 * 5 * HOUR_IN_MILLISEC ) 

    datat = read_queue_by_ts('pizza', 0, 48 * HOUR_IN_MILLISEC )

    spark = SparkSession \
        .builder \
        .appName("SparkModel1") \
        .config("spark.executor.memory", "8g") \
        .config('spark.sql.session.timeZone', 'UTC') \
        .getOrCreate() 
        #spark.executor.memory should define how much memory the process uses

    s_tweet = spark.createDataFrame([(value['id'], value['datetime'], value['text'], value['retweets']) for value in datat[:-1]], ['id', 'datetime', 'text', 'retweets'])
    s_market = spark.createDataFrame([(value['datetime'], value['open'], value['high'], value['low'], value['close'], value['volume']) for value in dataf[:-1]], ['datetime', 'open', 'high', 'low', 'close', 'volume'])

    # convert market fields to float
    for col_name in ["open", "high", "low", "close"]:
        s_market = s_market.withColumn(col_name, s_market[col_name].cast('float'))

    # convert datetime type from string to datetime
    s_tweet = s_tweet.withColumn("datetime", 
                                  s_tweet["datetime"]
                                  .cast( TimestampType() ))


    s_market = s_market.withColumn("datetime", 
                                  s_market["datetime"]
                                  .cast( TimestampType() ))
    s_tweet.show()
    s_market.show()



    # Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features").setNumFeatures(150)
    lin_mod =  LinearRegression(featuresCol="features", labelCol="retweets", regParam = 0.01) # https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.regression.LinearRegression.html
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lin_mod])

    # # Fit the pipeline to training documents.
    #model = pipeline.fit(s_tweet)

    
    # df3 = s_tweet.filter(
    #         F.col("datetime").between(
    #             F.expr("current_timestamp - interval 24 hours"), #from
    #             F.expr("current_timestamp"), #to
    #         )
    #     )




    df4 = s_tweet.filter(
            F.col("datetime").between(
                "2022-07-22 0:18:00", #from
                F.expr("current_timestamp"),
                #"2022-07-22 15:18:00" + F.expr("+ interval 7 hours"), #to
            )
            )
    df4.show()

    # market_fluctuation_udf = F.udf(lambda dt: market_fluctuation(s_market, dt, 3, 30))
    # df5 = df4.withColumn("BTC_var", 
    #                     market_fluctuation_udf(df4["datetime"]))
    
    ph = []
    for row in df4.collect(): # rowwise operaion does not work with function variables outside dataframe
        ph.append( market_fluctuation(s_market, row["datetime"], 3, 30) )


    print(ph)
    #df5.show()