"""Domain-neutral data types for template extension."""

from typing import Iterator
from semantiva.data_types import BaseDataType, DataCollectionType


class StringDataType(BaseDataType[str]):
    """A simple data type that holds a string value.

    This serves as an example of how to implement BaseDataType
    for your domain-specific data.
    """

    def validate(self, data: str) -> bool:
        """Validate that data is a string.

        Args:
            data: Value to validate.

        Returns:
            bool: True if the value is a string.

        Raises:
            TypeError: If data is not a string.
        """
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        return True


class StringDataCollection(DataCollectionType[StringDataType, list]):
    """A collection of StringDataType objects.

    This serves as an example of how to implement DataCollectionType
    for your domain-specific collections.
    """

    @classmethod
    def _initialize_empty(cls) -> list:
        """Initialize an empty collection container."""
        return []

    def __iter__(self) -> Iterator[StringDataType]:
        """Iterate over the string data elements."""
        return iter(self._data)

    def append(self, item: StringDataType) -> None:
        """Append a StringDataType item to the collection.

        Args:
            item: The StringDataType element to add to the collection.

        Raises:
            TypeError: If item is not a StringDataType instance.
        """
        if not isinstance(item, StringDataType):
            raise TypeError("Item must be of type StringDataType")
        self._data.append(item)

    def __len__(self) -> int:
        """Return the number of items in the collection."""
        return len(self._data)

    def validate(self, data):
        """Validate that all items in the collection are StringDataType instances.

        Args:
            data: The collection to validate.

        Raises:
            TypeError: If any element is not a StringDataType instance.
        """
        for item in data:
            if not isinstance(item, StringDataType):
                raise TypeError("Data must be a list of StringDataType objects")
