from __future__ import annotations

SYSTEM_PROMPT = """You are a meticulous clinical information extraction system.
Extract ONLY facts that are explicitly stated in the report. Do not infer.
Return STRICT JSON that conforms to the provided JSON Schema. Use millimeters for size.
If a field is not stated, omit it rather than guessing.
For lymph nodes, record the SHORT AXIS in mm when available. Include an evidence_span for each numeric or categorical value when possible.
"""

# Minimal few-shot exemplars (edit/expand with your synthetic styles)
FEW_SHOT = [
    {
        "report": """EXAM: CT CHEST/ABDOMEN/PELVIS WITH IV CONTRAST
IMPRESSION:
1. Left upper lobe mass measures 28 mm (previously 22 mm).
2. Enlarged right paratracheal node (station 4R) short axis 12 mm.
3. New 9 mm hypodense lesion in segment 6 of the liver, suspicious for metastasis.
""".strip(),
        "json": {
            "summary": {
                "modality": "CT", "body_region": "CAP",
                "tn_stage_reported": None, "metastasis_present": True, "total_lesion_count": 3
            },
            "lesions": [
                {
                    "lesion_id": "L1",
                    "finding_type": "primary",
                    "body_site": "lung upper lobe",
                    "is_node": False,
                    "laterality": "left",
                    "measure_axis": "longest",
                    "size_mm": 28,
                    "certainty": "present",
                    "evidence_span": "Left upper lobe mass measures 28 mm"
                },
                {
                    "lesion_id": "L2",
                    "finding_type": "ln",
                    "body_site": "mediastinum",
                    "is_node": True,
                    "node_station": "4R",
                    "measure_axis": "short_axis",
                    "size_mm": 12,
                    "certainty": "present",
                    "evidence_span": "right paratracheal node (station 4R) short axis 12 mm"
                },
                {
                    "lesion_id": "L3",
                    "finding_type": "met",
                    "body_site": "liver",
                    "metastatic_site": "liver",
                    "is_node": False,
                    "size_mm": 9,
                    "certainty": "possible",
                    "evidence_span": "New 9 mm hypodense lesion in segment 6 of the liver, suspicious for metastasis"
                }
            ]
        }
    }
]
