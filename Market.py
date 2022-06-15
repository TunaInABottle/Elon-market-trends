from datetime import datetime

from MessageData import MessageData
import typing
from typing import List
import dateutil.parser as parser
import enum

T = typing.TypeVar('T', bound='Trend')

##########################
 
class MarketType(enum.Enum):
    STOCK = 1
    CRYPTO = 2

##########################

class Trend(MessageData):
    def __init__(self, datetime: datetime, open: str, high: str, low: str, close: str, volume: str) -> None:
        self.datetime = datetime
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def to_repr(self) -> dict:
        return {
            "datetime": self.datetime.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }

    @staticmethod
    def from_repr(raw_data: dict) -> 'Trend':
        return Trend(
            raw_data["datetime"],
            raw_data["open"],
            raw_data["high"],
            raw_data["low"],
            raw_data["close"],
            raw_data["volume"]
        )


##########################

class Market(MessageData):
    """Representation of a market"""
    def __init__(self, name: str, type: MarketType) -> None:
        """
        Args:
            name (str): The name of the market.
            market_type (MarketType): The type of market.
        """
        self.name = name
        self.type = type
        self._trend_list: List[Trend] = []

    def add(self, trends: List[Trend]) -> None:
        """Add a series of trends to the market
        
        Args:
            trends (List[Trend]): trends to add to this Market
        """
        self._trend_list = self._trend_list + trends

    def from_repr(self):
        pass #TODO

    def to_repr(self) -> dict:
        pass #TODO


##########################

class TrendBuilder:
    @staticmethod
    def from_alphaVantage_repr(raw_data: dict, datetime: str, marketName: str = "") -> Trend:
        """Make a new object that holds the data given.

        Args:
            raw_data: a dictionary coming from a call to AlphaVantage API, needed to instantiate an object.

        Returns:
            An instantiated object.
        """
        return Trend(
            parser.parse(datetime),
            raw_data["1. open"],
            raw_data["2. high"],
            raw_data["3. low"],
            raw_data["4. close"],
            raw_data["5. volume"]
        )

