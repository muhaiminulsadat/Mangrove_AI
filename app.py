import io
import json
import os
import time
from datetime import datetime

import streamlit as st
from PIL import Image

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

st.set_page_config(
    page_title="Mangrove AI Protector — Green Flare",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

from core.gemini import init_gemini
from core.graph import build_graph
from ui.css import inject_css
from ui.components import (
    draw_boxes,
    pipeline_svg,
    RISK_BG,
    RISK_BORDER,
    RISK_TEXT,
    NODES_META,
)
from ui.tabs import (
    render_tab_detection,
    render_tab_accuracy,
    render_tab_carbon,
    render_tab_ecosystem,
    render_tab_report,
    render_tab_log,
)

api_key = None
try:
    api_key = st.secrets["GEMINI_KEY"]
except Exception:
    pass
if not api_key:
    api_key = os.getenv("GEMINI_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    st.sidebar.markdown("#### 🔑 API Key")
    api_key = st.sidebar.text_input(
        "Gemini API Key", type="password", placeholder="AIza..."
    )

if not api_key:
    st.markdown(
        """
    <div style="max-width:480px;margin:80px auto;padding:48px;background:#1e293b;
         border-radius:16px;box-shadow:0 4px 24px rgba(0,0,0,0.5);text-align:center;border:1px solid #334155;">
      <div style="font-size:3rem;margin-bottom:16px;">🌿</div>
      <h2 style="color:#34d399;font-size:1.5rem;margin:0 0 10px;font-weight:700;">API Key Required</h2>
      <p style="color:#94a3b8;font-size:1rem;line-height:1.65;margin:0 0 24px;">
        Paste your Gemini API key in the sidebar to activate the analysis pipeline.
      </p>
      <code style="background:#064e3b;color:#6ee7b7;padding:12px 20px;border-radius:8px;
           font-size:0.95rem;border:1px solid #059669;display:block;">GEMINI_KEY = "AIza..."</code>
    </div>""",
        unsafe_allow_html=True,
    )
    st.stop()

init_gemini(api_key)
inject_css()

st.markdown(
    """
<div class="project-header">
  <div class="project-header-left">
    <h1>🌿 Mangrove AI Protector</h1>
    <p>Satellite deforestation intelligence for the Sundarbans ecosystem.
       8-node LangGraph pipeline combining Gemini Vision, deterministic NDVI spectral analysis,
       IPCC Tier 1 carbon accounting, ecosystem impact modelling, and cross-modal validation.</p>
    <div class="header-badges">
      <span class="hbadge">LangGraph 8-Node StateGraph</span>
      <span class="hbadge">NDVI · Zero AI</span>
      <span class="hbadge">IPCC Tier 1 Carbon</span>
      <span class="hbadge">Ecosystem Impact Model</span>
      <span class="hbadge">Cross-Modal Validation</span>
      <span class="hbadge-gray">Gemini Vision</span>
      <span class="hbadge-gray">5-Signal Accuracy</span>
      <span class="hbadge-gray">Recovery Projection</span>
    </div>
  </div>
  <div class="project-header-right">
    <div class="team-badge">⚡ TEAM GREEN FLARE</div>
    <span class="hackathon-label">Eco-Tech Hackathon 2026 · Environment Watch: BUET</span>
  </div>
</div>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<span class="sidebar-label">Current Image Source</span>',
        unsafe_allow_html=True,
    )
    img_in = None
    up = st.file_uploader(
        "Satellite or aerial image",
        type=["png", "jpg", "jpeg", "tif", "tiff"],
        label_visibility="collapsed",
    )
    if up:
        img_in = Image.open(up).convert("RGBA")
    else:
        st.caption("Upload a satellite / aerial image to begin.")

    st.markdown(
        '<span class="sidebar-label">Detection Settings</span>', unsafe_allow_html=True
    )
    temperature = st.slider(
        "AI Temperature",
        0.0,
        0.8,
        0.1,
        0.05,
        help="Lower = more conservative detections",
    )
    max_box_pct = (
        st.slider(
            "Max box area (%)",
            2,
            40,
            15,
            2,
            help="Filter AI bounding boxes larger than this % of image",
        )
        / 100
    )

    st.markdown(
        '<span class="sidebar-label">Pipeline — 8 Nodes</span>', unsafe_allow_html=True
    )
    for tag, name, desc in [
        ("N1", "Validator", "Image gate — blocks non-satellite"),
        ("N2", "Spectral", "NDVI pixel analysis — zero AI"),
        ("N3", "Detector", "Gemini Vision — primary detection"),
        ("N4", "Cross-Val", "Geometric + spectral verification"),
        ("N5", "Carbon", "IPCC Tier 1 — zero AI"),
        ("N6", "Ecosystem", "Biodiversity + coastal — zero AI"),
        ("N7", "Reporter", "Scientific narrative — AI text"),
        ("N8", "Scorer", "5-signal accuracy composite"),
    ]:
        st.markdown(
            f'<div style="display:flex;gap:12px;margin-bottom:12px;align-items:flex-start;">'
            f"<span style=\"font-family:'JetBrains Mono',monospace;font-size:0.75rem;font-weight:700;"
            f"background:#064e3b;border:1px solid #059669;color:#34d399;padding:2px 6px;"
            f'border-radius:4px;flex-shrink:0;margin-top:2px;">{tag}</span>'
            f'<div><span style="font-size:0.95rem;font-weight:600;color:#f8fafc;">{name}</span>'
            f'<br><span style="font-size:0.8rem;color:#94a3b8;line-height:1.4;display:block;">{desc}</span></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("gemini-2.5-flash · langgraph ≥ 0.2 · Sentinel-2 10m")

if img_in is None:
    st.stop()

col_img, col_out = st.columns(2)
with col_img:
    st.markdown(
        '<div class="section-head">📡 Satellite Input <span>—</span></div>',
        unsafe_allow_html=True,
    )
    st.image(img_in, use_container_width=True)
    st.caption(f"{img_in.width} × {img_in.height} px · {img_in.mode}")

run_col, _ = st.columns([1, 4])
with run_col:
    run_btn = st.button("🚀  Execute Pipeline", use_container_width=True)

if run_btn:
    graph = build_graph()
    t_start = time.time()
    pipe_ph = st.empty()
    status_ph = st.empty()

    def render_pipe(done, active="", msg=""):
        with pipe_ph:
            st.markdown(
                f'<div class="pipeline-wrap">'
                f'<p class="pipeline-title">LangGraph StateGraph · 8 nodes · conditional routing</p>'
                f"{pipeline_svg(done, active)}</div>",
                unsafe_allow_html=True,
            )
        if msg:
            with status_ph:
                st.markdown(
                    f'<div class="status-line"><span class="status-dot"></span>{msg}</div>',
                    unsafe_allow_html=True,
                )

    render_pipe([], "", "Initialising LangGraph StateGraph...")

    from core.state import MangroveState

    init: MangroveState = {
        "image": img_in,
        "image_width": img_in.width,
        "image_height": img_in.height,
        "temperature": temperature,
        "max_box_pct": max_box_pct,
        "is_valid": False,
        "image_type": "",
        "validator_conf": 0,
        "validator_note": "",
        "ndvi_mean": 0.0,
        "ndvi_std": 0.0,
        "damage_pct": 0.0,
        "healthy_pct": 0.0,
        "water_pct": 0.0,
        "heatmap": None,
        "spectral_conf": 0.0,
        "damage_mask": None,
        "raw_hotspots": [],
        "scene_summary": "",
        "validated_hotspots": [],
        "rejected_count": 0,
        "total_ha": 0.0,
        "damaged_ha": 0.0,
        "carbon_stock": 0.0,
        "carbon_loss": 0.0,
        "co2_eq": 0.0,
        "econ_loss_bdt": 0.0,
        "defor_rate": 0.0,
        "species_at_risk": 0,
        "habitat_loss_index": 0.0,
        "coastal_km_at_risk": 0.0,
        "recovery_years_natural": 0.0,
        "recovery_years_assisted": 0.0,
        "annual_seq_loss": 0.0,
        "ecosystem_services_bdt": 0.0,
        "carbon_5yr_projection": [],
        "assessment": "",
        "actions": [],
        "risk_level": "LOW",
        "alert_msg": "",
        "accuracy_score": 0.0,
        "health_score": 10.0,
        "health_status": "Healthy",
        "acc_breakdown": {},
        "spectral_agreement": 100.0,
        "tp_count": 0,
        "fp_count": 0,
        "pipeline_log": [],
        "errors": [],
        "timings": {},
        "done_nodes": [],
        "total_time": 0.0,
    }

    render_pipe([], "validator", "Node N1 — validating image type...")
    try:
        final = None
        for s in graph.stream(init, config={"recursion_limit": 50}, stream_mode="values"):
            final = s
            done = s.get("done_nodes", [])
            
            active_node = ""
            active_desc = ""
            for key, num, name in NODES_META:
                if key not in done:
                    active_node = key
                    active_desc = f"Node {num} — {name} running..."
                    break
            
            if not active_node:
                active_desc = "Pipeline completed."
            
            render_pipe(done, active_node, active_desc)
            time.sleep(0.05)
            
    except Exception as e:
        status_ph.error(f"Pipeline error: {e}")
        st.exception(e)
        st.stop()

    final["total_time"] = round(time.time() - t_start, 1)
    render_pipe(final.get("done_nodes", []), "", "")
    status_ph.empty()

    if not final.get("is_valid", False):
        st.markdown(
            f'<div class="risk-box" style="--rb:#991b1b;--rg:#450a0a;--rt:#fca5a5;">'
            f'<span class="risk-icon">⛔</span>'
            f'<span class="risk-txt"><strong>Invalid image:</strong> {final.get("validator_note","Not a valid satellite image.")} — Please upload a satellite or aerial photograph.</span></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    hotspots = final.get("validated_hotspots", [])
    annotated = draw_boxes(img_in, hotspots)
    with col_out:
        st.markdown(
            '<div class="section-head">🗺️ Validated Damage Map <span>—</span></div>',
            unsafe_allow_html=True,
        )
        st.image(annotated, use_container_width=True)
        st.caption(
            f"{len(hotspots)} confirmed hotspot(s) · {final.get('rejected_count',0)} filtered · Runtime: {final['total_time']}s"
        )

    risk = final.get("risk_level", "LOW")
    alert = final.get("alert_msg", "")
    rb, rg, rt = (
        RISK_BORDER.get(risk, "#14532d"),
        RISK_BG.get(risk, "#052e16"),
        RISK_TEXT.get(risk, "#86efac"),
    )
    icon = "🚨" if risk in ("HIGH", "CRITICAL") else "⚠️" if risk == "MODERATE" else "✅"
    if alert and risk in ("HIGH", "CRITICAL"):
        st.markdown(
            f'<div class="risk-box" style="--rb:{rb};--rg:{rg};--rt:{rt};"><span class="risk-icon">{icon}</span><span class="risk-txt"><strong>Alert:</strong> {alert}</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="risk-box" style="--rb:{rb};--rg:{rg};--rt:{rt};"><span class="risk-icon">{icon}</span><span class="risk-txt">Risk Level: <strong>{risk}</strong> · Forest Health: <strong>{final.get("health_score",10)}/10 — {final.get("health_status","Healthy")}</strong></span></div>',
            unsafe_allow_html=True,
        )

    dl1, dl2, dl3, dl4 = st.columns(4)
    with dl1:
        buf = io.BytesIO()
        annotated.convert("RGB").save(buf, format="PNG")
        st.download_button(
            "⬇ Annotated Map",
            buf.getvalue(),
            "damage_map.png",
            "image/png",
            use_container_width=True,
        )
    with dl2:
        hm_img = final.get("heatmap")
        if hm_img:
            buf2 = io.BytesIO()
            hm_img.save(buf2, format="PNG")
            st.download_button(
                "⬇ Spectral Heatmap",
                buf2.getvalue(),
                "heatmap.png",
                "image/png",
                use_container_width=True,
            )
    with dl3:
        report_json = {
            "timestamp": datetime.now().isoformat(),
            "team": "Green Flare",
            "hackathon": "Eco-Tech Hackathon 2026",
            "institution": "Environment Watch · BUET",
            "model": "gemini-2.5-flash",
            "pipeline": "LangGraph 8-node StateGraph",
            "health": {
                "score": final.get("health_score"),
                "status": final.get("health_status"),
            },
            "accuracy": {
                "score": final.get("accuracy_score"),
                "spectral_agreement_pct": final.get("spectral_agreement"),
            },
            "risk_level": final.get("risk_level"),
            "hotspots": hotspots,
            "spectral": {
                "ndvi_mean": final.get("ndvi_mean"),
                "ndvi_std": final.get("ndvi_std"),
                "damage_pct": final.get("damage_pct"),
                "healthy_pct": final.get("healthy_pct"),
                "water_pct": final.get("water_pct"),
            },
            "carbon": {
                "total_ha": final.get("total_ha"),
                "damaged_ha": final.get("damaged_ha"),
                "carbon_stock_tc": final.get("carbon_stock"),
                "carbon_loss_tc": final.get("carbon_loss"),
                "co2_eq_tc": final.get("co2_eq"),
                "economic_loss_bdt": final.get("econ_loss_bdt"),
                "deforestation_rate_pct": final.get("defor_rate"),
            },
            "ecosystem": {
                "species_at_risk": final.get("species_at_risk"),
                "habitat_loss_index_pct": final.get("habitat_loss_index"),
                "coastal_km_at_risk": final.get("coastal_km_at_risk"),
                "annual_seq_loss_tco2e": final.get("annual_seq_loss"),
                "ecosystem_services_bdt": final.get("ecosystem_services_bdt"),
                "recovery_natural_years": final.get("recovery_years_natural"),
                "recovery_assisted_years": final.get("recovery_years_assisted"),
                "carbon_5yr_projection_tco2e": final.get("carbon_5yr_projection"),
            },
            "assessment": final.get("assessment"),
            "actions": final.get("actions"),
            "pipeline_log": final.get("pipeline_log"),
            "node_timings_s": final.get("timings"),
        }
        st.download_button(
            "⬇ Full JSON Report",
            json.dumps(report_json, indent=2),
            "mangrove_report.json",
            "application/json",
            use_container_width=True,
        )
    with dl4:
        csv_rows = [
            "Zone,Severity,AI_Confidence,Damage_Type,Spectral_Overlap_Pct,Verdict,Note"
        ]
        for i, hs in enumerate(hotspots):
            zone = f"SB-{chr(65+i)}{i+1:02d}"
            csv_rows.append(
                f'{zone},{hs.get("severity","")},{hs.get("final_confidence","")},{hs.get("damage_type","")},{hs.get("spectral_overlap_pct","")},{hs.get("geometric_verdict","")},"{hs.get("note","")}"'
            )
        st.download_button(
            "⬇ Hotspot CSV",
            "\n".join(csv_rows),
            "hotspots.csv",
            "text/csv",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "🗺️  Detection Map",
            "📊  Accuracy & Validation",
            "🌱  Carbon Science",
            "🌍  Ecosystem Impact",
            "📋  Full Report",
            "⚙️  Pipeline Log",
        ]
    )

    with tab1:
        render_tab_detection(final, annotated, hotspots)
    with tab2:
        render_tab_accuracy(final, hotspots)
    with tab3:
        render_tab_carbon(final)
    with tab4:
        render_tab_ecosystem(final)
    with tab5:
        render_tab_report(final)
    with tab6:
        render_tab_log(final)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;padding:24px 0 16px;border-top:1px solid #334155;">'
    '<p style="color:#64748b;font-size:0.8rem;letter-spacing:0.18em;text-transform:uppercase;margin:0;font-weight:600;">'
    "Mangrove AI Protector · LangGraph Pipeline · Team Green Flare · Eco-Tech Hackathon 2026 · Environment Watch: BUET"
    "</p></div>",
    unsafe_allow_html=True,
)
