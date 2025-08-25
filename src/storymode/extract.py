from __future__ import annotations
import os, json, time
from typing import Dict, Any, List
from dotenv import load_dotenv
from .schema import ReportExtraction
from .decode import constrained_json_completion, get_json_schema, coerce_and_validate
from .postprocess import normalize_units_and_cleanup
from .prompts import SYSTEM_PROMPT, FEW_SHOT
from .utils import make_openai_client, read_txt, dump_json, Timer

def build_prompt(report_text: str, prompt_version: str = "v1") -> Dict[str, Any]:
    # Few-shot messages for OpenAI-style API
    few = []
    for ex in FEW_SHOT:
        few.append({"role": "user", "content": ex["report"]})
        few.append({"role": "assistant", "content": json.dumps(ex["json"])})

    # JSON Schema for the user instruction context
    schema = get_json_schema()
    user = f"""Extract structured JSON conforming to the following JSON Schema:
{json.dumps(schema, indent=2)}
Report:
{report_text}
"""
    return {
        "system": SYSTEM_PROMPT + f"\nPROMPT_VERSION={prompt_version}",
        "fewshot_messages": few,
        "user": user
    }

def extract_from_text(report_text: str, client, model: str, **gen_kwargs) -> Dict[str, Any]:
    prompt = build_prompt(report_text, prompt_version="v1")
    raw = constrained_json_completion(prompt, client=client, model=model, **gen_kwargs)
    post = normalize_units_and_cleanup(raw, original_text=report_text)
    return post

def batch_extract(in_dir: str, out_dir: str, model: str, max_workers: int = 4, **gen_kwargs):
    os.makedirs(out_dir, exist_ok=True)
    client = make_openai_client()
    files = [f for f in os.listdir(in_dir) if f.lower().endswith(".txt")]
    files.sort()

    for fname in files:
        fp = os.path.join(in_dir, fname)
        report_text = read_txt(fp)
        with Timer() as t:
            data = extract_from_text(report_text, client=client, model=model, **gen_kwargs)
        data["model_name"] = model
        data["prompt_version"] = "v1"
        dump_json(data, os.path.join(out_dir, fname.replace(".txt", ".json")))
        print(f"Processed {fname} in {t.elapsed_ms:.1f} ms")