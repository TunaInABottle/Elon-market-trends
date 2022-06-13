from abc import ABC, abstractmethod
from typing import Dict, Type
from AlphavantageFetcher import AlphavantageFetcher
from Fetcher import Fetcher




class supper(ABC):


    @abstractmethod
    def add(self, fetcher: Type[Fetcher]) -> None:
        pass




class subclass(supper):
    def __init__(self) -> None:
        pass


    def add(self, fetcher: AlphavantageFetcher) -> None:
        pass



ara = subclass()

ara.add(AlphavantageFetcher("ara","ara","ara"))

print( issubclass(AlphavantageFetcher, Fetcher) )