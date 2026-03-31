from typing import TypedDict, Annotated, List, Dict, Any
import operator


class MangroveState(TypedDict):
    image: Any
    image_width: int
    image_height: int
    temperature: float
    max_box_pct: float
    is_valid: bool
    image_type: str
    validator_conf: int
    validator_note: str
    ndvi_mean: float
    ndvi_std: float
    damage_pct: float
    healthy_pct: float
    water_pct: float
    heatmap: Any
    spectral_conf: float
    damage_mask: Any
    raw_hotspots: List[Dict]
    scene_summary: str
    validated_hotspots: List[Dict]
    rejected_count: int
    total_ha: float
    damaged_ha: float
    carbon_stock: float
    carbon_loss: float
    co2_eq: float
    econ_loss_bdt: float
    defor_rate: float
    species_at_risk: int
    habitat_loss_index: float
    coastal_km_at_risk: float
    recovery_years_natural: float
    recovery_years_assisted: float
    annual_seq_loss: float
    ecosystem_services_bdt: float
    carbon_5yr_projection: List[float]
    assessment: str
    actions: List[str]
    risk_level: str
    alert_msg: str
    accuracy_score: float
    health_score: float
    health_status: str
    acc_breakdown: Dict[str, float]
    spectral_agreement: float
    tp_count: int
    fp_count: int
    pipeline_log: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]
    timings: Dict[str, float]
    done_nodes: Annotated[List[str], operator.add]
    total_time: float
