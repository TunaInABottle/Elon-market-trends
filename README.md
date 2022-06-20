# Elon-market-trends

### What we have so far in this project:

- Setup of kafka using docker
- kafka consumer + kafka producer
- sample data generator to generate messages for testing
- requirement.txt file with the requirements
- init.sh script to autimatically set up the virtual environment
- getting Elon Musk Twitter Data
- sending each tweet seperately to kafka

## How to Run:

### Setting up the virtual environment

To install the requirements run this in terminal:
`source init.sh`

### Setting up Kafka with docker

(put quick tutorial here how to set up our kafka environment so that it can be replicated)

### Create a Twitter Developer Account

Once you have your twitter API account, create a file `.env` and put your keys in there like so:
(replace 'your_key' with your keys). This sets the API keys as environment variables.

```bash
API_KEY = your_key
API_KEY_SECRET = your_key
BEARER_TOKEN = your_key
ACCESS_TOKEN = your_key
ACCESS_TOKEN_SECRET = your_key
```

### Run the code

To run the code for testing, open the folder in VS Code, open a split Terminal and first run the consumer.py, then the producer.py file in the other window. You should see the producer producing messages (containing twitter Info) and the consumer receiving it.


## google docs:

https://docs.google.com/document/d/12WIlLMl_l3vX2dv1bb3ZnQXg9orOfPYFRbv1ARFO-7A/edit


## write on paper

- As it is a dummy example, for the kafka topics we set up replication factor and partition equal to 1. In case of a deployment, it might be worth considering better number  so to improve robustness
- Currently the fetching in Kafka's topics is based on an estimation of Elon Musk's Tweets per day multiplied by the number of days the model deems relevant for the computation. If this system would run for longer, it would be possible to get messages based on Kafka's offset thanks to the call https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html#kafka.KafkaConsumer.offsets_for_times
