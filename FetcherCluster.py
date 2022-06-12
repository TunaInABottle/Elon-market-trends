from abc import ABC, abstractmethod

class FetcherClusters(ABC):
    def __init__(self, api_key, url) -> None:
        self._api_key = api_key
        self._url = url

    @abstractmethod
    def fetch(self) -> json:
        pass