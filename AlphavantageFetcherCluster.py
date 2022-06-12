from FetcherCluster import FetcherCluster


class AlphavantageFetcherCluster(FetcherCluster):
    def __init__(self, api_key: str, url: str, type: str, market: str) -> None:
        super().__init__(api_key, url)
        self._type = type
        self._market = market