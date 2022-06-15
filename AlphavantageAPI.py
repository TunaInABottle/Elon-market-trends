from AbstractFetcher import Fetcher, FetcherCluster
from Market import Market
from MessageData import MessageData
from setup_logger import fetch_log
from typing import Dict, List, Type, TypeVar
import requests

T = TypeVar("T", bound="AlphavantageFetcherCluster")

#######

class AlphavantageFetcher(Fetcher):
    def __init__(self, api_key: str, type: str, market: str) -> None:
        super().__init__()
        self._api_key = api_key
        self._type = type
        self._market = market
        fetch_log.info(f"istantiated: {type} - {market}")

    def fetch(self) -> List[MessageData]: #@TODO should _type be more robust?
        r = requests.get( 'https://www.alphavantage.co/query?function=' + self._type + '_INTRADAY&symbol=' + self._market + '&market=USD&interval=5min&outputsize=full&apikey=' + self._api_key )
        return r.json()

    def get_characteristics(self) -> str:
        return f"{self._type} {self._market}"


#####

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


    def fetch_all(self) -> dict:

        ret_val = {}

        for key, fetcher in self._fetcher_dict.items():
            ret_val[key] = fetcher.fetch()

        return ret_val


    def add(self, fetcher: AlphavantageFetcher) -> None:
        self._fetcher_dict[fetcher.get_characteristics()] = fetcher