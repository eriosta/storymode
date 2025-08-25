# StoryMode

Zero-/few-shot pipeline to extract lesion-level, TNM-relevant facts from (synthetic) radiology reports using **strict JSON schemas**, **deterministic prompting**, and **constrained decoding**. No fine-tuning required to start.

## Why this repo?
- Enforces a single source of truth schema (Pydantic + JSON Schema).
- Deterministic decoding with schema validation + repair loop.
- Post-processing for unit normalization (mm), ontology hooks, and span grounding.
- Evaluation harness with entity F1, numeric error, JSON-validity, hallucination/omission rates.
- CLI to run extraction on a folder of reports and to evaluate against references.

## Install

### Option 1: Using Conda (Recommended)
```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate storymode
```

### Option 2: Using Python venv
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### Installing Conda
If you don't have conda installed, you can install Miniconda from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html) or Anaconda from [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution).

## Conda Environment Setup

### 1. Create the Environment
```bash
conda env create -f environment.yml
```

### 2. Activate the Environment
```bash
conda activate storymode
```

### 3. Test the CLI
```bash
# From the project root directory
python -c "import sys; sys.path.append('src'); from storymode.cli import app; print('CLI ready!')"
```

## Quickstart
Extract JSON from example reports using a local or hosted LLM (OpenAI-style API supported).

```bash
# Run extraction
python -m storymode.cli extract \  --in_dir data/examples/reports \  --out_dir runs/example_json \  --model gpt-4o-mini \  --max_workers 4

# Evaluate (requires provided references for examples)
python -m storymode.cli eval \  --pred_dir runs/example_json \  --ref_dir data/examples/labels
```

## Repo layout
```
storymode/
  data/examples/
    reports/                 # sample synthetic reports (.txt)
    labels/                  # matching JSON labels to the schema
  src/storymode/
    schema.py                # Pydantic models + JSON Schema
    prompts.py               # system + few-shot exemplars
    decode.py                # constrained JSON decoding + repair loop
    extract.py               # core pipeline (prompt -> JSON -> postprocess)
    postprocess.py           # unit normalization, ontology hooks, dedupe
    eval.py                  # metrics
    cli.py                   # CLI (extract/eval)
    utils.py                 # logging, IO, timing helpers
  tests/
    test_validation.py
  requirements.txt
  pyproject.toml (optional)
```

## Notes
- JSON outputs are strictly in **millimeters** for size fields.
- Each numeric field should include an `evidence_span` pointing back to source text when possible.
- This repository is model-agnostic. It provides an OpenAI-compatible client and a hook to plug your own inference function.
