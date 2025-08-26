"""
StoryMode: Radiology Report Information Extraction

A flexible framework for extracting structured information from radiology reports 
using open-source language models.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Core imports
from .schema import ReportExtraction, Lesion, Summary
from .extract import extract_from_text, batch_extract
from .eval import evaluate
from .models import model_manager, ModelConfig, ModelBackend

# CLI
from .cli import app

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "ReportExtraction",
    "Lesion", 
    "Summary",
    "extract_from_text",
    "batch_extract",
    "evaluate",
    "model_manager",
    "ModelConfig",
    "ModelBackend",
    "app",
]
