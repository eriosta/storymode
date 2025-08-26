from __future__ import annotations
import os
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
try:
    from vllm import LLM, SamplingParams
    VLLM_AVAILABLE = True
except ImportError:
    VLLM_AVAILABLE = False
    LLM = None
    SamplingParams = None


@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    name: str
    backend: str  # "openai", "vllm", "transformers", "tgi"
    model_path: str  # HuggingFace model ID or local path
    max_tokens: int = 1200
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = -1
    repetition_penalty: float = 1.0
    stop_tokens: Optional[List[str]] = None
    system_prompt_template: str = "<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n"
    user_prompt_template: str = "{user}"
    assistant_prompt_template: str = "{assistant}"
    requires_system_prompt: bool = True
    json_mode_supported: bool = False
    context_window: int = 8192

class ModelBackend(ABC):
    """Abstract base class for model backends"""
    
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate text from messages"""
        pass
    
    @abstractmethod
    def close(self):
        """Clean up resources"""
        pass



class VLLMBackend(ModelBackend):
    """Backend for vLLM inference"""
    
    def __init__(self, model_path: str, model_name: str = None, **kwargs):
        if not VLLM_AVAILABLE:
            raise ImportError("vLLM is not available. Please install vLLM or use transformers backend instead.")
        self.llm = LLM(model=model_path, **kwargs)
        self.model_name = model_name
        self.sampling_params = SamplingParams(
            temperature=0.0,
            top_p=1.0,
            max_tokens=1200,
            stop=["<|im_end|>", "\n\n"]
        )
    
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Convert messages to prompt format
        prompt = self._messages_to_prompt(messages)
        
        # Update sampling params if provided
        sampling_params = self.sampling_params
        if kwargs:
            sampling_params = SamplingParams(
                temperature=kwargs.get("temperature", self.sampling_params.temperature),
                top_p=kwargs.get("top_p", self.sampling_params.top_p),
                max_tokens=kwargs.get("max_tokens", self.sampling_params.max_tokens),
                stop=kwargs.get("stop", self.sampling_params.stop)
            )
        
        outputs = self.llm.generate([prompt], sampling_params)
        return outputs[0].outputs[0].text.strip()
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to prompt string"""
        from .prompt_templates import get_formatter
        formatter = get_formatter(self.model_name or "mistral-7b-instruct")
        return formatter(messages)
    
    def close(self):
        if hasattr(self, 'llm'):
            del self.llm

class TransformersBackend(ModelBackend):
    """Backend for local transformers inference"""
    
    def __init__(self, model_path: str, device: str = "auto", **kwargs):
        self.device = device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            **kwargs
        )
        
        # Set pad token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Convert messages to prompt
        prompt = self._messages_to_prompt(messages)
        
        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
        if self.device == "cuda":
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=kwargs.get("max_tokens", 1200),
                temperature=kwargs.get("temperature", 0.0),
                top_p=kwargs.get("top_p", 1.0),
                do_sample=kwargs.get("temperature", 0.0) > 0,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        generated_text = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        return generated_text.strip()
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to prompt string"""
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt += f"<|im_start|>system\n{content}<|im_end|>\n"
            elif role == "user":
                prompt += f"<|im_start|>user\n{content}<|im_end|>\n"
            elif role == "assistant":
                prompt += f"<|im_start|>assistant\n{content}<|im_end|>\n"
        
        prompt += "<|im_start|>assistant\n"
        return prompt
    
    def close(self):
        if hasattr(self, 'model'):
            del self.model
        if hasattr(self, 'tokenizer'):
            del self.tokenizer

class ModelManager:
    """Manages different model backends and configurations"""
    
    # Pre-configured model configurations
    MODEL_CONFIGS = {
        # General-purpose models
        "mistral-7b-instruct": ModelConfig(
            name="mistral-7b-instruct",
            backend="transformers",
            model_path="mistralai/Mistral-7B-Instruct-v0.2",
            temperature=0.0,
            max_tokens=1200,
            system_prompt_template="<s>[INST] {system} [/INST]",
            user_prompt_template="[INST] {user} [/INST]",
            assistant_prompt_template="{assistant}",
            requires_system_prompt=False,
            context_window=8192
        ),
        "mixtral-8x7b-instruct": ModelConfig(
            name="mixtral-8x7b-instruct",
            backend="transformers",
            model_path="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.0,
            max_tokens=1200,
            system_prompt_template="<s>[INST] {system} [/INST]",
            user_prompt_template="[INST] {user} [/INST]",
            assistant_prompt_template="{assistant}",
            requires_system_prompt=False,
            context_window=32768
        ),
        "qwen2.5-7b-instruct": ModelConfig(
            name="qwen2.5-7b-instruct",
            backend="transformers",
            model_path="Qwen/Qwen2.5-7B-Instruct",
            temperature=0.0,
            max_tokens=1200,
            system_prompt_template="<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n",
            user_prompt_template="<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n",
            assistant_prompt_template="{assistant}<|im_end|>",
            requires_system_prompt=True,
            context_window=32768
        ),
        "qwen2.5-14b-instruct": ModelConfig(
            name="qwen2.5-14b-instruct",
            backend="transformers",
            model_path="Qwen/Qwen2.5-14B-Instruct",
            temperature=0.0,
            max_tokens=1200,
            system_prompt_template="<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n",
            user_prompt_template="<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n",
            assistant_prompt_template="{assistant}<|im_end|>",
            requires_system_prompt=True,
            context_window=32768
        ),
        
        # Biomedical models
        "biomistral-7b": ModelConfig(
            name="biomistral-7b",
            backend="transformers",
            model_path="BioMistral/BioMistral-7B",
            temperature=0.0,
            max_tokens=1200,
            system_prompt_template="<s>[INST] {system} [/INST]",
            user_prompt_template="[INST] {user} [/INST]",
            assistant_prompt_template="{assistant}",
            requires_system_prompt=False,
            context_window=8192
        ),
        "meditron-7b": ModelConfig(
            name="meditron-7b",
            backend="transformers",
            model_path="epfl-llm/meditron-7b",
            temperature=0.0,
            max_tokens=1200,
            system_prompt_template="<s>[INST] {system} [/INST]",
            user_prompt_template="[INST] {user} [/INST]",
            assistant_prompt_template="{assistant}",
            requires_system_prompt=False,
            context_window=8192
        ),
        

    }
    
    def __init__(self):
        self.backends: Dict[str, ModelBackend] = {}
    
    def get_model_config(self, model_name: str) -> ModelConfig:
        """Get model configuration by name"""
        if model_name not in self.MODEL_CONFIGS:
            raise ValueError(f"Unknown model: {model_name}. Available models: {list(self.MODEL_CONFIGS.keys())}")
        return self.MODEL_CONFIGS[model_name]
    
    def get_backend(self, model_name: str) -> ModelBackend:
        """Get or create backend for a model"""
        if model_name in self.backends:
            return self.backends[model_name]
        
        config = self.get_model_config(model_name)
        
        if config.backend == "vllm":
            backend = VLLMBackend(config.model_path, model_name=model_name)
        
        elif config.backend == "transformers":
            backend = TransformersBackend(config.model_path)
        
        else:
            raise ValueError(f"Unsupported backend: {config.backend}")
        
        self.backends[model_name] = backend
        return backend
    
    def close_all(self):
        """Close all backends"""
        for backend in self.backends.values():
            backend.close()
        self.backends.clear()

# Global model manager instance
model_manager = ModelManager()
