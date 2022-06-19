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
    """Represents a time-bounded trend of a market."""
    def __init__(self, datetime: datetime, open: str, high: str, low: str, close: str, volume: str) -> None:
        """
        Args:
            datetime: when the trend is happening.
            open: at which amount the market's trend opened.
            high: the highest the trend reached in a certain time span.
            low: the lowest the trend reached in a certain time span.
            close: at which amount the market's trend close.
            volume: number of transaction for this trend.
        """
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

    def __eq__(self, other: 'Trend') -> bool:
        if isinstance(other, Trend):
            return (
                self.datetime == other.datetime and
                self.open == other.open and
                self.high == other.high and
                self.low == other.low and
                self.close == other.close and
                self.volume == other.volume)
        return False


##########################

class Market(MessageData):
    """Representation of a market"""
    def __init__(self, name: str, type: MarketType) -> None:
        """
        Args:
            name: The name of the market.
            market_type: The type of market.
        """
        self.name = name
        self.type = type
        self.trend_list: List[Trend] = []

    def add(self, trends: List[Trend]) -> None:
        """Add a series of trends to the market
        
        Args:
            trends: trends to add to this Market
        """
        self.trend_list = self.trend_list + trends

    @staticmethod
    def from_repr(raw_data: dict) -> 'Market': #TODO check if works as expected
        new_market = Market( raw_data["marketName"], raw_data["type"] )

        [new_market.add(trend) for trend in raw_data["trends"]]

        return new_market

    def to_repr(self) -> dict:

        trends = [ trend.to_repr() for trend in self.trend_list ]

        return {
            "marketName": self.name,
            "type": self.type.name,
            "trends": trends
        }


##########################

class TrendBuilder:
    """Builder for instantiating new market trends."""
    @staticmethod
    def from_alphaVantage_repr(raw_data: dict, datetime: str) -> Trend:
        """Make a new Trend object from an AlphaVantage request.

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

