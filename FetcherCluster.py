from abc import ABC, abstractmethod
from typing import Dict, Type
from Fetcher import Fetcher
from typing import TypeVar


T = TypeVar("T", bound="FetcherCluster")

class FetcherCluster(ABC):
    """
    Represent a generic cluster of web fetchers that pool from the same source.
    """
    def __init__(self, api_key: str) -> None:
        self._fetcher_list: Dict[str, Type[Fetcher]] = {}
        self._api_key = api_key


    #@property
    #@abstractmethod
    #def _api_key():
    #    raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], fetcher_dict: dict) -> T:
            
        """
        Istantiate class from a dictionary
        """
        pass

    @abstractmethod
    def fetch_all(self) -> str:
        pass

    @abstractmethod
    def add(self, fetcher: Type[Fetcher]) -> None:
        pass
