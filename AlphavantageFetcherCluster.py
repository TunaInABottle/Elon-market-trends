from AlphavantageFetcher import AlphavantageFetcher
from FetcherCluster import FetcherCluster
from setup_logger import fetch_log
from typing import Dict


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
                new_fetcher = AlphavantageFetcher( fetcher_dict["api_key"], api_req_type, market)
                cluster.add( new_fetcher )



    def fetch_all(self) -> str:
        pass


    #def add(self, fetcher: AlphavantageFetcher, market_type: str, market: str) -> None:
    #    if market_type not in self._fetcher_dict:
    #        self._fetcher_dict[market_type] = {}
    #        
    #    self._fetcher_dict[market_type][market] = fetcher


    def add(self, fetcher: AlphavantageFetcher) -> None:
        self._fetcher_dict[fetcher.get_characteristics()] = fetcher