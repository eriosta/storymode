from __future__ import annotations
import json, os
from typing import Any, Dict
from jsonschema import Draft202012Validator
from pydantic import TypeAdapter
from tenacity import retry, stop_after_attempt, wait_fixed
from .schema import ReportExtraction

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

@retry(stop=stop_after_attempt(2), wait=wait_fixed(0.2))
def constrained_json_completion(prompt: str, client, model: str, **gen_kwargs) -> Dict[str, Any]:
    """Generic constrained decoding using an OpenAI-compatible client.
    The caller must provide `client` with a .chat.completions.create() method.
    """
    # Prefer response_format with json_schema when available
    json_schema = get_json_schema()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt["system"]},
            *prompt["fewshot_messages"],
            {"role": "user", "content": prompt["user"]}
        ],
        temperature=gen_kwargs.get("temperature", 0.0),
        max_tokens=gen_kwargs.get("max_tokens", 1200),
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "ReportExtraction", "schema": json_schema}
        }
    )
    text = response.choices[0].message.content
    return coerce_and_validate(text)
