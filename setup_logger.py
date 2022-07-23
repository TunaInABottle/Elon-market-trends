# source: https://stackoverflow.com/questions/50391429/logging-in-classes-python
import logging, logging.config, yaml

import os
if not os.path.exists('log'):
    os.makedirs('log')

with open('./config/logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)



fetch_log = logging.getLogger("fetchersLogger")
producer_log = logging.getLogger("producersLogger")
model_log = logging.getLogger("modelLogger")
consumer_log = logging.getLogger("consumersLogger")

