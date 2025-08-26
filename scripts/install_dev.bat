@echo off
REM Development installation script for StoryMode (Windows)

echo 🚀 Setting up StoryMode development environment...

REM Check if conda is available
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Conda is not installed. Please install Miniconda or Anaconda first.
    exit /b 1
)

REM Create conda environment
echo 📦 Creating conda environment...
call conda env create -f environment.yml

REM Activate environment
echo 🔧 Activating environment...
call conda activate storymode

REM Install package in development mode
echo 📥 Installing package in development mode...
pip install -e .

REM Install development dependencies
echo 🔧 Installing development dependencies...
pip install -e ".[dev]"

REM Install pre-commit hooks
echo 🔗 Installing pre-commit hooks...
pre-commit install

echo ✅ Development environment setup complete!
echo.
echo Next steps:
echo 1. Activate the environment: conda activate storymode
echo 2. Run tests: pytest
echo 3. Check code quality: black . && isort . && flake8
echo 4. Start developing!

pause

