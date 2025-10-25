"""Template extension package for Semantiva.

This package provides a comprehensive template for building domain-specific
Semantiva extensions with examples of all major component types.
"""

from semantiva.registry import SemantivaExtension
from semantiva.registry.processor_registry import ProcessorRegistry

# Import main components for convenient access
from . import data_types
from . import operations
from . import probes
from . import data_io
from . import context_processors


class TemplateExtension(SemantivaExtension):
    """Extension template with comprehensive component examples.

    This extension demonstrates all major Semantiva component types:
    - Data types (StringDataType, StringDataCollection)
    - Operations (string transformations)
    - Probes (string analysis)
    - Data I/O (file sources/sinks, payload sources/sinks)
    - Context processors (string processing, metadata addition)
    """

    def register(self) -> None:
        """Register all template extension modules with the ProcessorRegistry.

        The ProcessorRegistry.register_modules() method automatically imports each module,
        which triggers component registration via the SemantivaComponent metaclass.
        This ensures components are available for both pipeline resolution and
        doctor discovery.
        """
        ProcessorRegistry.register_modules(
            [
                "template_extension.data_types.data_types",
                "template_extension.operations.operations",
                "template_extension.probes.probes",
                "template_extension.data_io.data_io",
                "template_extension.context_processors.processors",
            ]
        )


__all__ = [
    "data_types",
    "operations",
    "probes",
    "data_io",
    "context_processors",
    "TemplateExtension",
]
