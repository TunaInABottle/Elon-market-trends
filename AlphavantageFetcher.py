import logging
from Fetcher import Fetcher
import requests
import json

from setup_logger import fetch_log


class AlphavantageFetcher(Fetcher):
    def __init__(self, api_key: str, type: str, market: str) -> None:
        super().__init__()
        self._api_key = api_key
        self._type = type
        self._market = market
        fetch_log.debug(f"istantiated: {type} - {market}")

    def fetch(self) -> str: #@TODO should _type be more robust?
        r = requests.get( 'https://www.alphavantage.co/query?function=' + self._type + '_INTRADAY&symbol=' + self._market + '&market=USD&interval=5min&outputsize=full&apikey=' + self._api_key )
        return r.json()

    def get_characteristics(self) -> str:
        return f"{self._type} {self._market}"


###############


if __name__ == "__main__":

    with open('./config/AlphaVantageKey.txt') as f:
        alphavantage_key = f.read()


    #fetcherIBM = AlphavantageFetcher(alphavantage_key, "TIME_SERIES", "IBM")
    #print( fetcherIBM.fetch() )

    #print( "---" )

    fetcherBitcoin = AlphavantageFetcher(alphavantage_key, "CRYPTO", "BTC")
    print( fetcherBitcoin.fetch() )

