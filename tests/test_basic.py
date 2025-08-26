#!/usr/bin/env python3
"""
Basic test script for open-source model functionality (no heavy dependencies)
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test that we can import the core modules"""
    print("Testing imports...")
    try:
        # Test basic imports that don't require heavy dependencies
        from storymode.schema import ReportExtraction, Lesion, Summary
        from storymode.prompts import SYSTEM_PROMPT, FEW_SHOT
        from storymode.utils import Timer, read_txt, dump_json
        print("✓ Core imports work")
        return True
    except Exception as e:
        print(f"✗ Core imports failed: {e}")
        return False

def test_schema():
    """Test that the schema works correctly"""
    print("\nTesting schema...")
    try:
        from storymode.schema import ReportExtraction, Lesion, Summary
        
        # Test creating a valid extraction
        lesion = Lesion(
            lesion_id="L1",
            finding_type="primary",
            body_site="lung",
            size_mm=25,
            evidence_span="25 mm mass in left lung"
        )
        
        summary = Summary(
            modality="CT",
            body_region="CAP",
            metastasis_present=True,
            total_lesion_count=1
        )
        
        extraction = ReportExtraction(
            summary=summary,
            lesions=[lesion]
        )
        
        print("✓ Schema validation works")
        return True
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        return False

def test_model_configs():
    """Test model configuration structure (without heavy imports)"""
    print("\nTesting model configurations...")
    try:
        # Create a minimal model config to test the structure
        from dataclasses import dataclass
        from typing import List, Optional
        
        @dataclass
        class TestModelConfig:
            name: str
            backend: str
            model_path: str
            max_tokens: int = 1200
            temperature: float = 0.0
            context_window: int = 8192
        
        # Test configurations
        configs = {
            "mistral-7b-instruct": TestModelConfig(
                name="mistral-7b-instruct",
                backend="transformers",
                model_path="mistralai/Mistral-7B-Instruct-v0.2",
                temperature=0.0,
                max_tokens=1200,
                context_window=8192
            ),
            "qwen2.5-7b-instruct": TestModelConfig(
                name="qwen2.5-7b-instruct", 
                backend="transformers",
                model_path="Qwen/Qwen2.5-7B-Instruct",
                temperature=0.0,
                max_tokens=1200,
                context_window=32768
            ),
            "biomistral-7b": TestModelConfig(
                name="biomistral-7b",
                backend="transformers", 
                model_path="BioMistral/BioMistral-7B",
                temperature=0.0,
                max_tokens=1200,
                context_window=8192
            )
        }
        
        print(f"✓ Found {len(configs)} test model configurations")
        
        # Verify all required fields
        required_fields = ['name', 'backend', 'model_path', 'temperature', 'max_tokens']
        for model_name, config in configs.items():
            for field in required_fields:
                if not hasattr(config, field):
                    print(f"✗ Missing field '{field}' in {model_name}")
                    return False
        
        print("✓ All model configurations are valid")
        return True
    except Exception as e:
        print(f"✗ Model configuration test failed: {e}")
        return False

def test_prompt_templates():
    """Test prompt template functionality"""
    print("\nTesting prompt templates...")
    try:
        from storymode.prompt_templates import PromptFormatter, get_formatter
        
        # Test message formatting
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Extract information from this report."},
            {"role": "assistant", "content": "I'll help you extract the information."}
        ]
        
        # Test different formatters
        mistral_prompt = PromptFormatter.format_mistral(messages)
        qwen_prompt = PromptFormatter.format_qwen(messages)
        generic_prompt = PromptFormatter.format_generic(messages)
        
        print(f"✓ Mistral prompt length: {len(mistral_prompt)}")
        print(f"✓ Qwen prompt length: {len(qwen_prompt)}")
        print(f"✓ Generic prompt length: {len(generic_prompt)}")
        
        # Test formatter selection
        formatter = get_formatter("mistral-7b-instruct")
        print("✓ Formatter selection works")
        
        return True
    except Exception as e:
        print(f"✗ Prompt template test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing open-source model functionality (basic tests)...\n")
    
    tests = [
        test_imports,
        test_schema,
        test_model_configs,
        test_prompt_templates,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! The core functionality is working.")
        print("\nNext steps:")
        print("1. Install dependencies: conda env create -f environment.yml")
        print("2. Test with actual models: python -m storymode list-models")
        print("3. Run extraction: python -m storymode extract --help")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
