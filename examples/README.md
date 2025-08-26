# StoryMode Examples

This directory contains examples and sample data for using StoryMode.

## 📁 Directory Structure

```
examples/
├── README.md                 # This file
├── data/                     # Sample data
│   ├── reports/             # Sample radiology reports
│   │   ├── sample_001.txt
│   │   ├── sample_002.txt
│   │   └── sample_003.txt
│   └── labels/              # Ground truth labels
│       ├── sample_001.json
│       ├── sample_002.json
│       └── sample_003.json
├── notebooks/               # Jupyter notebooks
│   ├── basic_extraction.ipynb
│   ├── model_comparison.ipynb
│   └── evaluation_analysis.ipynb
└── scripts/                 # Example scripts
    ├── batch_extract.py
    ├── model_evaluation.py
    └── custom_model.py
```

## 🚀 Quick Examples

### Basic Extraction

```python
from storymode import extract_from_text, model_manager

# Load a sample report
with open("examples/data/reports/sample_001.txt", "r") as f:
    report_text = f.read()

# Extract information using Mistral 7B
extraction = extract_from_text(
    report_text, 
    model_name="mistral-7b-instruct"
)

print(extraction.json(indent=2))
```

### Batch Processing

```python
from storymode import batch_extract
from pathlib import Path

# Process all reports in a directory
results = batch_extract(
    in_dir="examples/data/reports",
    out_dir="results",
    model_name="qwen2.5-7b-instruct",
    temperature=0.0
)

print(f"Processed {len(results)} reports")
```

### Model Comparison

```python
from storymode import batch_extract, evaluate_extractions

models = ["mistral-7b-instruct", "biomistral-7b", "qwen2.5-7b-instruct"]

for model in models:
    print(f"\nEvaluating {model}...")
    
    # Extract with current model
    batch_extract(
        in_dir="examples/data/reports",
        out_dir=f"results/{model}",
        model_name=model
    )
    
    # Evaluate against ground truth
    metrics = evaluate_extractions(
        pred_dir=f"results/{model}",
        ref_dir="examples/data/labels"
    )
    
    print(f"F1 Score: {metrics['f1_score']:.3f}")
```

## 📊 Sample Data

The `data/` directory contains:

- **Reports**: Sample radiology reports in plain text format
- **Labels**: Ground truth annotations in JSON format matching the extraction schema

### Report Format

Sample radiology report (`sample_001.txt`):
```
EXAM: CT CHEST/ABDOMEN/PELVIS WITH IV CONTRAST

TECHNIQUE: Multi-detector CT scan of the chest, abdomen, and pelvis 
was performed with intravenous contrast administration.

FINDINGS:

CHEST:
- Left upper lobe mass measures 28 mm (previously 22 mm)
- No significant mediastinal or hilar lymphadenopathy
- No pleural effusion

ABDOMEN:
- New 9 mm hypodense lesion in segment 6 of the liver, 
  suspicious for metastasis
- No other focal liver lesions
- Normal appearing pancreas, spleen, and kidneys

PELVIS:
- No significant findings

IMPRESSION:
1. Left upper lobe mass measures 28 mm (previously 22 mm)
2. New 9 mm hypodense lesion in segment 6 of the liver, 
   suspicious for metastasis
3. Recommend follow-up imaging in 3 months
```

### Label Format

Corresponding ground truth label (`sample_001.json`):
```json
{
  "summary": {
    "modality": "CT",
    "body_region": "CAP",
    "tn_stage_reported": null,
    "metastasis_present": true,
    "total_lesion_count": 2
  },
  "lesions": [
    {
      "lesion_id": "L1",
      "finding_type": "primary",
      "body_site": "lung upper lobe",
      "is_node": false,
      "laterality": "left",
      "measure_axis": "longest",
      "size_mm": 28,
      "certainty": "present",
      "evidence_span": "Left upper lobe mass measures 28 mm"
    },
    {
      "lesion_id": "L2",
      "finding_type": "met",
      "body_site": "liver",
      "metastatic_site": "liver",
      "is_node": false,
      "size_mm": 9,
      "certainty": "possible",
      "evidence_span": "New 9 mm hypodense lesion in segment 6 of the liver, suspicious for metastasis"
    }
  ]
}
```

## 📓 Jupyter Notebooks

The `notebooks/` directory contains interactive examples:

- **basic_extraction.ipynb**: Step-by-step extraction tutorial
- **model_comparison.ipynb**: Comparing different models
- **evaluation_analysis.ipynb**: Detailed evaluation analysis

## 🔧 Example Scripts

The `scripts/` directory contains reusable Python scripts:

- **batch_extract.py**: Command-line batch extraction
- **model_evaluation.py**: Automated model evaluation
- **custom_model.py**: Adding custom model configurations

## 🎯 Getting Started

1. **Install StoryMode**: Follow the main README installation instructions
2. **Explore Examples**: Start with the basic extraction notebook
3. **Run Scripts**: Try the example scripts with your own data
4. **Customize**: Modify examples for your specific use case

## 🤝 Contributing Examples

We welcome contributions of new examples! Please:

1. Follow the existing directory structure
2. Include clear documentation and comments
3. Test your examples before submitting
4. Add appropriate metadata and descriptions

For more information, see the main [Contributing Guide](../docs/contributing.md).

