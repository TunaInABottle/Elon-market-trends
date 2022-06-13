from abc import ABC, abstractmethod
import typing

T = typing.TypeVar('T', bound='MessageData') #source https://stackoverflow.com/questions/58986031/type-hinting-child-class-returning-self

class MessageData(ABC):
    def __init__(self) -> None:
        self.is_data = True

    @abstractmethod
    def to_repr(self) -> dict:
        """Convert the parameters stored in this class into a dictionary.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            A dictionary with the data of this object.
        """
        pass


    @abstractmethod
    @staticmethod
    def from_repr(raw_data: dict) -> T:
        """Make a new object that holds the data given.

        Args:
            raw_data: a dictionary that has the data needed to instantiate an object.

        Returns:
            An instantiated object.
        """
        pass