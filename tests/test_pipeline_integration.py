"""Integration test for template extension pipeline execution."""

from pathlib import Path
from semantiva import load_pipeline_from_yaml


def test_pipeline_yaml_can_be_loaded():
    """Test that the pipeline YAML file is valid and can be parsed."""

    # Load the test pipeline YAML
    pipeline_file = Path(__file__).parent / "test_pipeline.yaml"
    assert pipeline_file.exists(), "test_pipeline.yaml should exist"

    pipeline_config = load_pipeline_from_yaml(pipeline_file)

    # Check that processors are specified
    for step in pipeline_config:
        assert "processor" in step


def test_component_types_are_complete():
    """Verify that all major Semantiva component types are represented."""

    # Check that we have examples of all component types
    from template_extension import (
        data_types,
        operations,
        probes,
        data_io,
        context_processors,
    )

    # Data Types
    assert hasattr(data_types, "StringDataType")
    assert hasattr(data_types, "StringDataCollection")

    # Operations
    assert hasattr(operations, "StringUppercaseOperation")
    assert hasattr(operations, "StringConcatenateOperation")

    # Probes
    assert hasattr(probes, "StringAnalysisProbe")
    assert hasattr(probes, "StringLengthProbe")

    # Data I/O
    assert hasattr(data_io, "StringDataSource")
    assert hasattr(data_io, "StringFileSink")
    assert hasattr(data_io, "StringPayloadSource")
    assert hasattr(data_io, "StringPayloadSink")

    # Processors
    assert hasattr(context_processors, "EchoContextProcessor")
    assert hasattr(context_processors, "MetadataContextProcessor")


if __name__ == "__main__":
    test_pipeline_yaml_can_be_loaded()
    test_component_types_are_complete()
    print("Pipeline integration tests passed!")
