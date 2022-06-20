from abc import ABC, abstractmethod
import typing
from typing import Type

T = typing.TypeVar('T', bound='MessageData') #source https://stackoverflow.com/questions/58986031/type-hinting-child-class-returning-self

class MessageData(ABC):
    """Abstract class for generic data that need to be shared through a pipeline"""
    def __init__(self) -> None:
        self.is_data = True

    @abstractmethod
    def to_repr(self) -> dict:
        """Convert the parameters stored in this class into a dictionary.

        Returns:
            A dictionary with the data of this object.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_repr(raw_data: dict) -> 'MessageData':
        """Make a new object that holds the data given.

        Args:
            raw_data: a dictionary that has the data needed to instantiate an object.

        Returns:
            An instantiated object with this type.
        """
        pass

    @abstractmethod
    def __eq__(self, other: 'MessageData') -> bool:
        pass