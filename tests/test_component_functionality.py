"""
Comprehensive functional tests for all template extension components.

This file demonstrates and validates the exact behavior of each component
in the template extension. It serves as both test validation and usage examples
for developers adapting this template.

Each test focuses on a single component and verifies its core functionality.
Context processors are tested via pipeline execution since they require
pipeline context to function properly.
"""

import pytest
import tempfile
import os

from semantiva import ContextType
from semantiva import Pipeline, load_pipeline_from_yaml

# Import all template components
from template_extension.data_types import StringDataType, StringDataCollection
from template_extension.operations import (
    StringUppercaseOperation,
    StringLowercaseOperation,
    StringConcatenateOperation,
    StringCollectionJoinOperation,
)
from template_extension.probes import StringAnalysisProbe, StringLengthProbe
from template_extension.data_io import (
    StringDataSource,
    StringFileDataSource,
    StringFileSink,
    StringPayloadSource,
    StringPayloadSink,
)


class TestDataTypes:
    """Test data type validation and behavior."""

    def test_string_data_type_validation(self):
        """StringDataType accepts strings and rejects non-strings."""
        data = StringDataType("abc")

        # Valid strings
        assert data.data == "abc"

    def test_string_collection_validation(self):
        """StringDataCollection accepts lists of strings."""
        collection_type = StringDataCollection._initialize_empty()
        collection_type.append(StringDataType("single"))
        collection_type.append(StringDataType("another"))

        # Valid collections
        assert collection_type[0].data == "single"
        assert collection_type[1].data == "another"


class TestOperations:
    """Test data transformation operations."""

    def test_string_uppercase_operation(self):
        """StringUppercaseOperation converts strings to uppercase."""
        operation = StringUppercaseOperation()

        result = operation.run(StringDataType("hello world"))
        assert result.data == "HELLO WORLD"

        result = operation.run(StringDataType("MiXeD cAsE"))
        assert result.data == "MIXED CASE"

    def test_string_lowercase_operation(self):
        """StringLowercaseOperation converts strings to lowercase."""
        operation = StringLowercaseOperation()

        result = operation.run(StringDataType("HELLO WORLD"))
        assert result.data == "hello world"

        result = operation.run(StringDataType("MiXeD cAsE"))
        assert result.data == "mixed case"

    def test_string_concatenate_operation(self):
        """StringConcatenateOperation joins two strings with space."""
        operation = StringConcatenateOperation()

        result = operation.run(StringDataType("hello"), suffix=" world")
        assert result.data == "hello world"

        result = operation.run(StringDataType(" "), suffix="test")
        assert result.data == " test"

    def test_string_collection_join_operation(self):
        """StringCollectionJoinOperation joins string lists with commas."""
        operation = StringCollectionJoinOperation()

        result = operation.run(
            StringDataCollection(
                [
                    StringDataType("apple"),
                    StringDataType("banana"),
                    StringDataType("cherry"),
                ]
            )
        )
        assert result.data == "apple banana cherry"

        result = operation.run(StringDataCollection([StringDataType("single")]))
        assert result.data == "single"

        result = operation.run(StringDataCollection([]))
        assert result.data == ""


class TestProbes:
    """Test data analysis probes."""

    def test_string_analysis_probe(self):
        """StringAnalysisProbe extracts detailed string metrics."""

        result = StringAnalysisProbe.run(StringDataType("Hello World!"))
        expected = {
            "value": "Hello World!",
            "length": 12,
            "word_count": 2,
            "character_count": 12,
            "uppercase_count": 2,
            "lowercase_count": 8,
            "digit_count": 0,
            "whitespace_count": 1,
            "is_empty": False,
            "is_numeric": False,
            "is_alphabetic": False,
            "has_uppercase": True,
            "has_lowercase": True,
        }
        assert result == expected

    def test_string_length_probe(self):
        """StringLengthProbe returns string length."""

        assert StringLengthProbe.run(StringDataType("hello")) == 5
        assert StringLengthProbe.run(StringDataType("")) == 0
        assert StringLengthProbe.run(StringDataType("a" * 100)) == 100


class TestDataIO:
    """Test data input/output components."""

    def test_string_data_source(self):
        """StringDataSource generates configured string data."""
        source = StringDataSource()

        result = source.get_data("test string")
        assert result.data == "test string"

    def test_string_file_data_source(self):
        """StringFileDataSource reads from file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("File content test")
            temp_path = f.name

        try:
            source = StringFileDataSource()
            result = source.get_data(file_path=temp_path)
            assert result.data == "File content test"
        finally:
            os.unlink(temp_path)

    def test_string_file_sink(self):
        """StringFileSink writes data to file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            sink = StringFileSink()
            sink.send_data(StringDataType("test output"), file_path=temp_path)

            # Verify file content
            with open(temp_path, "r") as f:
                content = f.read()
            assert content == "test output"
        finally:
            os.unlink(temp_path)

    def test_string_payload_source(self):
        """StringPayloadSource extracts string from context payload."""
        context = ContextType()
        context.set_value("payload.message", "payload test")

        source = StringPayloadSource()
        result = source.get_payload("payload test", "my_key")
        assert result.data.data == "payload test"
        assert result.context.get_value("my_key") == {
            "content_length": 12,
            "source": "StringPayloadSource",
            "timestamp": "example_timestamp",
        }

    def test_string_payload_sink(self):
        """StringPayloadSink processes string payloads statelessly."""
        from semantiva.pipeline import Payload

        # Create proper payload
        data = StringDataType("test content")
        context = ContextType()
        payload = Payload(data, context)

        # Since the sink is stateless, we just verify it doesn't raise an exception
        StringPayloadSink.send_payload(payload)


class TestContextProcessorsViaPipeline:
    """Test context processors through pipeline execution."""

    def test_echo_context_processor_pipeline(self):
        """EchoContextProcessor adds echo metadata via pipeline."""
        pipeline_yaml = """
        extensions: ["template_extension"]
        pipeline:
          nodes:
            - processor: EchoContextProcessor
              parameters:
                message: "Pipeline executed successfully"
            - processor: StringDataSource
              parameters:
                data: "test data"
            - processor: StringFileSink
              parameters:
                file_path: "/tmp/test_echo_output.txt"
        """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(pipeline_yaml)
            config_path = f.name

        try:
            config = load_pipeline_from_yaml(config_path)
            pipeline = Pipeline(config)
            context = pipeline.process().context

            # Verify echo metadata was added
            echo_data = context.get_value("template.echo")
            assert echo_data == {"message": "Pipeline executed successfully"}

        finally:
            os.unlink(config_path)
            if os.path.exists("/tmp/test_echo_output.txt"):
                os.unlink("/tmp/test_echo_output.txt")

    def test_string_context_processor_pipeline(self):
        """Test a simple pipeline with context processor metadata."""
        pipeline_yaml = """
        extensions: ["template_extension"]
        pipeline:
          nodes:
            - processor: MetadataContextProcessor
              parameters:
                include_timestamp: true
                include_stats: false
            - processor: StringDataSource
              parameters:
                data: "test data"
            - processor: StringFileSink
              parameters:
                file_path: "/tmp/test_string_output.txt"
        """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(pipeline_yaml)
            config_path = f.name

        try:
            config = load_pipeline_from_yaml(config_path)
            pipeline = Pipeline(config)
            context = pipeline.process().context

            # Verify metadata was added
            metadata = context.get_value("template.metadata")
            assert "timestamp" in metadata
            assert metadata["processor"]["name"] == "MetadataContextProcessor"

        finally:
            os.unlink(config_path)
            if os.path.exists("/tmp/test_string_output.txt"):
                os.unlink("/tmp/test_string_output.txt")

    def test_metadata_context_processor_pipeline(self):
        """MetadataContextProcessor adds execution metadata via pipeline."""
        pipeline_yaml = """
        extensions: ["template_extension"]
        pipeline:
          nodes:
            - processor: MetadataContextProcessor
              parameters:
                include_timestamp: true
                include_stats: true
                custom_metadata:
                  operation: "test_operation"
                  version: "1.0"
            - processor: StringDataSource
              parameters:
                data: "test data"
            - processor: StringFileSink
              parameters:
                file_path: "/tmp/test_metadata_output.txt"
        """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(pipeline_yaml)
            config_path = f.name

        try:
            config = load_pipeline_from_yaml(config_path)
            pipeline = Pipeline(config)
            context = pipeline.process().context

            # Verify execution metadata was added
            metadata = context.get_value("template.metadata")
            assert "timestamp" in metadata
            assert metadata["context_stats"]["processor_active"]
            assert metadata["custom"]["operation"] == "test_operation"
            assert metadata["custom"]["version"] == "1.0"
            assert metadata["processor"]["name"] == "MetadataContextProcessor"

        finally:
            os.unlink(config_path)
            if os.path.exists("/tmp/test_metadata_output.txt"):
                os.unlink("/tmp/test_metadata_output.txt")


class TestComponentIntegration:
    """Test components working together in realistic scenarios."""

    def test_complete_string_processing_pipeline(self):
        """Test a complete pipeline using multiple template components."""
        # Create input file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("hello world")
            input_path = f.name

        # Create output file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            output_path = f.name

        pipeline_yaml = f"""
        extensions: ["template_extension"]
        pipeline:
          nodes:
            - processor: EchoContextProcessor
              parameters:
                message: "String processing pipeline"
            - processor: StringFileDataSource
              parameters:
                file_path: "{input_path}"
            - processor: StringUppercaseOperation
            - processor: StringLengthProbe
              context_keyword: "probes.length_result"
            - processor: StringFileSink
              parameters:
                file_path: "{output_path}"
        """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(pipeline_yaml)
            config_path = f.name

        try:
            config = load_pipeline_from_yaml(config_path)
            pipeline = Pipeline(config)
            context = pipeline.process().context

            # Verify the pipeline processed correctly
            with open(output_path, "r") as f:
                result = f.read()
            assert result == "HELLO WORLD"

            # Verify probe result was captured with context keyword
            probe_result = context.get_value("probes.length_result")
            assert probe_result == 11  # Length of "HELLO WORLD"

            # Verify processor added metadata
            echo_data = context.get_value("template.echo")
            assert echo_data == {"message": "String processing pipeline"}

        finally:
            for path in [input_path, output_path, config_path]:
                if os.path.exists(path):
                    os.unlink(path)


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v"])
