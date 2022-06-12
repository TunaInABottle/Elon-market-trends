from FetcherClusterFactory import FetcherClusterFactory

with open('stockkey.txt') as f:
    alphavantage_key = f.read()

markets_of_interest = {
    "AlphaVantage": {
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

markets_of_interest["AlphaVantage"]["api_key"] = alphavantage_key



FetcherClusterFactory.create("AlphaVantage", markets_of_interest)
FetcherClusterFactory.create("AlphaVanage", markets_of_interest)