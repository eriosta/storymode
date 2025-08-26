# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive project reorganization and cleanup
- Modern Python packaging with `pyproject.toml`
- Development tools and quality checks
- Pre-commit hooks for code quality
- Comprehensive documentation structure
- Contributing guidelines
- Example scripts and notebooks structure
- Makefile for common development tasks

### Changed
- Removed OpenAI models and dependencies
- Switched to pure open-source model support
- Updated project structure for better organization
- Improved code quality and testing infrastructure

### Fixed
- Windows compatibility issues with vLLM
- Package installation and import issues
- Code formatting and linting issues

## [0.1.0] - 2024-08-25

### Added
- Initial release of StoryMode
- Support for open-source language models (Mistral, Qwen, BioMistral, Meditron)
- Radiology report information extraction functionality
- Structured JSON output with schema validation
- Command-line interface for batch processing
- Model abstraction layer with multiple backends (vLLM, Transformers)
- Evaluation framework for model comparison
- Biomedical model support (BioMistral, Meditron)

### Features
- **Multi-Model Support**: Local inference with vLLM and Transformers
- **Structured Output**: Standardized JSON schema for radiology data
- **Biomedical Models**: Pre-configured medical-domain models
- **Deterministic Generation**: Reproducible results with configurable parameters
- **Validation**: JSON schema validation with automatic repair
- **CLI Interface**: Easy-to-use command-line tools
- **Batch Processing**: Efficient processing of multiple reports
- **Evaluation Metrics**: Comprehensive model evaluation framework

### Supported Models
- **General-Purpose**: Mistral 7B/8×7B, Qwen2.5-7B/14B
- **Biomedical**: BioMistral-7B, Meditron-7B

### Technical Details
- Python 3.11+ compatibility
- PyTorch-based inference
- HuggingFace Transformers integration
- vLLM support for high-performance inference
- Cross-platform compatibility (Windows, Linux, macOS)

---

## Version History

### Version 0.1.0
- **Release Date**: August 25, 2024
- **Status**: Initial release
- **Key Features**: Core extraction functionality, open-source model support
- **Breaking Changes**: None (initial release)

---

## Deprecated Features

None in current version.

## Migration Guides

### From Pre-0.1.0 (Development Versions)

If you were using development versions before 0.1.0:

1. **Update imports**: Package structure has been standardized
2. **Model names**: Some model names may have changed
3. **Configuration**: Use new `pyproject.toml` for dependencies
4. **Installation**: Follow new installation instructions in README

---

## Contributing to the Changelog

When contributing to this project, please update the changelog by:

1. Adding entries under the `[Unreleased]` section
2. Using the appropriate categories:
   - **Added**: New features
   - **Changed**: Changes in existing functionality
   - **Deprecated**: Soon-to-be removed features
   - **Removed**: Removed features
   - **Fixed**: Bug fixes
   - **Security**: Vulnerability fixes

3. Following the existing format and style
4. Including relevant details and breaking changes

---

For more information about versioning and releases, see [CONTRIBUTING.md](CONTRIBUTING.md).

