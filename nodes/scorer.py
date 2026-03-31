import time


def node_scorer(state) -> dict:
    t0 = time.time()
    hotspots = state.get("validated_hotspots", [])
    max_box = state.get("max_box_pct", 0.40)

    s1 = (
        sum(
            h.get("final_confidence", h.get("detection_confidence", 50))
            for h in hotspots
        )
        / len(hotspots)
        if hotspots
        else 95.0
    )
    if hotspots:
        confirmed = sum(
            1 for h in hotspots if h.get("geometric_verdict") == "CONFIRMED"
        )
        s2 = confirmed / len(hotspots) * 100
        tp, fp = confirmed, len(hotspots) - confirmed
    else:
        s2, tp, fp = 100.0, 0, 0
    s3 = state.get("spectral_conf", 70.0)
    s4 = float(state.get("validator_conf", 80))
    if hotspots:
        avg_area = sum(
            ((h["box_2d"][3] - h["box_2d"][1]) / 1000)
            * ((h["box_2d"][2] - h["box_2d"][0]) / 1000)
            for h in hotspots
        ) / len(hotspots)
        s5 = max(0.0, 100.0 - (avg_area / max_box) * 40)
    else:
        s5 = 100.0

    accuracy = round(
        min(99.9, s1 * 0.25 + s2 * 0.20 + s3 * 0.20 + s4 * 0.20 + s5 * 0.15), 1
    )
    breakdown = {
        "AI Detection Confidence (25%)": round(s1, 1),
        "Spectral Cross-Modal Agreement (20%)": round(s2, 1),
        "Pixel Spectral Confidence (20%)": round(s3, 1),
        "Image Validator Confidence (20%)": round(s4, 1),
        "Bounding Box Precision (15%)": round(s5, 1),
    }
    counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    for h in hotspots:
        sev = h.get("severity", "MODERATE").upper()
        counts[sev] = counts.get(sev, 0) + 1
    penalty = (
        counts["CRITICAL"] * 2.5
        + counts["HIGH"] * 1.5
        + counts["MODERATE"] * 0.7
        + counts["LOW"] * 0.2
        + state.get("defor_rate", 0) * 0.1
    )
    health = round(max(1.0, 10.0 - penalty), 1)
    status = (
        "Healthy"
        if health >= 8.5
        else (
            "Moderate Concern"
            if health >= 7.0
            else (
                "At Risk"
                if health >= 5.5
                else "Degraded" if health >= 3.5 else "Critical"
            )
        )
    )
    elapsed = round(time.time() - t0, 2)
    return {
        "accuracy_score": accuracy,
        "health_score": health,
        "health_status": status,
        "acc_breakdown": breakdown,
        "spectral_agreement": round(s2, 1),
        "tp_count": tp,
        "fp_count": fp,
        "pipeline_log": [
            f"[Node 8 · {elapsed}s] Scorer: accuracy={accuracy}% health={health}/10 ({status})"
        ],
        "done_nodes": ["scorer"],
        "timings": {"scorer": elapsed},
        "errors": [],
    }
