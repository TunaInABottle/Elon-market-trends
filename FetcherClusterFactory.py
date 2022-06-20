from AbstractFetcher import FetcherCluster
from AlphavantageAPI import AlphavantageFetcherCluster
from .config.setup_logger import fetch_log
from typing import Type

class FetcherClusterFactory():
    """ Factory of clusters of web fetchers. """

    @staticmethod
    def create(data_source: str, fetch_pools: dict) -> FetcherCluster:
        """
        Creates a cluster of web fetchers.

        Parameters:
            main_source: URL of the source to be fetched.
            fetch_pools: details on how to instantiate a cluster of web fetchers, it must contain main_souce as key.

        Returns:
            A cluster of web fetchers for the specified source.
        """

        data_sources = {
            "AlphaVantage": AlphavantageFetcherCluster,
            #"Twitter": TwitterFetcherCluster
        }

        if data_source not in data_sources:
            fetch_log.error(f"cluster_fetcher_factory: {data_source} is not in the list of clusters")
            raise KeyError
        if data_source not in fetch_pools:
            fetch_log.error(f"cluster_fetcher_factory: {data_source} is not in the list of sources that can be fetched")
            raise KeyError

        return data_sources[data_source].from_dict(fetch_pools[data_source])