import requests

with open('stockkey.txt') as f:
    alphavantage_key = f.read()


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=' + alphavantage_key
r = requests.get(url)
data = r.json()

#print(data)


### BITCOIN

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=BTC&market=USD&interval=5min&outputsize=full&apikey=' + alphavantage_key
r = requests.get(url)
data = r.json()

print(data)