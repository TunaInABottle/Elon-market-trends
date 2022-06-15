from abc import ABC, abstractmethod
from typing import Dict, List, Type
from typing import TypeVar
from Market import Market

from MessageData import MessageData

### examples of abstract class https://www.pythontutorial.net/python-oop/python-abstract-class/
### @abstractclass meaning https://www.geeksforgeeks.org/classmethod-in-python/

class Fetcher(ABC):
    @abstractmethod
    def fetch(self) -> MessageData:
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
        """
        Args:
            api_key (str): the API key for the fetchers.
        """
        self._fetcher_list: Dict[str, Type[Fetcher]] = {}
        self._api_key = api_key

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], fetcher_dict: dict) -> T: 
        """
        Istantiate class from a dictionary.

        Args:
            fetcher_dict: A dictionary detailing which fetchers need to be instantiated.

        Returns:
            A cluster with the requested fetcher instantiated.
        """
        pass

    @abstractmethod
    def fetch_all(self) -> dict:
        """
        Fetch data with all the fetchers within this cluster.
        """
        pass

    @abstractmethod
    def add(self, fetcher: Type[Fetcher]) -> None:
        """
        Add a new fetcher to the cluster.

        Args:
            fetcher: the fetcher to be added to the cluster.
        """
        pass