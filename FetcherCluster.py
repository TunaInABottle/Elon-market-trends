from abc import ABC, abstractmethod
import json

from Fetcher import Fetcher



class FetcherCluster(ABC):
    """
    Represent a generic cluster of web fetchers that pool from the same source.
    """
    def __init__(self, api_key: str) -> None:
        self._fetcher_list = {}
        self._api_key = api_key


    #@property
    #@abstractmethod
    #def _api_key():
    #    raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, fetcher_dict: dict) -> None:
            
        """
        Istantiate class from a dictionary
        """
        pass

    @abstractmethod
    def fetch_all(self) -> json:
        pass

    @abstractmethod
    def add(self, fetcher: Fetcher) -> None:
        pass
