import streamlit as st
from langgraph.graph import StateGraph, START, END
from core.state import MangroveState
from nodes.validator import node_validator
from nodes.spectral import node_spectral
from nodes.detector import node_detector
from nodes.cross_val import node_cross_val
from nodes.carbon import node_carbon
from nodes.ecosystem import node_ecosystem
from nodes.report import node_report
from nodes.scorer import node_scorer


def route_validator(state: MangroveState) -> str:
    return "spectral" if state.get("is_valid", False) else END


@st.cache_resource
def build_graph():
    g = StateGraph(MangroveState)
    g.add_node("validator", node_validator)
    g.add_node("spectral", node_spectral)
    g.add_node("detector", node_detector)
    g.add_node("cross_val", node_cross_val)
    g.add_node("carbon", node_carbon)
    g.add_node("ecosystem", node_ecosystem)
    g.add_node("report", node_report)
    g.add_node("scorer", node_scorer)
    g.add_edge(START, "validator")
    g.add_conditional_edges(
        "validator", route_validator, {"spectral": "spectral", END: END}
    )
    g.add_edge("spectral", "detector")
    g.add_edge("detector", "cross_val")
    g.add_edge("cross_val", "carbon")
    g.add_edge("carbon", "ecosystem")
    g.add_edge("ecosystem", "report")
    g.add_edge("report", "scorer")
    g.add_edge("scorer", END)
    return g.compile()
