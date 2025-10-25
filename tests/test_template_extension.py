"""Tests for template extension pipeline functionality."""

from pathlib import Path
import tempfile


def test_template_extension_components():
    """Test that all template extension components can be imported and instantiated."""

    # Test data types
    from template_extension.data_types import StringDataType, StringDataCollection

    # Test basic data type functionality
    string_data = StringDataType("test string")
    assert string_data.data == "test string"

    # Test collection functionality
    collection = StringDataCollection()
    collection.append(string_data)
    collection.append(StringDataType("second string"))
    assert len(collection) == 2

    # Test operations
    from template_extension.operations import (
        StringUppercaseOperation,
        StringConcatenateOperation,
    )

    upper_op = StringUppercaseOperation()
    result = upper_op._process_logic(string_data)
    assert result.data == "TEST STRING"

    concat_op = StringConcatenateOperation()
    result = concat_op._process_logic(string_data, " suffix")
    assert result.data == "test string suffix"

    # Test probes
    from template_extension.probes import StringAnalysisProbe, StringLengthProbe

    analysis_probe = StringAnalysisProbe()
    analysis = analysis_probe._process_logic(string_data)
    assert analysis["length"] == 11
    assert analysis["word_count"] == 2

    length_probe = StringLengthProbe()
    length = length_probe._process_logic(string_data)
    assert length == 11

    # Test data I/O
    from template_extension.data_io import StringDataSource

    source = StringDataSource()
    data = source._get_data("custom value")
    assert data.data == "custom value"


def test_template_extension_context_processors():
    """Test template extension context processors."""

    from template_extension.context_processors import (
        EchoContextProcessor,
        MetadataContextProcessor,
    )
    from semantiva.context_processors.context_observer import _ContextObserver
    from semantiva.context_processors.context_types import ContextType

    # Test echo processor
    echo_processor = EchoContextProcessor()
    context = ContextType()
    observer = _ContextObserver()

    _ = echo_processor.operate_context(
        context=context, context_observer=observer, message="test message"
    )
    assert observer.observer_context.get_value("template.echo") == {
        "message": "test message"
    }

    # Test metadata processor
    metadata_processor = MetadataContextProcessor()
    _ = metadata_processor.operate_context(
        context=context,
        context_observer=observer,
        include_timestamp=True,
        include_stats=True,
        custom_metadata={"test": "value"},
    )

    metadata = observer.observer_context.get_value("template.metadata")
    assert "timestamp" in metadata
    assert "context_stats" in metadata
    assert metadata["custom"]["test"] == "value"
    assert metadata["processor"]["name"] == "MetadataContextProcessor"


def test_template_extension_file_io():
    """Test file-based data I/O components."""

    from template_extension.data_io import StringFileDataSource, StringFileSink
    from template_extension.data_types import StringDataType

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test file writing
        test_file = Path(temp_dir) / "test.txt"
        test_data = StringDataType("Test file content\nWith multiple lines")

        sink = StringFileSink()
        sink._send_data(test_data, str(test_file))

        # Verify file was created and has correct content
        assert test_file.exists()
        content = test_file.read_text()
        assert content == "Test file content\nWith multiple lines"

        # Test file reading
        source = StringFileDataSource()
        loaded_data = source._get_data(str(test_file))
        assert loaded_data.data == "Test file content\nWith multiple lines"
        assert isinstance(loaded_data, StringDataType)


def test_template_extension_payload_components():
    """Test payload-based data I/O components."""

    from template_extension.data_io import StringPayloadSource, StringPayloadSink

    # Test payload source
    payload_source = StringPayloadSource()
    payload = payload_source._get_payload("test payload content", "template.custom")

    assert payload.data.data == "test payload content"
    assert (
        payload.context.get_value("template.custom")["source"] == "StringPayloadSource"
    )
    assert payload.context.get_value("template.custom")["content_length"] == 20

    # Test payload sink
    StringPayloadSink.send_payload(payload)


def test_extension_registration():
    """Test that the extension can be registered and discovered."""

    from template_extension import TemplateExtension
    from semantiva.registry.processor_registry import ProcessorRegistry

    # Create extension instance
    extension = TemplateExtension()

    # Test that register method exists and can be called
    extension.register()  # Should not raise any exceptions

    # Test that some components are now available through ProcessorRegistry
    # Note: This test verifies the registration pattern works
    registered_modules = ProcessorRegistry.registered_modules()
    expected_modules = [
        "template_extension.data_types.data_types",
        "template_extension.operations.operations",
        "template_extension.probes.probes",
        "template_extension.data_io.data_io",
        "template_extension.context_processors.processors",
    ]

    for module in expected_modules:
        assert module in registered_modules


if __name__ == "__main__":
    # Run a simple smoke test
    test_template_extension_components()
    test_template_extension_context_processors()
    test_template_extension_file_io()
    test_template_extension_payload_components()
    test_extension_registration()
    print("All tests passed!")
