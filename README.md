# Semantiva Extension Template

A template for building domain-specific Semantiva extensions with scaffolding for all component types.

## Quick Start

Clone this template and adapt it for your domain:

```bash
git clone git@github.com:semantiva/semantiva-extension-template.git my-semantiva-extension
cd my-semantiva-extension
```

## Adaptation Guide

Follow these steps to create your own Semantiva extension:

### 1. Rename Package Structure

Replace all occurrences of `template_extension` with your extension name:

- **Folder name**: Rename `template_extension/` → `my_extension/` 
- **Import statements**: Update all `from template_extension` imports
- **pyproject.toml**: Update package name, entry point, and description
- **Extension class**: Rename `TemplateExtension` → `MyExtension` in `__init__.py`
- **Module registration**: Update module names in the `register()` method

### 2. Update Configuration Files

**pyproject.toml**:
```toml
name = "semantiva-my-extension"
description = "My domain-specific extension for Semantiva"

[project.entry-points."semantiva.extensions"]
my_extension = "my_extension:MyExtension"
```

### 3. Define Your Domain Components

This template includes exemplar implementations of all Semantiva component types. Replace them with your domain-specific logic:

- **Data Types** (`data_types/`): Replace `StringDataType` and `StringDataCollection` with your domain types
- **Operations** (`operations/`): Replace string manipulation operations with your domain operations  
- **Probes** (`probes/`): Replace string analysis probes with your domain probes
- **Data I/O** (`data_io/`): Replace file-based sources/sinks with your domain I/O
- **Context Processors** (`processors/`): Replace echo processor with your domain context processors

### 4. Register Your Components

Update `__init__.py` to register your new modules:

```python
from semantiva.registry import SemantivaExtension
from semantiva.registry.processor_registry import ProcessorRegistry

class MyExtension(SemantivaExtension):
    def register(self) -> None:
        """Register all extension modules with the ProcessorRegistry.
        
        The ProcessorRegistry.register_modules() method automatically imports each module,
        which triggers component registration via the SemantivaComponent metaclass.
        This ensures components are available for both pipeline resolution and
        doctor discovery.
        """
        ProcessorRegistry.register_modules([
            "my_extension.data_types.data_types",
            "my_extension.operations.operations", 
            "my_extension.probes.probes",
            "my_extension.data_io.data_io",
            "my_extension.context_processors.processors",
        ])
```

## Component Architecture

This template demonstrates best practices for all Semantiva component types:

```
my_extension/
├── __init__.py              # Package initialization + SemantivaExtension
├── data_types/              # Domain data types
│   ├── __init__.py
│   └── data_types.py        # BaseDataType, DataCollectionType implementations
├── operations/              # Data transformations
│   ├── __init__.py  
│   └── operations.py        # DataOperation implementations
├── probes/                  # Data analysis
│   ├── __init__.py
│   └── probes.py            # DataProbe implementations  
├── data_io/                 # Input/output operations
│   ├── __init__.py
│   └── data_io.py           # DataSource, DataSink, PayloadSource, PayloadSink
└── context_processors/      # Context processors
    ├── __init__.py
    └── processors.py        # EchoContextProcessor, MetadataContextProcessor
```

## Features

- **Complete scaffolding**: Examples of all Semantiva component types
- **Entry point registration**: Automatic discovery via `semantiva.extensions`
- **Pipeline YAML example**: Demonstrates end-to-end usage
- **Comprehensive tests**: Unit tests and integration pipeline test
- **Clean architecture**: Follows Semantiva best practices
- **Domain neutrality**: Template avoids domain-specific terminology


## Development Workflow

1. **Install in development mode**:
   ```bash
   pip install -e .
   ```

2. **Run tests**:
   ```bash
   pytest -v
   ```

3. **Test your extension in a pipeline**:
   ```python
   from semantiva.registry import load_extensions
   from semantiva.pipeline import load_pipeline_from_yaml
   
   load_extensions("my_extension")
   pipeline = load_pipeline_from_yaml("tests/test_pipeline.yaml")
   results = pipeline.run()
   ```

4. **Validate your extension components**:
   ```bash
   # Validate all components in your extension
   semantiva dev lint --modules my_extension
   
   # Validate components used in a specific pipeline
   semantiva dev lint --yaml tests/test_pipeline.yaml
   
   # Get detailed validation information with debug mode
   semantiva dev lint --modules my_extension --debug
   
   # Export contract rules documentation
   semantiva dev lint --export-contracts contract_rules.md
   ```

## Component Validation

The `semantiva dev lint` command validates that your components follow Semantiva's architectural contracts, including:

- **Type safety**: All data type methods return proper types
- **Metadata completeness**: Required metadata keys are present
- **Stateless design**: Data I/O components use classmethods (SVA005, SVA007, SVA009, SVA011)
- **Interface contracts**: Components match their declared data types
- **Registry coherence**: Components are properly registered

Semantiva includes a comprehensive linting system via `semantiva dev lint` that validates your extension components against established design patterns and contracts. This ensures compatibility across the Semantiva ecosystem.

### Validation Features

- **Contract Compliance**: Ensures components follow proper interfaces and method signatures
- **Type Safety**: Validates data type definitions and relationships
- **Documentation Standards**: Checks for proper docstrings and metadata
- **Design Patterns**: Verifies components follow Semantiva architectural patterns
- **Integration Testing**: Confirms components work correctly with the pipeline system

### Using the Linter

```bash
# Validate all components in your extension
semantiva dev lint --modules my_extension

# Validate specific components from filesystem paths
semantiva dev lint --paths my_extension/data_types my_extension/operations

# Validate components discovered from a pipeline YAML
semantiva dev lint --yaml tests/test_pipeline.yaml

# Load and validate extension via entry point
semantiva dev lint --extensions my_extension

# Get detailed information about validation rules and results
semantiva dev lint --modules my_extension --debug

# Export validation rules documentation
semantiva dev lint --export-contracts validation_rules.md
```

### Understanding Validation Results

The linter categorizes issues into:
- **Errors**: Must be fixed for compatibility (e.g., missing required methods)
- **Warnings**: Should be addressed for best practices (e.g., long docstrings)
- **Info**: Informational notices about component design

All template components pass validation with ✓, demonstrating proper implementation patterns.

## Template Components

### Data Types (`data_types/`)
- **StringDataType**: Example BaseDataType implementation for strings
- **StringDataCollection**: Example DataCollectionType for string collections

### Operations (`operations/`)
- **StringUppercaseOperation**: Convert strings to uppercase
- **StringLowercaseOperation**: Convert strings to lowercase  
- **StringConcatenateOperation**: Append suffix to strings
- **StringCollectionJoinOperation**: Join string collections with separator

### Probes (`probes/`)
- **StringAnalysisProbe**: Comprehensive string analysis (length, character counts, etc.)
- **StringLengthProbe**: Simple string length measurement

### Data I/O (`data_io/`)
- **StringDataSource**: Generate string data with configurable content
- **StringFileDataSource**: Read strings from text files
- **StringFileSink**: Write strings to text files
- **StringPayloadSource**: Generate string payloads with context
- **StringPayloadSink**: Process string payloads and extract metadata

### Context Processors (`context_processors/`)
- **EchoContextProcessor**: Simple context processor for testing
- **MetadataContextProcessor**: Add metadata and statistics to context

## Testing

The template includes comprehensive testing and validation:

- **Component tests** (`test_template_extension.py`): Test individual components
- **Integration tests** (`test_pipeline_integration.py`): Test pipeline loading and architecture
- **Domain leak tests** (`test_no_domain_leaks.py`): Ensure template remains domain-neutral
- **Contract validation**: Use `semantiva dev lint` to validate component contracts

Run all tests:
```bash
pytest -v tests/
```

Validate all components:
```bash
semantiva dev lint --modules template_extension
```

## Dependencies

- **semantiva** >= 0.5.0

## Example Pipeline

The template includes a working pipeline example (`tests/test_pipeline.yaml`) that demonstrates:

1. Loading the template extension
2. Using data sources to generate content
3. Processing context with multiple processors
4. Applying data operations and transformations
5. Running analysis probes
6. Writing results to files

This provides a complete end-to-end example of Semantiva pipeline usage with extension components.