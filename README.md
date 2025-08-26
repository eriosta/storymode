# StoryMode: Radiology Report Information Extraction

A flexible framework for extracting structured information from radiology reports using open-source language models.

## Features

- **Multi-Model Support**: Works with local open-source models via vLLM and direct transformers inference
- **Structured Output**: Extracts lesions, lymph nodes, and metastases with standardized JSON schema
- **Biomedical Models**: Pre-configured support for medical-domain models like BioMistral and Meditron
- **Deterministic Generation**: Configurable temperature and sampling parameters for reproducible results
- **Validation**: JSON schema validation with automatic repair for malformed outputs

## Supported Models

### Open-Source Models (Primary)

- **Mistral 7B Instruct** - Fast, compact baseline for zero/few-shot extraction
- **Mixtral 8×7B Instruct** - MoE architecture with higher capacity
- **Qwen2.5-7B/14B Instruct** - Strong reasoning with long context windows
- **BioMistral-7B** - Biomedical specialization of Mistral
- **Meditron-7B** - Medical-pretrained variant



## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd storymode
   ```

2. **Install dependencies**:
   ```bash
   conda env create -f environment.yml
   conda activate storymode
   ```

3. **For GPU inference** (recommended):
   ```bash
   # Install CUDA toolkit if not already installed
   # vLLM will automatically use available GPUs
   ```

## Quick Start

### List Available Models
```bash
python -m storymode list-models
```

### Extract Information from Reports
```bash
# Using Mistral 7B (local inference)
python -m storymode extract \
    --in-dir data/reports \
    --out-dir results \
    --model mistral-7b-instruct

# Using Qwen2.5-14B with custom parameters
python -m storymode extract \
    --in-dir data/reports \
    --out-dir results \
    --model qwen2.5-14b-instruct \
    --temperature 0.2 \
    --max-tokens 1500


```

### Evaluate Results
```bash
python -m storymode eval \
    --pred-dir results \
    --ref-dir data/examples/labels
```

## Model Configuration

### Open-Source Models

The framework automatically handles:
- **Model downloading** from HuggingFace Hub
- **Prompt formatting** for different model families
- **Inference optimization** via vLLM
- **Memory management** and cleanup

### Model-Specific Settings

Each model has pre-configured:
- **Context windows** (8K-32K tokens)
- **Temperature** (0.0 for deterministic)
- **Max tokens** (1200 default)
- **Prompt templates** (Mistral, Qwen, Llama formats)

### Custom Models

Add custom models by modifying `src/storymode/models.py`:

```python
"my-custom-model": ModelConfig(
    name="my-custom-model",
    backend="vLLM",
    model_path="path/to/model",
    temperature=0.0,
    max_tokens=1200,
    # ... other settings
)
```

## Data Format

### Input Reports
Plain text files (`.txt`) containing radiology reports:
```
EXAM: CT CHEST/ABDOMEN/PELVIS WITH IV CONTRAST
IMPRESSION:
1. Left upper lobe mass measures 28 mm (previously 22 mm).
2. Enlarged right paratracheal node (station 4R) short axis 12 mm.
3. New 9 mm hypodense lesion in segment 6 of the liver.
```

### Output JSON
Structured extraction following the schema:
```json
{
  "summary": {
    "modality": "CT",
    "body_region": "CAP",
    "metastasis_present": true,
    "total_lesion_count": 3
  },
  "lesions": [
    {
      "lesion_id": "L1",
      "finding_type": "primary",
      "body_site": "lung upper lobe",
      "laterality": "left",
      "size_mm": 28,
      "evidence_span": "Left upper lobe mass measures 28 mm"
    }
  ]
}
```

## Performance Considerations

### Hardware Requirements

- **7B models**: 16GB+ GPU memory
- **14B models**: 24GB+ GPU memory  
- **Mixtral 8×7B**: 24GB+ GPU memory
- **CPU inference**: Available but slow

### Optimization Tips

1. **Use vLLM** for best performance
2. **Batch processing** for multiple reports
3. **Model quantization** for memory efficiency
4. **Context chunking** for long reports

## Research Use

This framework is designed for:
- **Reproducible evaluation** of extraction models
- **A/B testing** different model families
- **Domain adaptation** studies (biomedical vs general)
- **Prompt engineering** experiments

### Evaluation Metrics

- **Entity-level F1** for lesion detection
- **Numeric accuracy** for size measurements
- **Document-level classification** for metastasis presence
- **Inter-rater reliability** (ICC) for continuous variables

## License

[Add your license information here]

## Citation

[Add citation information if applicable]
