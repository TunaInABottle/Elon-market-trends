from abc import ABC, abstractmethod
import json



class FetcherClusters(ABC):
    def __init__(self, api_key: str) -> None:
        self._fetcher_list = {}
        self._api_key = api_key


    #@property
    #@abstractmethod
    #def _api_key():
    #    raise NotImplementedError

    @abstractmethod
    def fetch_all(self) -> json:
        pass

    @abstractmethod
    def add(self) -> None:
        pass
