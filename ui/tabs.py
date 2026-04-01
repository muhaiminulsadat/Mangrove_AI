import io
import json
import streamlit as st
from datetime import datetime
from ui.charts import (
    chart_spectral_breakdown,
    chart_severity_histogram,
    chart_carbon_breakdown,
    chart_5yr_projection,
    chart_recovery_timeline,
    chart_accuracy_radar,
)
from ui.components import HEALTH_COLOR, RISK_BG, RISK_BORDER, RISK_TEXT
from utils.image import calculate_temporal_diff


def render_tab_detection(final, annotated, hotspots):
    t1a, t1b = st.columns(2)
    with t1a:
        st.markdown(
            '<div class="section-head">Annotated Damage Map</div>',
            unsafe_allow_html=True,
        )
        st.image(annotated, use_container_width=True)
    with t1b:
        hm = final.get("heatmap")
        if hm:
            st.markdown(
                '<div class="section-head">Spectral Classification — Node N2 · Zero AI</div>',
                unsafe_allow_html=True,
            )
            st.image(hm, use_container_width=True)
            st.markdown(
                """
            <div class="legend-wrap">
              <div class="leg-item"><span class="leg-dot" style="background:#10b981;"></span>Healthy Vegetation</div>
              <div class="leg-item"><span class="leg-dot" style="background:#ef4444;"></span>Detected Damage</div>
              <div class="leg-item"><span class="leg-dot" style="background:#38bdf8;"></span>Water Bodies</div>
              <div class="leg-item"><span class="leg-dot" style="background:#475569;"></span>Bare / Unclassified</div>
            </div>""",
                unsafe_allow_html=True,
            )
            st.caption(
                "Deterministic RGB channel thresholds — no AI model involved in this classification."
            )

    t1c, t1d = st.columns(2)
    with t1c:
        bare = max(
            0,
            100
            - final.get("healthy_pct", 0)
            - final.get("damage_pct", 0)
            - final.get("water_pct", 0),
        )
        st.plotly_chart(
            chart_spectral_breakdown(
                final.get("healthy_pct", 0),
                final.get("damage_pct", 0),
                final.get("water_pct", 0),
                bare,
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with t1d:
        fig_sev = chart_severity_histogram(hotspots)
        if fig_sev:
            st.plotly_chart(
                fig_sev, use_container_width=True, config={"displayModeBar": False}
            )
        else:
            st.markdown(
                '<div class="card" style="text-align:center;padding:40px 16px;"><p style="color:#94a3b8;font-size:1rem;margin:0;">No hotspots detected.</p></div>',
                unsafe_allow_html=True,
            )

    if hotspots:
        st.markdown(
            '<div class="section-head">Hotspot Registry</div>', unsafe_allow_html=True
        )
        rows_html = ""
        for i, hs in enumerate(hotspots):
            sev = hs.get("severity", "MODERATE").upper()
            note = (hs.get("note") or "—")[:90]
            dtype = hs.get("damage_type", "—")
            zone = f"SB-{chr(65+i)}{i+1:02d}"
            verdict = hs.get("geometric_verdict", "—")
            ov = hs.get("spectral_overlap_pct", "—")
            rows_html += f"""<tr>
              <td><code style="font-size:0.9rem;color:#34d399;background:transparent;">{zone}</code></td>
              <td><span class="sev-pill sev-{sev}">{sev}</span></td>
              <td style="font-weight:500;">{dtype}</td>
              <td style="font-size:0.9rem;color:#cbd5e1;max-width:250px;">{note}</td>
              <td style="font-family:'JetBrains Mono',monospace;">{ov}%</td>
              <td><span class="verdict-pill verdict-{verdict}">{verdict}</span></td>
            </tr>"""
        st.markdown(
            f'<div style="border:1px solid #334155;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.2);">'
            f'<table class="hotspot-table"><thead><tr>'
            f"<th>Zone</th><th>Severity</th><th>Damage Type</th>"
            f"<th>Observation</th><th>Spectral Overlap</th><th>Verdict</th>"
            f"</tr></thead><tbody>{rows_html}</tbody></table></div>",
            unsafe_allow_html=True,
        )
    else:
        if final.get("damage_pct", 0) > 35:
            st.warning(
                f"AI bounding boxes suppressed due to large area size, but spectral analysis indicates {final.get('damage_pct'):.1f}% potential degradation (possible sediment/mudflat misclassification).",
                icon="⚠️",
            )
        else:
            st.success(
                "No significant damage confirmed across the imaged area. Forest appears healthy.",
                icon="✅",
            )


def render_tab_accuracy(final, hotspots):
    health_score = final.get("health_score", 10)
    health_status = final.get("health_status", "Healthy")
    acc = final.get("accuracy_score", 0)
    bd = final.get("acc_breakdown", {})
    sa = final.get("spectral_agreement", 100)
    tp = final.get("tp_count", 0)
    fp = final.get("fp_count", 0)
    hc = HEALTH_COLOR.get(health_status, "#34d399")

    st.markdown(
        f"""
    <div class="kpi-row">
      <div class="kpi" style="--c:{hc}"><div class="kpi-top"></div><p class="kpi-label">Forest Health Index</p><p class="kpi-value">{health_score}<sup>/10</sup></p><p class="kpi-note" style="color:{hc};font-weight:700;">{health_status}</p></div>
      <div class="kpi" style="--c:#60a5fa"><div class="kpi-top"></div><p class="kpi-label">Confidence Score</p><p class="kpi-value">{acc}<sup>%</sup></p><p class="kpi-note">5-signal composite</p></div>
      <div class="kpi" style="--c:#2dd4bf"><div class="kpi-top"></div><p class="kpi-label">Spectral Agreement</p><p class="kpi-value">{sa:.0f}<sup>%</sup></p><p class="kpi-note">Cross-modal validation</p></div>
      <div class="kpi" style="--c:#34d399"><div class="kpi-top"></div><p class="kpi-label">Confirmed (TP)</p><p class="kpi-value">{tp}</p><p class="kpi-note">AI + spectral agree</p></div>
      <div class="kpi" style="--c:#fbbf24"><div class="kpi-top"></div><p class="kpi-label">Uncertain (FP?)</p><p class="kpi-value">{fp}</p><p class="kpi-note">Methods disagree</p></div>
      <div class="kpi" style="--c:#94a3b8"><div class="kpi-top"></div><p class="kpi-label">Pipeline Runtime</p><p class="kpi-value">{final["total_time"]}<sup>s</sup></p><p class="kpi-note">8 nodes · 2 Gemini calls</p></div>
    </div>""",
        unsafe_allow_html=True,
    )

    t2a, t2b = st.columns([3, 2])
    with t2a:
        st.markdown(
            """
        <div class="acc-note">
            <strong>Methodology — what this confidence score measures, and what it cannot.</strong><br>
            This composite measures internal consistency across five independent signals.
            <strong>Signal S2 (Spectral Cross-Modal Agreement)</strong> is the most scientifically meaningful:
            it compares Gemini Vision (probabilistic) against our deterministic numpy spectral classifier.
            Agreement between these independent methods genuinely increases detection confidence.
            Disagreements are flagged as UNCERTAIN rather than suppressed.<br><br>
            <strong>Limitation:</strong> Without labelled ground-truth annotations, absolute metrics (IoU, precision, recall)
            cannot be computed. Any claim of exact percentage accuracy on unlabelled imagery is fabricated.
            True accuracy requires: labelled data from Global Mangrove Watch → fine-tune dedicated model → IoU on held-out test set.
        </div>""",
            unsafe_allow_html=True,
        )

        bar_colors = ["#60a5fa", "#2dd4bf", "#34d399", "#fbbf24", "#fb923c"]
        bars_html = '<div class="card">'
        for idx, (label, val) in enumerate(bd.items()):
            col = bar_colors[idx % len(bar_colors)]
            bars_html += f"""<div class="bar-wrap">
              <div class="bar-meta"><span>{label}</span><span style="color:{col};font-weight:700;">{val}%</span></div>
              <div class="bar-track"><div class="bar-fill" style="width:{val}%;background:{col};"></div></div>
            </div>"""
        bars_html += f"""<div class="bar-foot">
          <span style="font-size:0.9rem;color:#94a3b8;font-weight:600;">Weighted composite score</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:700;color:#60a5fa;">{acc}%</span>
        </div></div>"""
        st.markdown(bars_html, unsafe_allow_html=True)

    with t2b:
        if bd:
            st.plotly_chart(
                chart_accuracy_radar(bd),
                use_container_width=True,
                config={"displayModeBar": False},
            )

    st.markdown(
        '<div class="section-head">Node N2 — Spectral Analysis · Zero AI</div>',
        unsafe_allow_html=True,
    )
    sm1, sm2, sm3, sm4 = st.columns(4)
    sm1.metric("Healthy Coverage", f"{final.get('healthy_pct',0):.1f}%")
    sm2.metric("Damage Coverage", f"{final.get('damage_pct',0):.1f}%")
    sm3.metric("Water Coverage", f"{final.get('water_pct',0):.1f}%")
    sm4.metric("Spectral Confidence", f"{final.get('spectral_conf',0):.1f}%")
    st.caption(
        f"Green-R NDVI mean = {final.get('ndvi_mean',0):.4f} · std = {final.get('ndvi_std',0):.4f} · image type: {final.get('image_type','?')} · validator confidence: {final.get('validator_conf',0)}%"
    )


def render_tab_carbon(final):
    st.markdown(
        '<div class="section-head">Node N5 — IPCC Tier 1 Carbon & Economic Analysis · Zero AI</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Hamilton & Friess (2018) Nature Climate Change · Sundarbans-specific biomass constants"
    )

    t3a, t3b = st.columns(2)
    with t3a:
        st.markdown(
            f"""
        <div class="card">
          <p class="card-title">Area & Deforestation Metrics</p>
          <div class="data-row"><span class="dk">Total imaged area</span><span class="dv">{final.get('total_ha',0):,.1f} ha</span></div>
          <div class="data-row"><span class="dk">Estimated damaged area</span><span class="dv" style="color:#ef4444 !important;">{final.get('damaged_ha',0):,.3f} ha</span></div>
          <div class="data-row"><span class="dk">Deforestation rate</span><span class="dv" style="color:#f97316 !important;">{final.get('defor_rate',0):.3f}%</span></div>
          <div class="data-row"><span class="dk">Pixel resolution assumed</span><span class="dv">10 m (Sentinel-2)</span></div>
        </div>
        <div class="card">
          <p class="card-title">IPCC Tier 1 Biomass Constants</p>
          <div class="data-row"><span class="dk">Aboveground biomass</span><span class="dv">180 tC / ha</span></div>
          <div class="data-row"><span class="dk">Belowground soil carbon</span><span class="dv">200 tC / ha</span></div>
          <div class="data-row"><span class="dk">Total carbon density</span><span class="dv">380 tC / ha</span></div>
          <div class="data-row"><span class="dk">CO₂ conversion factor</span><span class="dv">3.67 tCO₂ / tC</span></div>
          <div class="data-row"><span class="dk">Carbon price (VCM 2025)</span><span class="dv">৳6,158 BDT / tCO₂e</span></div>
        </div>""",
            unsafe_allow_html=True,
        )

    with t3b:
        st.markdown(
            f"""
        <div class="card">
          <p class="card-title">Carbon Impact</p>
          <div class="data-row"><span class="dk">Total carbon stock</span><span class="dv">{final.get('carbon_stock',0):,.1f} tC</span></div>
          <div class="data-row"><span class="dk">Carbon loss (estimated)</span><span class="dv" style="color:#ef4444 !important;">{final.get('carbon_loss',0):,.2f} tC</span></div>
          <div class="data-row"><span class="dk">CO₂ equivalent released</span><span class="dv" style="color:#f97316 !important;">{final.get('co2_eq',0):,.2f} tCO₂e</span></div>
        </div>
        <div class="card">
          <p class="card-title">Economic Valuation</p>
          <div class="data-row"><span class="dk">Carbon credit loss</span><span class="dv" style="color:#fbbf24 !important;">৳{final.get('econ_loss_bdt',0):,.2f} BDT</span></div>
          <div class="data-row"><span class="dk">Ecosystem services value</span><span class="dv">~৳40.6 Lakh–৳2.39 Crore / ha / yr</span></div>
          <div class="data-row"><span class="dk">Blue carbon premium</span><span class="dv">Highest of any ecosystem</span></div>
          <div class="data-row"><span class="dk">Restoration cost estimate</span><span class="dv">~৳2.46 Lakh–৳9.85 Lakh / ha</span></div>
        </div>""",
            unsafe_allow_html=True,
        )

    t3c, t3d = st.columns(2)
    with t3c:
        st.plotly_chart(
            chart_carbon_breakdown(
                final.get("carbon_stock", 0),
                final.get("carbon_loss", 0),
                final.get("co2_eq", 0),
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with t3d:
        proj = final.get("carbon_5yr_projection", [])
        if proj:
            st.plotly_chart(
                chart_5yr_projection(proj, final.get("annual_seq_loss", 0)),
                use_container_width=True,
                config={"displayModeBar": False},
            )

    st.info(
        "IPCC Tier 1 default values used. Field measurements + Tier 2/3 required for policy. Nodes N5 and N6 make ZERO AI calls — results are fully deterministic and reproducible."
    )


def render_tab_ecosystem(final):
    st.markdown(
        '<div class="section-head">Node N6 — Ecosystem Impact Model · Zero AI</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Biodiversity, coastal protection, annual sequestration loss, recovery trajectory modelling"
    )

    t4a, t4b = st.columns(2)
    with t4a:
        em1, em2 = st.columns(2)
        em1.metric("Species at Risk", str(final.get("species_at_risk", 0)))
        em2.metric("Habitat Loss Index", f"{final.get('habitat_loss_index', 0):.2f}%")
        em3, em4 = st.columns(2)
        em3.metric("Coastline at Risk", f"{final.get('coastal_km_at_risk', 0):.2f} km")
        em4.metric(
            "Annual Seq. Loss", f"{final.get('annual_seq_loss', 0):.1f} tCO₂e/yr"
        )

        st.markdown(
            f"""
        <div class="card">
          <p class="card-title">Ecosystem Services Impact</p>
          <div class="data-row"><span class="dk">Annual sequestration capacity lost</span><span class="dv" style="color:#ef4444 !important;">{final.get('annual_seq_loss',0):.2f} tCO₂e/yr</span></div>
          <div class="data-row"><span class="dk">Ecosystem services value lost</span><span class="dv" style="color:#fbbf24 !important;">৳{final.get('ecosystem_services_bdt',0):,.0f} BDT/yr</span></div>
          <div class="data-row"><span class="dk">Species density reference</span><span class="dv">341 species per 100 ha</span></div>
          <div class="data-row"><span class="dk">Coastal protection ratio</span><span class="dv">0.5 km per ha</span></div>
        </div>
        <div class="card">
          <p class="card-title">Recovery Timeline Projection</p>
          <div class="data-row"><span class="dk">Natural recovery to 90% canopy</span><span class="dv" style="color:#94a3b8 !important;">{final.get('recovery_years_natural',0):.0f} years</span></div>
          <div class="data-row"><span class="dk">Assisted restoration to 90%</span><span class="dv" style="color:#34d399 !important;">{final.get('recovery_years_assisted',0):.0f} years</span></div>
          <div class="data-row"><span class="dk">Natural recovery rate</span><span class="dv">8% canopy / year</span></div>
          <div class="data-row"><span class="dk">Assisted recovery rate</span><span class="dv">22% canopy / year</span></div>
        </div>""",
            unsafe_allow_html=True,
        )

    with t4b:
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(
            chart_recovery_timeline(
                final.get("recovery_years_natural", 29),
                final.get("recovery_years_assisted", 10),
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        reduction = max(
            0,
            (
                1
                - final.get("recovery_years_assisted", 10)
                / max(final.get("recovery_years_natural", 29), 1)
            )
            * 100,
        )
        st.markdown(
            f"""
        <div class="card" style="background:#422006;border-color:#9a3412;">
          <p class="card-title" style="color:#fdba74 !important;border-bottom-color:#7c2d12 !important;">Key Ecological Takeaway</p>
          <p style="font-size:1.05rem;color:#fed7aa !important;line-height:1.8;margin:0;">
            Mangroves represent the highest carbon density of any terrestrial ecosystem. Their loss creates a
            double climate penalty: both immediate release of stored carbon and permanent loss of future
            sequestration capacity. The <strong>assisted restoration scenario</strong> reduces recovery time by
            approximately {reduction:.0f}% compared to passive natural recovery, underscoring the economic
            case for active intervention programs.
          </p>
        </div>""",
            unsafe_allow_html=True,
        )


def render_tab_report(final):
    r5a, r5b = st.columns([3, 2])
    with r5a:
        st.markdown(
            '<div class="section-head">Scientific Environmental Assessment</div>',
            unsafe_allow_html=True,
        )
        assessment_text = final.get("assessment", "")
        if assessment_text:
            paras = [p.strip() for p in assessment_text.split("\n\n") if p.strip()]
            body_html = "".join(f"<p>{p}</p>" for p in paras)
            st.markdown(
                f'<div class="assessment-prose">{body_html}</div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            f'<div class="meta-panel">'
            f'<span class="meta-k">IMAGE TYPE &nbsp;&nbsp;</span>{final.get("image_type","—")}<br>'
            f'<span class="meta-k">RISK LEVEL &nbsp;&nbsp;</span>{final.get("risk_level","—")}<br>'
            f'<span class="meta-k">GENERATED &nbsp;&nbsp; </span>{datetime.now().strftime("%Y-%m-%d %H:%M UTC")}<br>'
            f'<span class="meta-k">PIPELINE &nbsp;&nbsp;&nbsp;&nbsp;</span>LangGraph StateGraph · 8 nodes<br>'
            f'<span class="meta-k">AI MODEL &nbsp;&nbsp;&nbsp;&nbsp;</span>gemini-2.5-flash · prototype stand-in<br>'
            f'<span class="meta-k">TEAM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>Green Flare · Eco-Tech Hackathon 2026 · BUET'
            f"</div>",
            unsafe_allow_html=True,
        )
    with r5b:
        st.markdown(
            '<div class="section-head">Action Plan</div>', unsafe_allow_html=True
        )
        actions = final.get("actions", [])
        if actions:
            acts_html = ""
            for i, a in enumerate(actions, 1):
                acts_html += f'<div class="action-item"><span class="action-num">{i:02d}</span><span class="action-txt">{a}</span></div>'
            st.markdown(acts_html, unsafe_allow_html=True)



def render_tab_log(final):
    st.markdown(
        '<div class="section-head">LangGraph Execution Log</div>',
        unsafe_allow_html=True,
    )
    logs = final.get("pipeline_log", [])
    log_html = '<div class="log-wrap">'
    for line in logs:
        if "error" in line.lower():
            lc = "#ef4444"
        elif "ZERO AI" in line or "IPCC" in line:
            lc = "#34d399"
        elif "Node" in line:
            lc = "#60a5fa"
        else:
            lc = "#94a3b8"
        log_html += f'<div class="log-line" style="color:{lc};">{line}</div>'
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)



    errs = final.get("errors", [])
    if errs:
        with st.expander(f"⚠️ Pipeline warnings ({len(errs)})"):
            for err in errs:
                st.markdown(
                    f'<div style="background:#450a0a;border:1px solid #991b1b;border-radius:8px;padding:12px 16px;font-size:0.95rem;color:#fca5a5;margin-bottom:8px;">{err}</div>',
                    unsafe_allow_html=True,
                )


def render_tab_temporal(final, img_in, img_baseline):
    st.markdown(
        '<div class="section-head">Temporal Degradation Analysis</div>',
        unsafe_allow_html=True,
    )
    if img_baseline:
        loss_pct, loss_map = calculate_temporal_diff(img_baseline, img_in)
        st.metric("Deterministic Canopy Loss vs. Baseline", f"{loss_pct:.2f}%")
        base_col, curr_col = st.columns(2)
        with base_col:
            st.markdown(
                '<div class="card-title">Past Baseline Image</div>',
                unsafe_allow_html=True,
            )
            st.image(img_baseline, use_container_width=True)
        with curr_col:
            st.markdown(
                '<div class="card-title">Current Image (Loss Highlighted)</div>',
                unsafe_allow_html=True,
            )
            overlay = img_in.convert("RGBA").copy()
            overlay.alpha_composite(loss_map)
            st.image(overlay, use_container_width=True)
    else:
        st.info(
            "Upload a past/baseline image in the sidebar to activate the temporal comparison engine.",
            icon="⏳",
        )
