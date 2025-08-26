from __future__ import annotations
import json, os
from typing import Any, Dict, List
from jsonschema import Draft202012Validator
from pydantic import TypeAdapter
from tenacity import retry, stop_after_attempt, wait_fixed
from .schema import ReportExtraction
from .models import model_manager

def get_json_schema() -> Dict[str, Any]:
    # Build JSON Schema from Pydantic
    ta = TypeAdapter(ReportExtraction)
    json_schema = ta.json_schema()
    return json_schema

def validate_json(data: Dict[str, Any]) -> None:
    schema = get_json_schema()
    Draft202012Validator(schema).validate(data)

def _repair_common(json_text: str) -> str:
    # Lightweight repairs: trailing commas, single quotes, True/False/null variants
    fixed = json_text.strip()
    fixed = fixed.replace("\'", '"').replace("'", '"')
    fixed = fixed.replace("True", "true").replace("False", "false").replace("None", "null")
    return fixed

def coerce_and_validate(json_text: str) -> Dict[str, Any]:
    # Try to parse, repair once if needed, and validate
    try:
        obj = json.loads(json_text)
    except Exception:
        obj = json.loads(_repair_common(json_text))
    validate_json(obj)
    return obj

def format_messages_for_model(prompt: Dict[str, Any], model_name: str) -> List[Dict[str, str]]:
    """Format prompt into messages appropriate for the specific model"""
    config = model_manager.get_model_config(model_name)
    messages = []
    
    # Add system message if required
    if config.requires_system_prompt:
        messages.append({"role": "system", "content": prompt["system"]})
    
    # Add few-shot examples
    for msg in prompt["fewshot_messages"]:
        messages.append(msg)
    
    # Add user message
    messages.append({"role": "user", "content": prompt["user"]})
    
    return messages

@retry(stop=stop_after_attempt(2), wait=wait_fixed(0.2))
def constrained_json_completion(prompt: Dict[str, Any], model_name: str, **gen_kwargs) -> Dict[str, Any]:
    """Generic constrained decoding using the model abstraction layer."""
    
    # Get model backend and config
    backend = model_manager.get_backend(model_name)
    config = model_manager.get_model_config(model_name)
    
    # Format messages for the specific model
    messages = format_messages_for_model(prompt, model_name)
    
    # Prepare generation parameters
    gen_params = {
        "temperature": gen_kwargs.get("temperature", config.temperature),
        "max_tokens": gen_kwargs.get("max_tokens", config.max_tokens),
        "top_p": gen_kwargs.get("top_p", config.top_p),
    }
    
    # Add JSON schema if supported
    if config.json_mode_supported:
        json_schema = get_json_schema()
        gen_params["response_format"] = {
            "type": "json_schema",
            "json_schema": {"name": "ReportExtraction", "schema": json_schema}
        }
    
    # Generate response
    text = backend.generate(messages, **gen_params)
    
    # Parse and validate JSON
    return coerce_and_validate(text)
