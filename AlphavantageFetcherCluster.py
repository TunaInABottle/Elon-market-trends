from FetcherCluster import FetcherCluster
import json


class AlphavantageFetcherCluster(FetcherCluster):
    def __init__(self, api_key: str) -> None:
        self._fetcher_list = {}
        self._api_key = api_key
        print("AlphavantageFetcherCluster istantiated")


    @classmethod
    def from_dict(cls, api_key: str, fetcher_init_dict: dict): # -> FetcherCluster:
            #cluster = cls(api_key)
            # add each fetcher into cluster
            #return cluster
            pass


    def fetch_all(self) -> json:
        pass


    def add(self) -> None:
        pass