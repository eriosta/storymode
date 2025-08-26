# Contributing to StoryMode

Thank you for your interest in contributing to StoryMode! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome contributions in the following areas:

- **Bug Reports**: Report bugs and issues
- **Feature Requests**: Suggest new features and improvements
- **Code Contributions**: Submit code changes and improvements
- **Documentation**: Improve documentation and examples
- **Testing**: Add tests and improve test coverage
- **Examples**: Create new examples and tutorials

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up the development environment** (see below)
4. **Create a feature branch** for your changes
5. **Make your changes** following the guidelines below
6. **Test your changes** thoroughly
7. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.11 or higher
- Conda or Miniconda
- Git

### Quick Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/storymode.git
cd storymode

# Create conda environment
conda env create -f environment.yml
conda activate storymode

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Windows Setup

```bash
# Use the Windows batch script
scripts/install_dev.bat
```

## 📝 Code Style and Standards

### Python Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Running Code Quality Checks

```bash
# Format code
make format

# Run linters
make lint

# Run all checks
make check
```

### Pre-commit Hooks

Pre-commit hooks automatically run code quality checks on commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_specific.py

# Run with verbose output
pytest -v tests/
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Use fixtures for common setup

Example test structure:

```python
import pytest
from storymode import extract_from_text

def test_extract_from_text_success():
    """Test successful extraction from text."""
    report = "EXAM: CT CHEST\nIMPRESSION: Left upper lobe mass 25mm"
    result = extract_from_text(report, model_name="mistral-7b-instruct")
    assert result is not None
    assert hasattr(result, 'summary')

def test_extract_from_text_empty_input():
    """Test extraction with empty input."""
    with pytest.raises(ValueError):
        extract_from_text("", model_name="mistral-7b-instruct")
```

## 📚 Documentation

### Documentation Structure

- **User Documentation**: In `docs/` directory
- **API Documentation**: Docstrings in code
- **Examples**: In `examples/` directory
- **README**: Main project documentation

### Writing Documentation

- Use clear, concise language
- Include code examples
- Keep documentation up to date with code changes
- Use proper markdown formatting

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
make docs
```

## 🔧 Adding New Models

### Model Configuration

To add a new model:

1. **Add model configuration** in `src/storymode/models.py`:

```python
"my-new-model": ModelConfig(
    name="my-new-model",
    backend="transformers",
    model_path="huggingface/model-id",
    temperature=0.0,
    max_tokens=1200,
    system_prompt_template="<s>[INST] {system} [/INST]",
    user_prompt_template="[INST] {user} [/INST]",
    assistant_prompt_template="{assistant}",
    requires_system_prompt=False,
    context_window=8192
)
```

2. **Add prompt formatter** in `src/storymode/prompt_templates.py` if needed
3. **Test the model** thoroughly
4. **Update documentation** with model information

### Backend Implementation

If adding a new backend:

1. **Implement backend class** inheriting from `ModelBackend`
2. **Add backend creation logic** in `ModelManager`
3. **Add tests** for the new backend
4. **Update documentation**

## 🐛 Bug Reports

### Before Submitting

- Check existing issues for duplicates
- Try to reproduce the issue
- Gather relevant information

### Bug Report Template

```markdown
**Bug Description**
Brief description of the issue.

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python version: [e.g., 3.11.0]
- StoryMode version: [e.g., 0.1.0]
- Model used: [e.g., mistral-7b-instruct]

**Additional Information**
Any other relevant information.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Brief description of the requested feature.

**Use Case**
Why this feature would be useful.

**Proposed Implementation**
How you think this could be implemented (optional).

**Alternatives Considered**
Other approaches you've considered (optional).
```

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure tests pass**: `make test`
2. **Run code quality checks**: `make check`
3. **Update documentation** if needed
4. **Add tests** for new functionality
5. **Update examples** if relevant

### Pull Request Template

```markdown
**Description**
Brief description of changes.

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test addition
- [ ] Other (please describe)

**Testing**
- [ ] Tests pass locally
- [ ] Code quality checks pass
- [ ] Documentation builds successfully

**Additional Notes**
Any additional information for reviewers.
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Address feedback** and make changes
4. **Merge** when approved

## 📋 Development Workflow

### Branch Naming

Use descriptive branch names:

- `feature/add-new-model`
- `bugfix/fix-extraction-error`
- `docs/update-installation-guide`
- `test/add-model-tests`

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```
feat(models): add new biomistral model configuration

fix(extract): handle empty input gracefully

docs(cli): update command line usage examples
```

## 🏷️ Release Process

### Version Bumping

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `src/storymode/__init__.py`
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Build and test package
- [ ] Create release tag
- [ ] Publish to PyPI

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow project conventions

### Communication

- Use GitHub Issues for bug reports and feature requests
- Use GitHub Discussions for questions and general discussion
- Be clear and concise in communications
- Provide context and examples

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the docs first
- **Examples**: Look at existing examples

## 🙏 Acknowledgments

Thank you to all contributors who help make StoryMode better!

---

For any questions about contributing, please open an issue or discussion on GitHub.

