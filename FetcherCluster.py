from abc import ABC, abstractmethod
import json

class FetcherClusters(ABC):
    def __init__(self) -> None:
        self._fetcher_list = {}

    @abstractmethod
    def fetch_all(self) -> json:
        pass

    @abstractmethod
    def add(self) -> None:
        pass