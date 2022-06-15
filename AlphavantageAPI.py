from AbstractFetcher import Fetcher, FetcherCluster
from Market import Market, MarketType, Trend, TrendBuilder
from MessageData import MessageData
from setup_logger import fetch_log
from typing import Dict, List, Type, TypeVar
import requests

T = TypeVar("T", bound="AlphavantageFetcherCluster")

#######

class AlphavantageFetcher(Fetcher):
    def __init__(self, api_key: str, market_type: MarketType, market_name: str) -> None:
        super().__init__()
        self._api_key = api_key
        self.market_type = market_type
        self._url_type_req = self.request_type(market_type)
        self._market_name = market_name
        fetch_log.info(f"istantiated: {market_type} - {market_name}")

    def fetch(self) -> Market: #@TODO should _type be more robust?
        #try:
        r = requests.get( 'https://www.alphavantage.co/query?function=' + self._url_type_req + 
            '_INTRADAY&symbol=' + self._market_name + 
            '&market=USD&interval=5min&outputsize=full&apikey=' + self._api_key )
        #except:


        content = r.json()

        trends_list: List[Trend] = []

        movement_list = None
        if self.market_type == MarketType.CRYPTO:
            movement_list = content['Time Series Crypto (5min)']
        else: #stock market
            movement_list = content['Time Series (5min)']
            


        for datetime, trend in movement_list.items():
            trends_list = trends_list + [TrendBuilder.from_alphaVantage_repr(trend, datetime, self._market_name)]

        market = Market(self._market_name, self.market_type)
        market.add(trends_list)
        return market

    def request_type(self, market_type: MarketType) -> str:
        if market_type == MarketType.CRYPTO:
            return "CRYPTO"
        elif market_type == MarketType.STOCK:
            return "TIME_SERIES"
        else:
            fetch_log.error(f"{market_type} does not belong to any of the expected markets!")
            raise KeyError

    def get_characteristics(self) -> str:
        return f"{self.market_type} {self._market_name}"


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
        fetch_log.info("istantiated")


    @classmethod
    def from_dict(cls: Type[T], fetcher_dict: dict) -> T:
        cluster = cls(fetcher_dict["api_key"])

        for key, val in fetcher_dict.items():
            if key == "api_key": #no interest in the API key
                continue

            fetch_log.debug(val)
            api_req_type = val["url_name"]

            for market_name in val["markets"]: #iterate list of markets
                new_fetcher = AlphavantageFetcher( fetcher_dict["api_key"], key, market_name)
                cluster.add( new_fetcher )

        return cluster


    def fetch_all(self) -> dict: #Dict[str, List[Market]]

        ret_val = {}

        for key, fetcher in self._fetcher_dict.items():
            ret_val[key] = fetcher.fetch()

        return ret_val


    def add(self, fetcher: AlphavantageFetcher) -> None:
        self._fetcher_dict[fetcher.get_characteristics()] = fetcher