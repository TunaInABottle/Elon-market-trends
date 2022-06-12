from enum import Enum

class MarketType(Enum):
    STOCK = "TIME_SERIES"
    CRYPTO = "CRYPTO"

    def __str__(self) -> str:
        return str(self.value)




#print(MarketType.STOCK)