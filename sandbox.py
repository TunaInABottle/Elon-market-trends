# from abc import ABC, abstractmethod
# from typing import Generic, Type, TypeVar


# class Fetcher(ABC):
#     @abstractmethod
#     def ara(self):
#         pass

# class FetcherCluster(ABC):
#     @abstractmethod
#     def fetch_all(self, fec: Type[Fetcher]):
#         pass

# #############

# class AlphaFetcher(Fetcher):
#     def ara(self):
#         pass

# class AlphaFetcherCluster(FetcherCluster):
#     def fetch_all(self, fec: AlphaFetcher):
#         pass


# r = AlphaFetcherCluster()

# print( Type[Fetcher] )
# print( issubclass(AlphaFetcher, Fetcher) )
# print( isinstance( AlphaFetcher(), Fetcher ))

###########################

# from dotenv import load_dotenv
# import os

# load_dotenv("./.env")

# print( os.getenv("API_KEY") )

from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)
for j in range(9999):
    print("Iteration", j)
    data = {'counter': j}
    producer.send('pizza', value=data)
    sleep(5)