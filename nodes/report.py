import time
import json
import textwrap
from core.gemini import gemini_text, _extract_json


def node_report(state) -> dict:
    t0 = time.time()
    hotspots = state.get("validated_hotspots", [])
    counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    for hs in hotspots:
        sev = hs.get("severity", "MODERATE").upper()
        counts[sev] = counts.get(sev, 0) + 1
    ctx = {
        "image_type": state.get("image_type"),
        "total_hotspots": len(hotspots),
        "severity_counts": counts,
        "healthy_pct": round(state.get("healthy_pct", 0), 1),
        "damage_pct": round(state.get("damage_pct", 0), 1),
        "ndvi_mean": round(state.get("ndvi_mean", 0), 3),
        "damaged_ha": state.get("damaged_ha", 0),
        "carbon_loss_tc": state.get("carbon_loss", 0),
        "co2_eq_tc": state.get("co2_eq", 0),
        "economic_bdt": state.get("econ_loss_bdt", 0),
        "defor_rate_pct": round(state.get("defor_rate", 0), 2),
        "species_at_risk": state.get("species_at_risk", 0),
        "coastal_km_at_risk": state.get("coastal_km_at_risk", 0),
        "hotspot_notes": [h.get("note", "") for h in hotspots[:5]],
    }
    prompt = textwrap.dedent(
        f"""
        You are a senior environmental scientist writing a formal satellite-based assessment.
        Data from multi-node analysis pipeline:
        {json.dumps(ctx, indent=2)}

        Return ONLY this JSON (no markdown):
        {{
          "paragraphs": [
            "Para 1 (3 sentences): Current forest health from spectral and visual analysis.",
            "Para 2 (3 sentences): Threats, damage patterns, ecological significance.",
            "Para 3 (2 sentences): Carbon impact and climate implications.",
            "Para 4 (2 sentences): Biodiversity and coastal protection implications.",
            "Para 5 (2 sentences): Urgency and conservation outlook."
          ],
          "actions": [
            "Immediate (0-30 days): specific action",
            "Short-term (1-6 months): specific action",
            "Medium-term (6-24 months): specific action",
            "Long-term (2-5 years): specific action"
          ],
          "risk_level": "LOW|MODERATE|HIGH|CRITICAL",
          "alert": "One urgent line if HIGH/CRITICAL, else empty string"
        }}
        Use real numbers from the data. Be scientific and direct. No fluff.
    """
    )
    err_msg = ""
    try:
        raw = gemini_text([prompt], temperature=0.35, json_mode=True)
        data = _extract_json(raw)
        assessment = "\n\n".join(data.get("paragraphs", []))
        actions = data.get("actions", [])
        risk = data.get("risk_level", "MODERATE").upper()
        alert = data.get("alert", "")
    except Exception as e:
        assessment = ""
        actions, risk, alert = [], "MODERATE", ""
        err_msg = f"Report API Error: {str(e)[:150]}"
        
    elapsed = round(time.time() - t0, 2)
    
    logs = [f"[Node 7 · {elapsed}s] Report: risk={risk}, {len(actions)} actions"]
    errs = []
    if err_msg:
        logs.append(f"[Node 7 ERROR] {err_msg}")
        errs.append(err_msg)

    return {
        "assessment": assessment,
        "actions": actions,
        "risk_level": risk,
        "alert_msg": alert,
        "pipeline_log": logs,
        "done_nodes": ["report"],
        "timings": {"report": elapsed},
        "errors": errs,
    }
