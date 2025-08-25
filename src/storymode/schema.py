from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal

MM = int  # store sizes as integer millimeters


class Lesion(BaseModel):
    lesion_id: str = Field(..., description="Stable identifier within the report")
    finding_type: Literal["primary","ln","met","indeterminate","benign"] = "indeterminate"
    body_site: str = Field(..., description="Normalized organ/site (map to RadLex later)")
    metastatic_site: Optional[str] = Field(None, description="If met, specify organ/site")
    is_node: bool = False
    node_station: Optional[str] = Field(None, description="If node, LN station (e.g., 4R)")
    laterality: Optional[Literal["left","right","midline","bilateral","unknown"]] = "unknown"
    measure_axis: Optional[Literal["longest","short_axis","perpendicular","unknown"]] = "unknown"
    size_mm: Optional[MM] = Field(None, description="Size in **millimeters**")
    certainty: Optional[Literal["present","possible","unlikely"]] = "present"
    date_relative: Optional[str] = Field(None, description="e.g., 'increased from 12 to 18 mm since 06/2023'")
    note: Optional[str] = None
    evidence_span: Optional[str] = Field(None, description="Verbatim supporting text from the report")

    @field_validator("size_mm")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("size_mm must be >= 0")
        return v


class Summary(BaseModel):
    modality: Literal["CT","PETCT","MRI","XR","US","UNKNOWN"] = "UNKNOWN"
    body_region: Optional[Literal["C","A","P","CAP","WB","UNKNOWN"]] = "UNKNOWN"
    tn_stage_reported: Optional[str] = None  # if explicit in text
    metastasis_present: Optional[bool] = None
    total_lesion_count: Optional[int] = None


class ReportExtraction(BaseModel):
    patient_id: Optional[str] = None
    study_date: Optional[str] = None
    report_id: Optional[str] = None
    summary: Summary
    lesions: List[Lesion]

    model_name: Optional[str] = None
    prompt_version: Optional[str] = None
    schema_version: Literal["1.0"] = "1.0"

