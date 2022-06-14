from AlphavantageFetcher import AlphavantageFetcher
from FetcherCluster import FetcherCluster
from setup_logger import fetch_log
from typing import Dict, Type, TypeVar

T = TypeVar("T", bound="AlphavantageFetcherCluster")

class AlphavantageFetcherCluster(FetcherCluster):
    """
    Cluster of web fetchers from AlphaVantage API.
    """

    def __init__(self, api_key: str) -> None:
        """
        Args:
            api_key (str): the API key for AlphaVantage.
        """
        self._fetcher_dict: Dict[str, AlphavantageFetcher] = {}
        self._api_key: str = api_key
        fetch_log.debug("istantiated")


    @classmethod
    def from_dict(cls: Type[T], fetcher_dict: dict) -> T:
        cluster = cls(fetcher_dict["api_key"])

        for key, val in fetcher_dict.items():
            if key == "api_key": #no interest in the API key
                continue

            fetch_log.debug(val)
            api_req_type = val["url_name"]

            for market in val["markets"]: #iterate list of markets
                new_fetcher = AlphavantageFetcher( fetcher_dict["api_key"], api_req_type, market)
                cluster.add( new_fetcher )

        return cluster


    # def add_from_dict(self, fetcher_dict: dict) -> None:

    #     for key, val in fetcher_dict.items():
    #         if key == "api_key": #no interest in the API key
    #             continue

    #         fetch_log.debug(val)
    #         api_req_type = val["url_name"]

    #         for market in val["markets"]: #iterate list of markets
    #             new_fetcher = AlphavantageFetcher( self._api_key, api_req_type, market)
    #             self._fetcher_dict[new_fetcher.get_characteristics()] = new_fetcher


    def fetch_all(self) -> str:
        for key, val in self._fetcher_dict.items():
            fetch_log.debug( val.fetch() )

        return "" #@TODO


    def add(self, fetcher: AlphavantageFetcher) -> None:
        self._fetcher_dict[fetcher.get_characteristics()] = fetcher