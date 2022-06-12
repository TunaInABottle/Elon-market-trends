# source: https://stackoverflow.com/questions/50391429/logging-in-classes-python
import logging, logging.config, yaml


with open('./config/logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)



fetch_log = logging.getLogger("fetchersLogger")

