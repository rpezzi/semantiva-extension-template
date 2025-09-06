"""Domain-neutral context processors for template extension."""

from typing import List, Optional

from semantiva.logger import Logger
from semantiva.context_processors.context_processors import ContextProcessor


class EchoContextProcessor(ContextProcessor):
    """
    Minimal domain-free example that writes a message into the context.
    """

    CONTEXT_OUTPUT_KEY = "template.echo"

    def __init__(self, logger: Optional[Logger] = None):
        super().__init__(logger)

    def _process_logic(self, *, message: str) -> None:
        """Store the provided message in the context.

        Args:
            message: The message to store in the context.
        """
        self._notify_context_update(self.CONTEXT_OUTPUT_KEY, {"message": message})

    @classmethod
    def context_keys(cls) -> List[str]:
        return [cls.CONTEXT_OUTPUT_KEY]


class MetadataContextProcessor(ContextProcessor):
    """A context processor that adds metadata information to the context.

    This demonstrates how to create processors that enrich context with
    computational metadata, timestamps, or derived information.
    """

    CONTEXT_OUTPUT_KEY = "template.metadata"

    def __init__(self, logger: Optional[Logger] = None):
        super().__init__(logger)

    def _process_logic(
        self,
        *,
        include_timestamp: bool = True,
        include_stats: bool = True,
        custom_metadata: Optional[dict] = None,
    ) -> None:
        """Add metadata information to the context.

        Args:
            include_timestamp: Whether to include a timestamp.
            include_stats: Whether to include context statistics.
            custom_metadata: Additional custom metadata to include.
        """
        metadata: dict = {}

        if include_timestamp:
            import datetime

            metadata["timestamp"] = datetime.datetime.now().isoformat()

        if include_stats:
            # For now, we'll add basic processor info since context stats
            # are harder to access in _process_logic
            metadata["context_stats"] = {
                "processor_active": True,
            }

        if custom_metadata:
            metadata["custom"] = custom_metadata

        # Add processor information
        metadata["processor"] = {
            "name": self.__class__.__name__,
            "version": "1.0.0",
        }

        # Store metadata in context
        self._notify_context_update(self.CONTEXT_OUTPUT_KEY, metadata)

    @classmethod
    def context_keys(cls) -> List[str]:
        """Return list of context keys created by this processor."""
        return [cls.CONTEXT_OUTPUT_KEY]
