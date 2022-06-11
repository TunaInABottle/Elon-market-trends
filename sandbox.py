from AlphavantageFetcher import AlphavantageFetcher


markets_of_interest = {
    "Alphavantage": {
        "Stock": {
            "url_name": "TIME_SERIES",
            "markets": ["IBM"]
        },
        "Crypto": {
            "url_name": "CRYPTO",
            "markets": ["BTC", "DOGE"]

        }
    }
}


for url_src, markets_info in markets_of_interest.items():
    print(url_src)



def cluster_fetcher_factory(main_source: str, sub_sources: dict) -> FetcherCluster: # @TODO Make a factory of clusters of fetchers, take as parameter the above dictionary and its key

    webSources = {
        "AlphaVantage": AlphavantageFetcherCluster,
        "Twitter": TwitterFetcherCluster
    }

    if main_source not in webSources: # @TODO does this check works?
        raise Exception(f"cluster_fetcher_factory: {main_source} is not in the list")

    return webSources[main_source](sub_sources)