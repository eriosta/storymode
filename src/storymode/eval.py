from __future__ import annotations
import os, json, math
from typing import Dict, Any, List, Tuple
from collections import Counter, defaultdict
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

def load_dir_json(d: str) -> Dict[str, Dict[str, Any]]:
    out = {}
    for fn in os.listdir(d):
        if fn.endswith('.json'):
            with open(os.path.join(d, fn), 'r') as f:
                out[fn] = json.load(f)
    return out

def _safe_get(d, *keys):
    for k in keys:
        if d is None:
            return None
        d = d.get(k)
    return d

def lesion_match_key(lesion: Dict[str, Any]) -> Tuple:
    return (
        lesion.get("finding_type"),
        (lesion.get("body_site") or "").lower(),
        (lesion.get("node_station") or "").lower()
    )

def pair_lesions(pred: List[Dict[str,Any]], ref: List[Dict[str,Any]]) -> List[Tuple[Dict[str,Any], Dict[str,Any]]]:
    # Greedy pairing by (finding_type, body_site, node_station)
    used = set()
    pairs = []
    for p in pred:
        key = lesion_match_key(p)
        best = None
        for i, r in enumerate(ref):
            if i in used:
                continue
            if lesion_match_key(r) == key:
                best = i
                break
        if best is not None:
            used.add(best)
            pairs.append((p, ref[best]))
    return pairs

def numeric_mae_mm(pairs: List[Tuple[Dict[str,Any], Dict[str,Any]]]) -> float:
    errs = []
    for p, r in pairs:
        pv, rv = p.get('size_mm'), r.get('size_mm')
        if pv is not None and rv is not None:
            errs.append(abs(pv - rv))
    return sum(errs)/len(errs) if errs else math.nan

def within_tolerance(pairs, tol_mm=2):
    hits = 0
    total = 0
    for p, r in pairs:
        pv, rv = p.get('size_mm'), r.get('size_mm')
        if pv is not None and rv is not None:
            total += 1
            hits += int(abs(pv-rv) <= tol_mm)
    return hits, total

def evaluate(pred_dir: str, ref_dir: str) -> Dict[str, Any]:
    P = load_dir_json(pred_dir)
    R = load_dir_json(ref_dir)
    assert set(P.keys()) == set(R.keys()), "Prediction and reference files must match by name"

    entity_counts = Counter()
    numeric_pairs_all = []

    for fn in sorted(P.keys()):
        p, r = P[fn], R[fn]
        # doc-level mets present
        y_pred = int(_safe_get(p, 'summary', 'metastasis_present') or 0)
        y_true = int(_safe_get(r, 'summary', 'metastasis_present') or 0)
        entity_counts.update({"doc_total": 1, "doc_correct": int(y_pred == y_true)})

        # lesions
        pairs = pair_lesions(p.get('lesions', []), r.get('lesions', []))
        numeric_pairs_all.extend(pairs)

        # categorical slots (site and node station presence)
        def collect_slots(lesions, slot):
            vals = [1 if (ls.get(slot) not in (None, "", "unknown")) else 0 for ls in lesions]
            return sum(vals), len(vals)

        for slot in ["body_site", "node_station", "finding_type"]:
            p_have, p_tot = collect_slots(p.get('lesions', []), slot)
            r_have, r_tot = collect_slots(r.get('lesions', []), slot)
            # rough proxy: the closer these are, the better (can expand with span-based scoring later)
            entity_counts.update({f"{slot}_pred": p_have, f"{slot}_true": r_have})

    mae = numeric_mae_mm(numeric_pairs_all)
    hits2, tot2 = within_tolerance(numeric_pairs_all, tol_mm=2)
    hits10p, tot10p = within_tolerance(numeric_pairs_all, tol_mm=0)  # placeholder; adjust to % tolerance if desired

    results = {
        "doc_accuracy_mets_present": entity_counts["doc_correct"] / entity_counts["doc_total"],
        "size_mae_mm": mae,
        "size_within_2mm": None if tot2==0 else hits2/tot2,
        "counts": entity_counts
    }
    return results
