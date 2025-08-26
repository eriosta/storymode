# StoryMode Project Structure

This document provides an overview of the StoryMode project structure and organization.

## 📁 Directory Structure

```
storymode/
├── 📄 Root Files
│   ├── README.md                 # Main project documentation
│   ├── CHANGELOG.md              # Version history and changes
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   ├── pyproject.toml            # Modern Python project configuration
│   ├── environment.yml           # Conda environment specification
│   ├── Makefile                  # Development task automation
│   ├── .gitignore                # Git ignore patterns
│   └── .pre-commit-config.yaml   # Code quality hooks
│
├── 📚 docs/                      # Documentation
│   └── README.md                 # Documentation structure guide
│
├── 💻 src/storymode/             # Main package source code
│   ├── __init__.py               # Package initialization and exports
│   ├── cli.py                    # Command-line interface
│   ├── models.py                 # Model abstraction layer
│   ├── extract.py                # Core extraction functionality
│   ├── decode.py                 # JSON completion and validation
│   ├── eval.py                   # Evaluation metrics
│   ├── schema.py                 # Data schemas and validation
│   ├── prompts.py                # System prompts and examples
│   ├── prompt_templates.py       # Model-specific prompt formatting
│   ├── postprocess.py            # Post-processing utilities
│   └── utils.py                  # General utilities
│
├── 🧪 tests/                     # Test suite
│   ├── test_basic.py             # Basic functionality tests
│   └── test_validation.py        # Schema validation tests
│
├── 📖 examples/                  # Examples and sample data
│   ├── README.md                 # Examples documentation
│   ├── reports/                  # Sample radiology reports
│   └── labels/                   # Ground truth annotations
│
├── 📓 notebooks/                 # Jupyter notebooks (placeholder)
├── 🔧 scripts/                   # Utility scripts
│   ├── install_dev.sh            # Linux/macOS dev setup
│   └── install_dev.bat           # Windows dev setup
│
└── 📦 build artifacts (gitignored)
    ├── dist/                     # Distribution packages
    ├── build/                    # Build artifacts
    └── *.egg-info/               # Package metadata
```

## 🏗️ Architecture Overview

### Core Components

1. **Model Abstraction Layer** (`models.py`)
   - `ModelConfig`: Configuration for each model
   - `ModelBackend`: Abstract base for inference backends
   - `ModelManager`: Singleton for managing models and backends
   - Backend implementations: `TransformersBackend`, `VLLMBackend`

2. **Extraction Pipeline** (`extract.py`, `decode.py`)
   - `extract_from_text()`: Single report extraction
   - `batch_extract()`: Batch processing
   - `constrained_json_completion()`: JSON generation with schema validation

3. **Data Schemas** (`schema.py`)
   - `ReportExtraction`: Main extraction result
   - `Lesion`: Individual lesion information
   - `Summary`: Document-level summary

4. **Evaluation Framework** (`eval.py`)
   - `evaluate()`: Comprehensive evaluation metrics
   - Lesion matching and scoring
   - Document-level classification metrics

5. **CLI Interface** (`cli.py`)
   - `extract`: Batch extraction command
   - `eval`: Evaluation command
   - `list-models`: Model information command

### Key Design Principles

1. **Modularity**: Clear separation of concerns
2. **Extensibility**: Easy to add new models and backends
3. **Type Safety**: Comprehensive type hints and validation
4. **Error Handling**: Graceful degradation and informative errors
5. **Cross-Platform**: Windows, Linux, and macOS support

## 🔧 Development Workflow

### Setup
```bash
# Create environment
conda env create -f environment.yml
conda activate storymode

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Common Tasks
```bash
# Run tests
make test

# Format code
make format

# Run linters
make lint

# Build package
make build

# Clean artifacts
make clean
```

### Adding New Models
1. Add configuration to `MODEL_CONFIGS` in `models.py`
2. Add prompt formatter to `prompt_templates.py` if needed
3. Test with `storymode list-models`
4. Update documentation

## 📊 Data Flow

```
Input Report (text) 
    ↓
[extract_from_text()]
    ↓
Model Backend (Transformers/vLLM)
    ↓
JSON Generation (constrained_json_completion)
    ↓
Schema Validation (pydantic)
    ↓
Output: ReportExtraction object
    ↓
[Optional: batch_extract() for multiple files]
    ↓
[Optional: evaluate() for metrics]
```

## 🎯 Supported Models

### Current Models (6 total)
- **General-Purpose**: Mistral 7B/8×7B, Qwen2.5-7B/14B
- **Biomedical**: BioMistral-7B, Meditron-7B

### Backend Support
- **Transformers**: Full support, cross-platform
- **vLLM**: Linux/macOS only (Windows compatibility issues)

## 🔍 Quality Assurance

### Code Quality Tools
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Automated quality checks

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Model Tests**: Model-specific functionality
- **Schema Tests**: Data validation testing

## 📈 Performance Considerations

### Memory Requirements
- **7B models**: 16GB+ GPU memory
- **14B models**: 24GB+ GPU memory
- **Mixtral 8×7B**: 24GB+ GPU memory

### Optimization Tips
1. Use vLLM for best performance (Linux/macOS)
2. Batch processing for multiple reports
3. Model quantization for memory efficiency
4. Context chunking for long reports

## 🚀 Deployment

### Package Distribution
- **PyPI**: Standard Python package distribution
- **Conda**: Environment-based distribution
- **Docker**: Containerized deployment (future)

### Installation Methods
```bash
# From PyPI
pip install storymode

# From source
git clone https://github.com/yourusername/storymode.git
cd storymode
pip install -e .

# With conda
conda env create -f environment.yml
```

## 🔮 Future Enhancements

### Planned Features
- **Docker Support**: Containerized deployment
- **Web Interface**: REST API and web UI
- **Additional Models**: More biomedical models
- **Advanced Metrics**: More sophisticated evaluation
- **Batch Processing**: Distributed processing support

### Extension Points
- **Custom Backends**: Easy backend addition
- **Custom Schemas**: Flexible data structures
- **Custom Metrics**: Extensible evaluation
- **Plugin System**: Modular functionality

---

This structure provides a solid foundation for a professional, maintainable, and extensible radiology information extraction framework.

