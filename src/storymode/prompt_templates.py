from __future__ import annotations
from typing import Dict, List, Any

class PromptFormatter:
    """Handles model-specific prompt formatting"""
    
    @staticmethod
    def format_mistral(messages: List[Dict[str, str]]) -> str:
        """Format messages for Mistral models"""
        prompt = "<s>"
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt += f"[INST] {content} [/INST]"
            elif role == "user":
                prompt += f"[INST] {content} [/INST]"
            elif role == "assistant":
                prompt += f" {content}"
        
        return prompt
    
    @staticmethod
    def format_qwen(messages: List[Dict[str, str]]) -> str:
        """Format messages for Qwen models"""
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
    
    @staticmethod
    def format_llama(messages: List[Dict[str, str]]) -> str:
        """Format messages for Llama models"""
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt += f"<s>[INST] <<SYS>>\n{content}\n<</SYS>>\n\n"
            elif role == "user":
                prompt += f"{content} [/INST]"
            elif role == "assistant":
                prompt += f" {content} </s><s>[INST] "
        
        return prompt
    
    @staticmethod
    def format_generic(messages: List[Dict[str, str]]) -> str:
        """Generic format for OpenAI-compatible models"""
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

# Model-specific formatters
MODEL_FORMATTERS = {
    "mistral-7b-instruct": PromptFormatter.format_mistral,
    "mixtral-8x7b-instruct": PromptFormatter.format_mistral,
    "biomistral-7b": PromptFormatter.format_mistral,
    "meditron-7b": PromptFormatter.format_mistral,
    "qwen2.5-7b-instruct": PromptFormatter.format_qwen,
    "qwen2.5-14b-instruct": PromptFormatter.format_qwen,
    "gpt-4o-mini": PromptFormatter.format_generic,
    "gpt-4o": PromptFormatter.format_generic,
}

def get_formatter(model_name: str):
    """Get the appropriate formatter for a model"""
    return MODEL_FORMATTERS.get(model_name, PromptFormatter.format_generic)

