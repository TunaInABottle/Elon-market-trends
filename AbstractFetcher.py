from abc import ABC, abstractmethod
from typing import Dict, List, Type
from typing import TypeVar

from MessageData import MessageData

### examples of abstract classhttps://www.pythontutorial.net/python-oop/python-abstract-class/
### @abstractclass meaning https://www.geeksforgeeks.org/classmethod-in-python/

class Fetcher(ABC):
    @abstractmethod
    def fetch(self) -> List[MessageData]:
        """ Obtain information from the endpoint.

        Returns:
        The information the fetcher is requested to fetch.
        """
        pass



########################


T = TypeVar("T", bound="FetcherCluster")

class FetcherCluster(ABC):
    """
    Represent a generic cluster of web fetchers that pool from the same source.
    """
    def __init__(self, api_key: str) -> None:
        self._fetcher_list: Dict[str, Type[Fetcher]] = {}
        self._api_key = api_key

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], fetcher_dict: dict) -> T:
            
        """
        Istantiate class from a dictionary
        """
        pass

    @abstractmethod
    def fetch_all(self) -> dict:
        pass

    @abstractmethod
    def add(self, fetcher: Type[Fetcher]) -> None:
        pass