from abc import ABC, abstractmethod
import json

from Fetcher import Fetcher



class FetcherCluster(ABC):
    def __init__(self, api_key: str) -> None:
        self._fetcher_list = {}
        self._api_key = api_key


    #@property
    #@abstractmethod
    #def _api_key():
    #    raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, api_key: str, fetcher_init_dict: dict): # -> FetcherCluster:
            #cluster = cls(api_key)
            # add each fetcher into cluster
            #return cluster
            pass

    @abstractmethod
    def fetch_all(self) -> json:
        pass

    @abstractmethod
    def add(self, fetcher: Fetcher) -> None:
        pass

    #def fetch(self, source_name: str):
    #    pass