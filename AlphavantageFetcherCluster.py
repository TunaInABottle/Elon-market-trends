from FetcherCluster import FetcherCluster
import json

#############

import logging, logging.config, yaml

with open('./config/logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger("fetchersLogger")

#############




class AlphavantageFetcherCluster(FetcherCluster):
    def __init__(self, api_key: str) -> None:
        self._fetcher_list = {}
        self._api_key = api_key
        logger.info("AlphavantageFetcherCluster istantiated")


    @classmethod
    def from_dict(cls, api_key: str, fetcher_init_dict: dict): # -> FetcherCluster:
            #cluster = cls(api_key)
            # add each fetcher into cluster
            #return cluster
            pass


    def fetch_all(self) -> json:
        pass


    def add(self) -> None:
        pass