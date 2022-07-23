
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from consumer_utils import read_queue, read_queue_by_ts, HOUR_IN_MILLISEC

### TODO ###
### try-catch as consumer is trying to get data of missing time serier as producer felt behind

## first spark attempt using MLib pipeline
if __name__ == '__main__':
    #messages = read_queue('CRYPTO_BTC', 0, last_n_messages = 20 )
    #consumer_log.debug( f"ara")
    
    dataf =  read_queue_by_ts('CRYPTO_BTC', 0, 3 * HOUR_IN_MILLISEC ) 

    datat = read_queue_by_ts('pizza', 0, 48 * HOUR_IN_MILLISEC )

    spark = SparkSession \
        .builder \
        .appName("SparkModel1") \
        .config("spark.executor.memory", "8g") \
        .getOrCreate() 
        #spark.executor.memory should define how much memory the process uses

    #print([(value['datetime'],) for value in dataf])
    #print([(value,) for value in datat])

    #creating a spark datafram from the twitter data in the kafka queue
    dft = spark.createDataFrame([(value['id'], value['datetime'], value['text'], value['retweets']) for value in datat[:-1]], ['id', 'datetime', 'text', 'retweets'])

    # Rainfallmm_udf = udf(lambda top_tweet: 1 if retweets > 200 else 0, IntegerType())

    dft.show()

    dft.filter(dft.retweets > 200).sort(dft.retweets).show()


    # tokenizer = Tokenizer(inputCol="text", outputCol="words")
    # wordsDataFrame = tokenizer.transform(dft)
    # # for words_label in wordsDataFrame.select("words").take(3):
    # #     print(words_label)

    # hashingTF = HashingTF(inputCol="words", outputCol="features").setNumFeatures(8)
    # hashingDataFrame = hashingTF.transform(wordsDataFrame)

    # hashingDataFrame.show()

    # algo = LinearRegression(featuresCol="features", labelCol="retweets")
    # model = algo.fit(hashingDataFrame)

    ##############################################################


    # Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features").setNumFeatures(8)
    lin_mod =  LinearRegression(featuresCol="features", labelCol="retweets", regParam = 0.01) # https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.regression.LinearRegression.html
    # lr = LogisticRegression(maxIter=2, regParam=0.001, featuresCol='features', labelCol='retweets')
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lin_mod])

    # # Fit the pipeline to training documents.
    model = pipeline.fit(dft)


    ### #### ###
    ### TODO ###
    # write the large market movement in the df, for each tweet and market

    # ######################################################################

    # test = spark.createDataFrame([(value['id'], value['datetime'], value['text']) for value in datat[-1]], ['id', 'datetime', 'text'])

    # prediction = model.transform(test)
    # selected = prediction.select("id", "datetime", "text", "prediction")
    # for row in selected.collect():
    #     rid, text, prob, prediction = row
    #     print(
    #         "(%d, %s) --> prob=%s, prediction=%f" % (
    #             rid, text, str(prob), prediction   # type: ignore
    #         )
    #     )

    # # df = spark.createDataFrame([(value['datetime'], value['open'], value['close'], value['high'], value['low']) for value in dataf], ['datetime', 'open', 'close', 'high', 'low'])

    # # df.show()
