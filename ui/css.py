import streamlit as st


def inject_css():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.stApp { background-color: #0f172a; color: #f8fafc; }
section[data-testid="stSidebar"] { background: #1e293b; border-right: 1px solid #334155; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-top: 2rem !important; }
section[data-testid="stSidebar"] .block-container { padding-top: 2rem !important; }
.stApp > header { background: transparent; }
h1, h2, h3, h4, h5, h6, .card-title, .section-head { color: #f8fafc !important; font-family: 'Inter', sans-serif; letter-spacing: -0.01em; }
p, span, div { color: #e2e8f0; }
.project-header { background: linear-gradient(135deg, #1e293b 0%, #064e3b 100%); border: 1px solid #059669; border-radius: 16px; padding: 40px 48px; margin-bottom: 32px; display: flex; align-items: flex-start; justify-content: space-between; gap: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
.project-header-left h1 { font-size: 2.4rem !important; font-weight: 700; color: #34d399 !important; margin: 0 0 10px; letter-spacing: -0.03em; line-height: 1.2; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
.project-header-left p { color: #cbd5e1 !important; font-size: 1.05rem; margin: 0 0 24px; line-height: 1.6; max-width: 800px; }
.header-badges { display: flex; flex-wrap: wrap; gap: 10px; }
.hbadge { background: #064e3b; border: 1px solid #059669; color: #6ee7b7; font-size: 0.85rem; font-weight: 600; padding: 5px 14px; border-radius: 20px; white-space: nowrap; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
.hbadge-gray { background: #334155; border: 1px solid #475569; color: #cbd5e1; font-size: 0.85rem; font-weight: 500; padding: 5px 14px; border-radius: 20px; white-space: nowrap; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
.project-header-right { text-align: right; flex-shrink: 0; }
.team-badge { background: #10b981; color: #022c22; font-size: 0.9rem; font-weight: 700; padding: 8px 18px; border-radius: 8px; letter-spacing: 0.05em; margin-bottom: 10px; display: inline-block; box-shadow: 0 4px 12px rgba(16,185,129,0.3); }
.hackathon-label { font-size: 0.8rem; color: #94a3b8; display: block; margin-top: 8px; font-weight: 500; }
.pipeline-wrap { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px 28px 16px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.pipeline-title { font-size: 0.8rem; font-weight: 700; color: #94a3b8 !important; letter-spacing: 0.18em; text-transform: uppercase; margin: 0 0 16px; }
.status-line { display: flex; align-items: center; gap: 12px; background: #064e3b; border: 1px solid #059669; border-radius: 8px; padding: 12px 20px; font-size: 1rem; color: #34d399 !important; margin-bottom: 20px; font-weight: 500; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.status-dot { width: 10px; height: 10px; background: #34d399; border-radius: 50%; flex-shrink: 0; animation: blink 1.2s ease-in-out infinite; box-shadow: 0 0 8px #34d399; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
.kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin: 24px 0; }
.kpi { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px 24px; position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.2s, box-shadow 0.2s; }
.kpi:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); border-color: #475569; }
.kpi-top { width: 100%; height: 4px; border-radius: 99px; background: var(--c, #34d399); margin-bottom: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
.kpi-label { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8 !important; margin: 0 0 10px; }
.kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: var(--c, #f8fafc) !important; line-height: 1; margin: 0; }
.kpi-value sup { font-size: 1.1rem; font-weight: 500; opacity: 0.7; margin-left: 4px; }
.kpi-note { font-size: 0.85rem; color: #cbd5e1 !important; margin: 8px 0 0; font-weight: 500; }
.section-head { font-size: 0.85rem !important; font-weight: 700 !important; letter-spacing: 0.16em !important; text-transform: uppercase !important; color: #cbd5e1 !important; margin: 32px 0 16px !important; padding-bottom: 12px !important; border-bottom: 1px solid #334155 !important; display: flex !important; align-items: center !important; gap: 12px !important; }
.section-head span { color: #475569 !important; }
.card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
.card-title { font-size: 0.9rem !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.14em !important; color: #94a3b8 !important; margin: 0 0 16px !important; padding-bottom: 12px !important; border-bottom: 1px solid #334155 !important; }
.data-row { display: flex; justify-content: space-between; align-items: baseline; padding: 10px 0; border-bottom: 1px solid #0f172a; }
.data-row:last-child { border-bottom: none; }
.dk { font-size: 0.95rem; color: #cbd5e1 !important; font-weight: 500; }
.dv { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 600; color: #f8fafc !important; }
.risk-box { border-radius: 10px; padding: 16px 24px; margin-bottom: 20px; display: flex; align-items: flex-start; gap: 16px; border: 1px solid var(--rb, #059669); background: var(--rg, #064e3b); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.risk-icon { font-size: 1.4rem; flex-shrink: 0; margin-top: 2px; }
.risk-txt { font-size: 1.05rem; color: var(--rt, #6ee7b7) !important; line-height: 1.6; font-weight: 500; }
.risk-txt strong { color: #ffffff !important; }
.proto-note { background: #422006; border: 1px solid #9a3412; border-radius: 10px; padding: 16px 24px; font-size: 0.95rem; color: #fdba74 !important; line-height: 1.7; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.proto-note strong { color: #fff !important; font-weight: 700; }
.hotspot-table { width: 100%; border-collapse: collapse; font-size: 0.95rem; background: #1e293b; }
.hotspot-table th { background: #0f172a; padding: 14px 18px; text-align: left; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8; border-bottom: 2px solid #334155; }
.hotspot-table td { padding: 16px 18px; border-bottom: 1px solid #334155; color: #e2e8f0; vertical-align: top; line-height: 1.5; }
.hotspot-table tr:last-child td { border-bottom: none; }
.hotspot-table tbody tr:hover td { background: #334155; }
.sev-pill { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.sev-CRITICAL { background: #7f1d1d; color: #fca5a5 !important; border: 1px solid #991b1b; }
.sev-HIGH { background: #7c2d12; color: #fdba74 !important; border: 1px solid #9a3412; }
.sev-MODERATE { background: #713f12; color: #fde047 !important; border: 1px solid #854d0e; }
.sev-LOW { background: #14532d; color: #86efac !important; border: 1px solid #166534; }
.verdict-pill { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.verdict-CONFIRMED { background: #064e3b; color: #6ee7b7 !important; border: 1px solid #059669; }
.verdict-UNCERTAIN { background: #422006; color: #fdba74 !important; border: 1px solid #9a3412; }
.acc-note { background: #1e3a8a; border: 1px solid #1e40af; border-radius: 10px; padding: 18px 24px; font-size: 0.95rem; color: #bfdbfe !important; line-height: 1.7; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.acc-note strong { color: #ffffff !important; }
.bar-wrap { margin-bottom: 16px; }
.bar-meta { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.9rem; color: #cbd5e1 !important; font-weight: 500; }
.bar-track { height: 8px; background: #0f172a; border-radius: 99px; overflow: hidden; border: 1px solid #334155; }
.bar-fill { height: 100%; border-radius: 99px; box-shadow: 0 0 10px rgba(255,255,255,0.2); }
.bar-foot { border-top: 1px solid #334155; padding-top: 16px; margin-top: 12px; display: flex; justify-content: space-between; align-items: center; }
.assessment-prose { background: #1e293b; border: 1px solid #334155; border-left: 4px solid #34d399; border-radius: 0 12px 12px 0; padding: 28px 32px; font-size: 1.05rem; line-height: 1.9; color: #f8fafc !important; margin-bottom: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
.assessment-prose p { margin: 0 0 1.2em; color: #f8fafc !important; }
.assessment-prose p:last-child { margin-bottom: 0; }
.action-item { display: flex; gap: 16px; align-items: flex-start; background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 16px 20px; margin-bottom: 10px; transition: border-color 0.2s, box-shadow 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.action-item:hover { border-color: #059669; box-shadow: 0 4px 12px rgba(52,211,153,0.15); }
.action-num { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; font-weight: 700; color: #34d399 !important; min-width: 28px; padding-top: 2px; }
.action-txt { font-size: 1rem; color: #e2e8f0 !important; line-height: 1.6; font-weight: 500; }
.meta-panel { background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 20px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #cbd5e1 !important; line-height: 2.2; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1); }
.meta-k { color: #64748b !important; font-weight: 600; }
.log-wrap { background: #020617; border: 1px solid #1e293b; border-radius: 10px; padding: 20px; font-family: 'JetBrains Mono', monospace; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5); }
.log-line { font-size: 0.85rem; padding: 5px 0; border-bottom: 1px solid #1e293b; line-height: 1.6; }
.log-line:last-child { border-bottom: none; }
.scene-box { background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 20px 24px; font-size: 1rem; color: #cbd5e1 !important; line-height: 1.8; margin-top: 12px; font-style: italic; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border-left: 4px solid #3b82f6; }
.legend-wrap { display: flex; flex-wrap: wrap; gap: 20px; padding: 12px 0; }
.leg-item { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; color: #cbd5e1 !important; font-weight: 500; }
.leg-dot { width: 14px; height: 14px; border-radius: 4px; flex-shrink: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.stButton > button { background: #10b981 !important; color: #022c22 !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 1.05rem !important; letter-spacing: 0.02em !important; height: 3.2em !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #34d399 !important; transform: translateY(-2px); }
.stDownloadButton > button { background: #1e293b !important; color: #f8fafc !important; border: 1px solid #475569 !important; border-radius: 10px !important; font-size: 0.95rem !important; font-weight: 600 !important; transition: all 0.2s !important; }
.stDownloadButton > button:hover { border-color: #34d399 !important; color: #34d399 !important; background: #0f172a !important; }
div[data-testid="stTabs"] [role="tablist"] { border-bottom: 2px solid #334155; }
div[data-testid="stTabs"] button { font-size: 1rem !important; font-weight: 600 !important; color: #94a3b8 !important; padding: 12px 16px !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #34d399 !important; border-bottom-color: #34d399 !important; background: transparent !important; }
div[data-testid="stMetric"] { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
div[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.9rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.05em; }
div[data-testid="stMetricValue"] { font-weight: 700 !important; color: #f8fafc !important; font-family: 'JetBrains Mono', monospace; font-size: 2.2rem !important; }
div[data-testid="stExpander"] { background: #1e293b; border: 1px solid #334155 !important; border-radius: 10px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
div[data-testid="stExpander"] p { color: #e2e8f0 !important; font-size: 1rem !important; font-weight: 500 !important; }
.sidebar-label { font-size: 0.8rem !important; font-weight: 700 !important; letter-spacing: 0.16em !important; text-transform: uppercase !important; color: #94a3b8 !important; margin: 12px 0 12px !important; display: block !important; border-bottom: 1px solid #334155; padding-bottom: 6px; }
hr { border-color: #334155 !important; }
.stRadio label { color: #cbd5e1 !important; font-size: 0.95rem !important; font-weight: 500 !important; }
.stSlider label { color: #cbd5e1 !important; font-size: 0.95rem !important; font-weight: 500 !important; }
.stFileUploader label { color: #cbd5e1 !important; font-size: 0.95rem !important; font-weight: 500 !important; }
</style>""",
        unsafe_allow_html=True,
    )
