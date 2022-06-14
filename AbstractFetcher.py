from abc import ABC, abstractmethod
from typing import Dict, Type
from typing import TypeVar

### examples of abstract classhttps://www.pythontutorial.net/python-oop/python-abstract-class/
### @abstractclass meaning https://www.geeksforgeeks.org/classmethod-in-python/

class Fetcher(ABC):
    @abstractmethod
    def fetch(self) -> str:
        """ Obtain information.

        Returns:
        The information the fetcher is requested to fetch.
        """
        pass

    """"

    @property # says that the next function has to be read as a property 
    @abstractmethod
    def _url():
        raise NotImplementedError

    
    @property
    @abstractmethod
    def _api_key():
        raise NotImplementedError
    
    def print_constant(self):
        print(type(self)._url)
    """



########################


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