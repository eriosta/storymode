#!/bin/bash
# Development installation script for StoryMode

set -e

echo "🚀 Setting up StoryMode development environment..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi

# Create conda environment
echo "📦 Creating conda environment..."
conda env create -f environment.yml

# Activate environment
echo "🔧 Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate storymode

# Install package in development mode
echo "📥 Installing package in development mode..."
pip install -e .

# Install development dependencies
echo "🔧 Installing development dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🔗 Installing pre-commit hooks..."
pre-commit install

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the environment: conda activate storymode"
echo "2. Run tests: pytest"
echo "3. Check code quality: black . && isort . && flake8"
echo "4. Start developing!"

