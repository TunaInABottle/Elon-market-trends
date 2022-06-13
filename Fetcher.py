from abc import ABC, abstractmethod
import json


### examples of abstract classhttps://www.pythontutorial.net/python-oop/python-abstract-class/
### @abstractclass meaning https://www.geeksforgeeks.org/classmethod-in-python/

class Fetcher(ABC):
    #def __init__(self, api_key: str) -> None:
    #    self._api_key = api_key

    @abstractmethod
    def fetch(self) -> json:
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
