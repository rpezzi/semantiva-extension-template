"""Domain-neutral probes for template extension."""

from semantiva.data_processors import DataProbe
from template_extension.data_types import StringDataType


class StringProbe(DataProbe):
    """Base class for probes that process StringDataType data."""

    @classmethod
    def input_data_type(cls):
        """Return the expected input data type for the probe."""
        return StringDataType


class StringAnalysisProbe(StringProbe):
    """A probe that analyzes StringDataType data and returns comprehensive metrics."""

    def _process_logic(self, data):
        """Analyze the string and return detailed metrics.

        Args:
            data: StringDataType containing the string to analyze.

        Returns:
            dict: Dictionary containing analysis results including length,
                  character counts, word counts, and content flags.
        """
        text = data.data
        return {
            "value": text,
            "length": len(text),
            "word_count": len(text.split()),
            "character_count": len(text),
            "uppercase_count": sum(1 for c in text if c.isupper()),
            "lowercase_count": sum(1 for c in text if c.islower()),
            "digit_count": sum(1 for c in text if c.isdigit()),
            "whitespace_count": sum(1 for c in text if c.isspace()),
            "is_empty": len(text) == 0,
            "is_numeric": text.isdigit() if text else False,
            "is_alphabetic": text.isalpha() if text else False,
            "has_uppercase": any(c.isupper() for c in text),
            "has_lowercase": any(c.islower() for c in text),
        }


class StringLengthProbe(StringProbe):
    """A simple probe that returns just the length of the string."""

    def _process_logic(self, data):
        """Return the length of the string.

        Args:
            data: StringDataType containing the string to measure.

        Returns:
            int: Length of the string.
        """
        return len(data.data)
