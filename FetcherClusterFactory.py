from FetcherCluster import FetcherCluster
from AlphavantageFetcherCluster import AlphavantageFetcherCluster

class FetcherClusterFactory():
    @staticmethod
    def create(main_source: str, fetch_pools: dict) -> FetcherCluster: # @TODO Make a factory of clusters of fetchers, take as parameter the above dictionary and its key

        webSources = {
            "AlphaVantage": AlphavantageFetcherCluster,
            #"Twitter": TwitterFetcherCluster
        }

        if main_source not in webSources:
            raise Exception(f"cluster_fetcher_factory: {main_source} is not in the list of the clusters")
        if main_source not in fetch_pools:
            raise Exception(f"cluster_fetcher_factory: {main_source} is not in the list of sources that can be fetched")


        return webSources[main_source](fetch_pools[main_source])