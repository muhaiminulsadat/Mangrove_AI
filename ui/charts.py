import numpy as np
import plotly.graph_objects as go


def make_plotly_theme():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="system-ui, -apple-system, sans-serif", size=14, color="#e2e8f0"
        ),
        margin=dict(l=0, r=0, t=35, b=0),
    )


def chart_spectral_breakdown(healthy, damage, water, bare):
    fig = go.Figure(
        go.Pie(
            labels=[
                "Healthy Vegetation",
                "Detected Damage",
                "Water Bodies",
                "Bare / Unclassified",
            ],
            values=[
                max(healthy, 0.1),
                max(damage, 0.1),
                max(water, 0.1),
                max(bare, 0.1),
            ],
            hole=0.6,
            marker=dict(
                colors=["#10b981", "#ef4444", "#38bdf8", "#64748b"],
                line=dict(color="#1e293b", width=3),
            ),
            textinfo="percent",
            textfont=dict(size=14, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        **make_plotly_theme(),
        height=300,
        showlegend=True,
        legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=12, color="#e2e8f0")),
    )
    fig.add_annotation(
        text=f"<b>{damage:.1f}%</b><br>Degraded",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="#fca5a5"),
        align="center",
    )
    return fig


def chart_carbon_breakdown(carbon_stock, carbon_loss, co2_eq):
    remaining = max(carbon_stock - carbon_loss, 0)
    fig = go.Figure(
        go.Pie(
            labels=["Remaining Carbon Stock", "Carbon Lost", "CO₂ Equivalent Released"],
            values=[remaining, carbon_loss, co2_eq - carbon_loss * 3.67 + co2_eq],
            hole=0.55,
            marker=dict(
                colors=["#10b981", "#ef4444", "#f97316"],
                line=dict(color="#1e293b", width=3),
            ),
            textinfo="percent",
            textfont=dict(size=13, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>%{value:,.1f} tC<extra></extra>",
        )
    )
    fig.update_layout(
        **make_plotly_theme(),
        height=280,
        showlegend=True,
        legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=12, color="#e2e8f0")),
    )
    return fig


def chart_5yr_projection(projection, annual_seq_loss):
    years = [f"Year {i}" for i in range(1, 6)]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=years,
            y=projection,
            marker=dict(
                color=["#fca5a5", "#f87171", "#ef4444", "#dc2626", "#991b1b"],
                line=dict(color="#1e293b", width=2),
            ),
            name="Cumulative CO₂ loss",
            hovertemplate="<b>%{x}</b><br>%{y:,.1f} tCO₂e lost<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=projection,
            mode="lines+markers",
            line=dict(color="#fecaca", width=3, dash="dot"),
            marker=dict(size=8, color="#fecaca"),
            showlegend=False,
        )
    )
    fig.update_layout(
        **make_plotly_theme(),
        height=260,
        yaxis=dict(
            title=dict(text="Cumulative tCO₂e", font=dict(size=13)), gridcolor="#334155"
        ),
        xaxis=dict(gridcolor="#334155"),
        title=dict(
            text=f"5-Year Carbon Sequestration Loss Projection ({annual_seq_loss:.1f} tCO₂e/yr)",
            font=dict(size=14, color="#f8fafc"),
        ),
    )
    return fig


def chart_recovery_timeline(recovery_natural, recovery_assisted):
    years_nat = np.linspace(0, recovery_natural * 1.2, 60)
    years_ast = np.linspace(0, recovery_assisted * 1.5, 60)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years_nat,
            y=100 * (1 - np.exp(-0.08 * years_nat)),
            mode="lines",
            name="Natural Recovery",
            line=dict(color="#94a3b8", width=3),
            fill="tozeroy",
            fillcolor="rgba(148,163,184,0.15)",
            hovertemplate="Year %{x:.0f}: %{y:.0f}% recovered<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years_ast,
            y=100 * (1 - np.exp(-0.22 * years_ast)),
            mode="lines",
            name="Assisted Restoration",
            line=dict(color="#34d399", width=3.5),
            fill="tozeroy",
            fillcolor="rgba(52,211,153,0.15)",
            hovertemplate="Year %{x:.0f}: %{y:.0f}% recovered<extra></extra>",
        )
    )
    fig.add_hline(
        y=90,
        line_dash="dot",
        line_color="#cbd5e1",
        annotation_text="90% recovery threshold",
        annotation_font_size=12,
        annotation_font_color="#f8fafc",
    )
    fig.update_layout(
        **make_plotly_theme(),
        height=280,
        yaxis=dict(
            title=dict(text="Canopy Recovery (%)", font=dict(size=13)),
            range=[0, 105],
            gridcolor="#334155",
        ),
        xaxis=dict(title=dict(text="Years", font=dict(size=13)), gridcolor="#334155"),
        legend=dict(x=0.6, y=0.2, font=dict(size=12, color="#e2e8f0")),
        title=dict(
            text="Mangrove Recovery Trajectory Model",
            font=dict(size=14, color="#f8fafc"),
        ),
    )
    return fig


def chart_accuracy_radar(breakdown):
    labels = [
        "AI Conf.",
        "Spectral Agree.",
        "Pixel Conf.",
        "Validator Conf.",
        "Box Precision",
    ]
    values = list(breakdown.values())
    fig = go.Figure(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor="rgba(52,211,153,0.2)",
            line=dict(color="#34d399", width=3),
            marker=dict(size=6, color="#10b981"),
            hovertemplate="<b>%{theta}</b><br>%{r:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="system-ui", size=12, color="#e2e8f0"),
        margin=dict(l=50, r=50, t=50, b=50),
        height=320,
        polar=dict(
            bgcolor="#0f172a",
            radialaxis=dict(
                range=[0, 100],
                showticklabels=True,
                tickfont=dict(size=11, color="#94a3b8"),
                gridcolor="#334155",
                linecolor="#475569",
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color="#f8fafc", weight="bold"),
                linecolor="#475569",
                gridcolor="#334155",
            ),
        ),
    )
    return fig


def chart_severity_histogram(hotspots):
    if not hotspots:
        return None
    sev_order = ["CRITICAL", "HIGH", "MODERATE", "LOW"]
    sev_colors = {
        "CRITICAL": "#ef4444",
        "HIGH": "#f97316",
        "MODERATE": "#eab308",
        "LOW": "#22c55e",
    }
    counts = {s: 0 for s in sev_order}
    for hs in hotspots:
        s = hs.get("severity", "MODERATE").upper()
        counts[s] = counts.get(s, 0) + 1
    active = [s for s in sev_order if counts[s] > 0]
    if not active:
        return None
    fig = go.Figure(
        go.Bar(
            x=active,
            y=[counts[s] for s in active],
            marker=dict(
                color=[sev_colors[s] for s in active],
                line=dict(color="#1e293b", width=2),
            ),
            hovertemplate="<b>%{x}</b><br>%{y} hotspot(s)<extra></extra>",
        )
    )
    fig.update_layout(
        **make_plotly_theme(),
        height=240,
        yaxis=dict(
            gridcolor="#334155",
            tickformat="d",
            title=dict(text="Count", font=dict(size=12)),
        ),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=13, color="#f8fafc")),
        title=dict(
            text="Hotspot Severity Distribution", font=dict(size=14, color="#f8fafc")
        ),
    )
    return fig
