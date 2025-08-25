from __future__ import annotations
import re
from typing import Dict, Any

def _cm_to_mm(val: float) -> int:
    return int(round(val * 10))

def normalize_units_and_cleanup(obj: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """Ensure mm units, basic cleanup, best-effort evidence span checks."""
    # Convert any 'size_mm' that look like centimeters in evidence to mm
    for ls in obj.get("lesions", []):
        ev = (ls.get("evidence_span") or "").lower()
        if " cm" in ev and isinstance(ls.get("size_mm"), (int, float)):
            # If evidence used cm but size_mm is a magnitude like 2 -> assume cm -> convert
            # Heuristic: if <= 10 and integer, treat as cm
            v = ls["size_mm"]
            if v is not None and v <= 10:
                ls["size_mm"] = _cm_to_mm(float(v))
        # Clamp negatives and nulls
        if ls.get("size_mm") is not None and ls["size_mm"] < 0:
            ls["size_mm"] = 0
    # Count lesions
    obj.setdefault("summary", {}).setdefault("total_lesion_count", len(obj.get("lesions", [])))
    # metastasis_present flag
    any_met = any(l.get("finding_type") == "met" for l in obj.get("lesions", []))
    obj["summary"]["metastasis_present"] = any_met
    return obj
