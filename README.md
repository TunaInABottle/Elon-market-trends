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

Once you have your twitter API account, create a file `secretfile.py` and put your keys in there like so:
(replace 'your key' with your keys)

```python
import os
os.environ['API_KEY'] = 'your key'
os.environ['API_KEY_SECRET'] = 'your key'
os.environ['BEARER_TOKEN'] = 'your key
os.environ['ACCESS_TOKEN'] = 'your key'
os.environ['ACCESS_TOKEN_SECRET'] = 'your key'
```

### Run the code

To run the code for testing, open the folder in VS Code, open a split Terminal and first run the consumer.py, then the producer.py file in the other window. You should see the producer producing messages (containing twitter Info) and the consumer receiving it.


## google docs:

https://docs.google.com/document/d/12WIlLMl_l3vX2dv1bb3ZnQXg9orOfPYFRbv1ARFO-7A/edit
