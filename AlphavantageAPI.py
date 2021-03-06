from time import sleep
from AbstractFetcher import Fetcher, FetcherCluster
from Market import Market, MarketType, Trend, TrendBuilder, MarketBuilder
from config.setup_logger import fetch_log
from typing import Dict, List, Type, TypeVar
import requests
from ProducerException import APILimitError

T = TypeVar("T", bound="AlphavantageFetcherCluster")

#######

class AlphavantageFetcher(Fetcher):
    """ Represent a fetcher on a specific AlphaVantage API."""

    def __init__(self, api_key: str, market_type: MarketType, market_name: str) -> None:
        """
        Args:
            api_key: API key for AlphaVantage.
            market_type: Which kind of market is being fetched.
            market_name: The name of the market (e.g. IBM).
        """
        super().__init__()
        self._api_key = api_key
        self.market_type = market_type #: Type of market
        self._url_type_req = self._request_type(market_type)
        self._market_name = market_name
        self._timespan = "30min"
        fetch_log.info(f"istantiated fetcher: {market_type} - {market_name}")

    def fetch(self) -> Market:
        """Fetch information from the Endpoint.

        Returns:
            A market object with the latest movements.

        """
        content = self._make_request()

        trends_list: List[Trend] = []

        fetch_log.debug(f"market: {self._market_name} keys: {content.keys()}")

        movement_list = None
        try:
            if self.market_type == MarketType.CRYPTO:
                movement_list = content['Time Series Crypto (' + self._timespan + ')']
            else: #stock market
                movement_list = content['Time Series (' + self._timespan + ')']
        except KeyError as ke:
            #fetch_log.error(f"there is no time series key in here: {content}\n {ke}")
            raise APILimitError(f"there is no time series key in here: {content}\n {ke}")

        for datetime, trend in movement_list.items():
            trends_list = trends_list + [TrendBuilder.from_alphaVantage_repr(trend, datetime)]

        market = MarketBuilder.from_alphaVantage_repr(self._market_name, self.market_type, trends_list)
        return market

    def _make_request(self):
        data = requests.get( 
            'https://www.alphavantage.co/query?function=' + self._url_type_req + 
            '_INTRADAY&symbol=' + self._market_name + 
            '&market=USD&interval=' + self._timespan + '&outputsize=full&apikey=' + self._api_key )

        content = data.json()

        if "Error Message" in content:
            err_mex = content["Error Message"]
            fetch_log.error(f"request failed: {err_mex}")
            raise KeyError

        return content

    def _request_type(self, market_type: MarketType) -> str:
        """Define the string depending on the market.

        Args:
            market_type: on which market make the decision.
        
        Returns:
            A string depending on the market.        

        Raises:
            KeyError if the market is not part of any of the expected ones.
        """
        if market_type == MarketType.CRYPTO:
            return "CRYPTO"
        elif market_type == MarketType.STOCK:
            return "TIME_SERIES"
        else:
            fetch_log.error(f"{market_type} does not belong to any of the expected markets!")
            raise KeyError

    def get_characteristics(self) -> str:
        """Write the characteristics of the market this fetcher is fetching.
        
        Returns:
            A string with the characteristics.
        """
        return f"{self.market_type.name}_{self._market_name}"

#######

class AlphavantageFetcherCluster(FetcherCluster):
    """Cluster of web fetchers from AlphaVantage API."""

    def __init__(self, api_key: str) -> None:
        self._fetcher_dict: Dict[str, AlphavantageFetcher] = {}
        self._api_key: str = api_key
        fetch_log.info("istantiated")

    @classmethod
    def from_dict(cls: Type[T], fetcher_dict: dict) -> T:
        """Istantiate a cluster of AlphaVantage Fetchers from a dictionary
        
        Args:
            fetcher_dict: A dictionary detailing which fetchers need to be instantiated.

        Returns:
            The AlphaVantage cluster with the requested fetcher instantiated.
        """
        cluster = cls(fetcher_dict["api_key"])

        for key, val in fetcher_dict.items(): #TODO more robust iteration?
            if key == "api_key": #no interest in the API key 
                continue

            fetch_log.debug(val)

            for market_name in val["markets"]: #iterate list of markets
                new_fetcher = AlphavantageFetcher( fetcher_dict["api_key"], key, market_name)
                cluster.add( new_fetcher )

        return cluster

    def fetch_all(self) -> Dict[str, Market]:
        """Fetch from all the fetchers connected to this cluster, pausing when the API limit is reached.

        Todo:
            Find a way to make this computation parallelizable.
            efficiency: do not fetch STOCK markets if current time not between american 4AM-8PM : https://www.alphavantage.co/documentation/

        Returns:
            A dictionary where for each key (a name of market) is associated its object representation.
        """
        ret_val = {}

        for key, fetcher in self._fetcher_dict.items():
            successful = False
            while not successful: 
                try:
                    ret_val[key] = fetcher.fetch()
                    successful = True
                except APILimitError:
                    fetch_log.info(f"Too many requests for the API, idling for 1 minute")
                    sleep(60)
                    fetch_log.info(f"Resuming...")

        return ret_val

    def add(self, fetcher: AlphavantageFetcher) -> None:
        """Add a fetcher to this cluster.

        Args:
            fetcher: the fetcher to be added.
        """
        self._fetcher_dict[fetcher.get_characteristics()] = fetcher