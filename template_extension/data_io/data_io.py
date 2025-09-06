"""Domain-neutral data I/O for template extension."""

from pathlib import Path

from semantiva.data_io import DataSource, DataSink, PayloadSource, PayloadSink
from semantiva.pipeline import Payload
from semantiva.context_processors import ContextType
from template_extension.data_types import StringDataType


class StringDataSource(DataSource):
    """A DataSource that outputs a configurable string as StringDataType."""

    @classmethod
    def _get_data(cls, value: str = "Hello, World!") -> StringDataType:
        """Generate string data.

        Args:
            value: The string value to provide. Defaults to "Hello, World!".

        Returns:
            StringDataType: The string data wrapped in StringDataType.
        """
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        return StringDataType(value)

    @classmethod
    def output_data_type(cls):
        """Return the data type produced by this source."""
        return StringDataType


class StringFileDataSource(DataSource):
    """A DataSource that reads string data from a text file."""

    @classmethod
    def _get_data(cls, file_path: str) -> StringDataType:
        """Read string data from a file.

        Args:
            file_path: Path to the text file to read.

        Returns:
            StringDataType: The file contents wrapped in StringDataType.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If the file cannot be read.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            content = path.read_text(encoding="utf-8")
            return StringDataType(content)
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

    @classmethod
    def output_data_type(cls):
        """Return the data type produced by this source."""
        return StringDataType


class StringFileSink(DataSink[StringDataType]):
    """A DataSink that writes StringDataType data to a text file."""

    @classmethod
    def _send_data(cls, data: StringDataType, file_path: str):
        """Write string data to a file.

        Args:
            data: StringDataType containing the data to write.
            file_path: Path where to write the file.

        Raises:
            TypeError: If data is not a StringDataType.
            IOError: If the file cannot be written.
        """
        if not isinstance(data, StringDataType):
            raise TypeError("Data must be of type StringDataType")

        path = Path(file_path)
        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data.data, encoding="utf-8")
        except Exception as e:
            raise IOError(f"Failed to write file {file_path}: {e}")

    @classmethod
    def input_data_type(cls):
        """Return the data type accepted by this sink."""
        return StringDataType


class StringPayloadSource(PayloadSource):
    """A PayloadSource that provides string data with context."""

    @classmethod
    def _get_payload(
        cls, value: str = "Payload Content", context_key: str = "template.source"
    ) -> Payload:
        """Generate a payload with string data and context.

        Args:
            value: The string value to include in the payload.
            context_key: Key to use for injecting metadata into context.

        Returns:
            Payload: Contains StringDataType data and context with metadata.
        """
        context = ContextType()
        context.set_value(
            context_key,
            {
                "source": "StringPayloadSource",
                "timestamp": "example_timestamp",
                "content_length": len(value),
            },
        )

        return Payload(StringDataType(value), context)

    @classmethod
    def output_data_type(cls):
        """Return the data type contained in the payload."""
        return StringDataType

    @classmethod
    def _injected_context_keys(cls):
        """Return the keys of the context injected by the source."""
        return ["template.source"]


class StringPayloadSink(PayloadSink[StringDataType]):
    """A PayloadSink that processes string payloads and stores metadata."""

    @classmethod
    def _send_payload(cls, payload: Payload):
        """Process the payload and extract context information.

        Args:
            payload: Payload containing StringDataType data and context.
        """
        # In a stateless implementation, we would typically save to external storage
        # For this template example, we just validate the payload structure
        if not isinstance(payload.data, StringDataType):
            raise TypeError("Payload data must be of type StringDataType")

    @classmethod
    def input_data_type(cls):
        """Return the data type contained in the payload."""
        return StringDataType
