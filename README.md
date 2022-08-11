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

### Setting up Kafka with docker

- Install and open Docker Desktop (if not already installed)
- Download the following Docker images for Kafka:
    - https://hub.docker.com/r/wurstmeister/zookeeper/
    - https://hub.docker.com/r/wurstmeister/kafka/ 
    This can be done with the following commands: 
    `docker pull wurstmeister/kafka`
    `docker pull wurstmeister/zookeeper`

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

### Get a API key for AlphaVantage

follow the instructions here:
https://www.alphavantage.co/support/#api-key 

### Run the code

To install the requirements in a virtual environment and run the code, enter this in terminal/command line:
`source init.sh`

This will first start the Docker images, then fetch the market & Twitter data and after some waiting time starts the prediction model

(we noticed that on some machines the docker containers need more time to start the first time, in that case starting them manually or running the command again might help)
