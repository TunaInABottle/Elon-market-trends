
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from consumer_utils import read_queue, read_queue_by_ts, HOUR_IN_MILLISEC

## first spark attempt using MLib pipeline
if __name__ == '__main__':
    #messages = read_queue('CRYPTO_BTC', 0, last_n_messages = 20 )
    #consumer_log.debug( f"ara")
    
    dataf =  read_queue_by_ts('CRYPTO_BTC', 0, 3 * HOUR_IN_MILLISEC ) 

    datat = read_queue_by_ts('pizza', 0, 3 * HOUR_IN_MILLISEC )

    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .getOrCreate()

    # print([(value['datetime'],) for value in dataf])

    #creating a spark datafram from the twitter data in the kafka queue
    dft = spark.createDataFrame([(value['id'], value['datetime'], value['text'], value['retweets']) for value in datat[:-1]], ['id', 'datetime', 'text', 'retweets'])

    dft.show()

    # Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
    lr = LogisticRegression(maxIter=2, regParam=0.001, featuresCol='features', labelCol='retweets')
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

    # Fit the pipeline to training documents.
    model = pipeline.fit(dft)

    test = spark.createDataFrame([(value['id'], value['datetime'], value['text']) for value in datat[-1]], ['id', 'datetime', 'text'])

    prediction = model.transform(test)
    selected = prediction.select("id", "datetime", "text", "prediction")
    for row in selected.collect():
        rid, text, prob, prediction = row
        print(
            "(%d, %s) --> prob=%s, prediction=%f" % (
                rid, text, str(prob), prediction   # type: ignore
            )
        )

    # df = spark.createDataFrame([(value['datetime'], value['open'], value['close'], value['high'], value['low']) for value in dataf], ['datetime', 'open', 'close', 'high', 'low'])

    # df.show()
