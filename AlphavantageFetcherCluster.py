from AlphavantageFetcher import AlphavantageFetcher
from FetcherCluster import FetcherCluster
import json

from setup_logger import fetch_log


class AlphavantageFetcherCluster(FetcherCluster):
    """
    Cluster of web fetchers from AlphaVantage API.
    """

    def __init__(self, api_key: str) -> None:
        """
        Args:
            api_key (str): the API key for AlphaVantage.
        """
        self._fetcher_dict = {}
        self._api_key = api_key
        fetch_log.debug("istantiated")


    @classmethod
    def from_dict(cls, fetcher_dict: dict) -> None:
        cluster = cls(fetcher_dict["api_key"])

        for key, val in fetcher_dict.items():
            if key == "api_key": #no interest in the API key
                continue

            fetch_log.debug(val)
            api_req_type = val["url_name"]

            for market in val["markets"]: #iterate list of markets
                cluster.add( api_req_type, market )



    def fetch_all(self) -> json:
        pass


    def add(self, market_type: str, market: str) -> None:
        if market_type not in self._fetcher_dict:
            self._fetcher_dict[market_type] = {}
            
        self._fetcher_dict[market_type][market] = AlphavantageFetcher(self._api_key, market_type, market)