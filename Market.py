from datetime import datetime
from MessageData import MessageData
import typing
import dateutil.parser as parser

T = typing.TypeVar('T', bound='Market')

class Market(MessageData):
    def __init__(self, datetime: datetime, open: str, high: str, low: str, close: str, volume: str, marketName: str = "") -> None:
        #super.__init__()
        self.datetime = datetime
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.marketName = marketName

    def to_repr(self) -> dict:
        return {
            "marketName": self.marketName,
            "datetime": self.datetime.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }

    @staticmethod
    def from_repr(raw_data: dict) -> T:
        return Market(
            raw_data["datetime"],
            raw_data["open"],
            raw_data["high"],
            raw_data["low"],
            raw_data["close"],
            raw_data["volume"],
            raw_data["marketName"]
        )

    @staticmethod
    def from_alphaVantage_repr(raw_data: dict, datetime: str, marketName: str = "") -> T:
        """Make a new object that holds the data given.

        Args:
            raw_data: a dictionary coming from a call to AlphaVantage API, needed to instantiate an object.

        Returns:
            An instantiated object.
        """
        return Market(
            parser.parse(datetime),
            raw_data["1. open"],
            raw_data["2. high"],
            raw_data["3. low"],
            raw_data["4. close"],
            raw_data["5. volume"],
            marketName
        )