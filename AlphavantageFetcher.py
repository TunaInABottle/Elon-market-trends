import logging
from Fetcher import Fetcher
import requests
import json


FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger('ph')


class AlphavantageFetcher(Fetcher):
    def __init__(self, api_key: str, url: str, type: str, market: str) -> None:
        super().__init__(api_key, url)
        self._type = type
        self._market = market

    def fetch(self) -> json:
        r = requests.get( 'https://www.alphavantage.co/query?function=' + self._type + '_INTRADAY&symbol=' + self._market + '&market=USD&interval=5min&outputsize=full&apikey=' + self._api_key )
        return r.json()





if __name__ == "__main__":

    with open('stockkey.txt') as f:
        alphavantage_key = f.read()


    #fetcherIBM = AlphavantageFetcher(alphavantage_key, "", "TIME_SERIES", "IBM")
    #print( fetcherIBM.fetch() )

    #print( "---" )

    fetcherBitcoin = AlphavantageFetcher(alphavantage_key, "", "CRYPTO", "BTC")
    print( fetcherBitcoin.fetch() )

