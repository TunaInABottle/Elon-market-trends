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



def is_this_a_factory(source: str): # @TODO I have to answer this question
    if source == "Alphavantage":
        pass
        # @TODO cluster of fetcher, implementation: list where each fetch is identified by type of market and shortname (IMB, BTC, etc)