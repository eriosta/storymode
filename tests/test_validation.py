from storymode.schema import ReportExtraction

def test_schema_roundtrip():
    js = {
        "summary": {"modality": "CT", "body_region": "CAP", "metastasis_present": True, "total_lesion_count": 2},
        "lesions": [
            {"lesion_id": "L1", "finding_type":"primary", "body_site":"lung", "size_mm": 28},
            {"lesion_id": "L2", "finding_type":"ln", "body_site":"mediastinum", "is_node": True, "node_station":"4R", "size_mm": 12}
        ]
    }
    obj = ReportExtraction(**js)
    assert obj.summary.total_lesion_count == 2
