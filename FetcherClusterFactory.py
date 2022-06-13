from FetcherCluster import FetcherCluster
from AlphavantageFetcherCluster import AlphavantageFetcherCluster
from setup_logger import fetch_log
from typing import Type

class FetcherClusterFactory():
    """ Factory of clusters of web fetchers. """

    @staticmethod
    def create(main_source: str, fetch_pools: dict) -> Type[FetcherCluster]:
        """
        Creates a cluster of web fetchers.

        Parameters:
            main_source (str): URL of the source to be fetched.
            fetch_pools (dict): details on how to instantiate a cluster of web fetchers, it must contain main_souce as key.

        Returns:
            A cluster of web fetchers for the specified source.
        """

        webSources = {
            "AlphaVantage": AlphavantageFetcherCluster,
            #"Twitter": TwitterFetcherCluster
        }

        if main_source not in webSources:
            fetch_log.error(f"cluster_fetcher_factory: {main_source} is not in the list of clusters")
            raise KeyError
        if main_source not in fetch_pools:
            fetch_log.error(f"cluster_fetcher_factory: {main_source} is not in the list of sources that can be fetched")
            raise KeyError

        return webSources[main_source].from_dict(fetch_pools[main_source])