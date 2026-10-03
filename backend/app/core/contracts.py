from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ==========================================
# ENUMS
# ==========================================

class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DQStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


class RuleType(str, Enum):
    NOT_NULL = "NOT_NULL"
    UNIQUE = "UNIQUE"
    TYPE = "TYPE"
    RANGE = "RANGE"
    FORMAT = "FORMAT"
    REFERENTIAL_INTEGRITY = "REFERENTIAL_INTEGRITY"
    RECONCILIATION = "RECONCILIATION"


# ==========================================
# INGESTION & PROFILING CONTRACTS
# ==========================================

class DatasetMetadata(BaseModel):
    source_type: str = Field(..., description="File format e.g. csv, json, parquet")
    rows: int = Field(0, ge=0)
    columns: int = Field(0, ge=0)
    filename: Optional[str] = None


class ColumnProfile(BaseModel):
    column_name: str
    data_type: str
    null_count: int = Field(0, ge=0)
    null_percentage: float = Field(0.0, ge=0.0, le=100.0)
    unique_count: int = Field(0, ge=0)
    unique_percentage: float = Field(0.0, ge=0.0, le=100.0)
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    detected_patterns: List[str] = Field(default_factory=list)


class Relationship(BaseModel):
    source_column: str
    target_dataset: str
    target_column: str
    relationship_type: str = "FOREIGN_KEY"


class DatasetProfile(BaseModel):
    dataset_name: str
    row_count: int = Field(0, ge=0)
    column_count: int = Field(0, ge=0)
    duplicate_rows: int = Field(0, ge=0)
    memory_usage_bytes: int = Field(0, ge=0)
    columns: Dict[str, ColumnProfile] = Field(default_factory=dict)
    relationships: List[Relationship] = Field(default_factory=list)


# ==========================================
# SCHEMA CONTRACTS
# ==========================================

class SchemaField(BaseModel):
    column_name: str
    data_type: str
    nullable: bool = True
    unique: bool = False
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    pattern: Optional[str] = None


class SchemaDefinition(BaseModel):
    name: str
    fields: List[SchemaField] = Field(default_factory=list)


# ==========================================
# DATA QUALITY CONTRACTS
# ==========================================

class DQRule(BaseModel):
    rule_id: str
    column: str
    type: RuleType
    severity: Severity = Severity.MEDIUM
    params: Dict[str, Any] = Field(default_factory=dict)


class DQResult(BaseModel):
    rule_id: str
    status: DQStatus
    checked_rows: int = Field(0, ge=0)
    failed_rows: int = Field(0, ge=0)
    failure_rate: float = Field(0.0, ge=0.0, le=100.0)
    details: Optional[str] = None


# ==========================================
# PIPELINE LOG CONTRACTS
# ==========================================

class PipelineLogEvent(BaseModel):
    timestamp: Optional[str] = None
    log_level: str = "INFO"
    component: str = "pipeline"
    message: str
    error_details: Optional[str] = None


# ==========================================
# AI DIAGNOSIS OUTPUT CONTRACTS
# ==========================================

class Evidence(BaseModel):
    source: str = Field(..., description="e.g. dq_result, log, profile")
    reference: str = Field(..., description="e.g. DQ-PAY-001 or line_number")
    observation: str = Field(..., description="Factual statement grounded in backend evidence")


class ImpactItem(BaseModel):
    asset: str = Field(..., description="Downstream component or metric affected")
    severity: Severity = Severity.MEDIUM
    reason: str


class RemediationItem(BaseModel):
    action: str
    priority: Severity = Severity.MEDIUM


class QualityRuleSuggestion(BaseModel):
    name: str
    type: RuleType
    column: str
    severity: Severity = Severity.MEDIUM


class DiagnosisResult(BaseModel):
    severity: Severity = Severity.MEDIUM
    root_cause: str
    affected_entities: List[str] = Field(default_factory=list)
    affected_columns: List[str] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    impact: List[ImpactItem] = Field(default_factory=list)
    remediation: List[RemediationItem] = Field(default_factory=list)
    quality_rules: List[QualityRuleSuggestion] = Field(default_factory=list)


# ==========================================
# TOP-LEVEL API REQUEST/RESPONSE CONTRACTS
# ==========================================

class AnalysisRequest(BaseModel):
    dataset_name: str
    schema_definition: Optional[SchemaDefinition] = None
    pipeline_logs: List[PipelineLogEvent] = Field(default_factory=list)
    dq_rules: List[DQRule] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    profile: Optional[DatasetProfile] = None
    dq_results: List[DQResult] = Field(default_factory=list)
    diagnosis: Optional[DiagnosisResult] = None
