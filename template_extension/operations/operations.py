"""Domain-neutral operations for template extension."""

from semantiva.data_processors import DataOperation
from template_extension.data_types import StringDataType, StringDataCollection


class StringOperation(DataOperation):
    """Base class for operations on StringDataType data."""

    @classmethod
    def input_data_type(cls):
        """Return the expected input data type."""
        return StringDataType

    @classmethod
    def output_data_type(cls):
        """Return the produced output data type."""
        return StringDataType


class StringCollectionMergeOperation(DataOperation):
    """Base class for operations that merge StringDataCollection into a single StringDataType."""

    @classmethod
    def input_data_type(cls):
        """Return the expected collection input type."""
        return StringDataCollection

    @classmethod
    def output_data_type(cls):
        """Return the merged output data type."""
        return StringDataType


class StringUppercaseOperation(StringOperation):
    """Convert StringDataType data to uppercase."""

    def _process_logic(self, data):
        """Convert the string to uppercase.

        Args:
            data: StringDataType containing the input string.

        Returns:
            StringDataType: New instance with uppercase string.
        """
        return StringDataType(data.data.upper())


class StringLowercaseOperation(StringOperation):
    """Convert StringDataType data to lowercase."""

    def _process_logic(self, data):
        """Convert the string to lowercase.

        Args:
            data: StringDataType containing the input string.

        Returns:
            StringDataType: New instance with lowercase string.
        """
        return StringDataType(data.data.lower())


class StringConcatenateOperation(StringOperation):
    """Concatenate StringDataType data with a suffix."""

    def _process_logic(self, data, suffix: str):
        """Concatenate the string with a suffix.

        Args:
            data: StringDataType containing the input string.
            suffix: String to append.

        Returns:
            StringDataType: New instance with concatenated string.
        """
        return StringDataType(data.data + suffix)


class StringCollectionJoinOperation(StringCollectionMergeOperation):
    """Join all items in a StringDataCollection with a separator."""

    def _process_logic(self, data, separator: str = " "):
        """Join all strings in the collection.

        Args:
            data: StringDataCollection containing input strings.
            separator: String to use as separator between elements.

        Returns:
            StringDataType: New instance with joined string.
        """
        strings = [item.data for item in data.data]
        joined = separator.join(strings)
        return StringDataType(joined)
