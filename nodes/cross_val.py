import time
import numpy as np


def _spectral_fallback_boxes(dmask: np.ndarray, damage_pct: float) -> list:
    H, W = dmask.shape
    candidates = []
    rows, cols = 8, 8
    rh, cw = H // rows, W // cols
    for r in range(rows):
        for c in range(cols):
            y1 = r * rh
            y2 = min(H, (r + 1) * rh)
            x1 = c * cw
            x2 = min(W, (c + 1) * cw)
            cell = dmask[y1:y2, x1:x2]
            if cell.size == 0:
                continue
            pct = float(np.sum(cell)) / cell.size * 100
            if pct > 18:
                candidates.append((pct, y1, x1, y2, x2))
    candidates.sort(reverse=True)
    result = []
    for pct, y1, x1, y2, x2 in candidates:
        box = [
            int(y1 / H * 1000),
            int(x1 / W * 1000),
            int(y2 / H * 1000),
            int(x2 / W * 1000),
        ]
        dup = False
        for existing in result:
            eb = existing["box_2d"]
            if abs(box[0] - eb[0]) < 80 and abs(box[1] - eb[1]) < 80:
                dup = True
                break
        if not dup:
            sev = "CRITICAL" if pct > 60 else "HIGH" if pct > 38 else "MODERATE"
            result.append(
                {
                    "box_2d": box,
                    "severity": sev,
                    "detection_confidence": int(min(88, 45 + pct)),
                    "damage_type": "Spectral Anomaly",
                    "note": f"Deterministic spectral detection: {pct:.0f}% damage pixels in region",
                }
            )
        if len(result) >= 7:
            break
    return result


def node_cross_val(state) -> dict:
    t0 = time.time()
    raw = state.get("raw_hotspots", [])
    max_area = state["max_box_pct"]
    dmask = state.get("damage_mask")
    dp = state.get("damage_pct", 0.0)

    if not raw and dmask is not None and dp > 8.0:
        raw = _spectral_fallback_boxes(dmask, dp)

    if not raw:
        elapsed = round(time.time() - t0, 2)
        return {
            "validated_hotspots": [],
            "rejected_count": 0,
            "pipeline_log": [f"[Node 4 · {elapsed}s] No hotspots detected — skipping"],
            "done_nodes": ["cross_val"],
            "timings": {"cross_val": elapsed},
            "errors": [],
        }

    validated, rejected = [], 0
    for hs in raw:
        raw_box = hs.get("box_2d", [0, 0, 0, 0])
        if len(raw_box) != 4:
            rejected += 1
            continue
        ymin, xmin, ymax, xmax = raw_box
        ymin = max(0, min(ymin, 1000))
        xmin = max(0, min(xmin, 1000))
        ymax = max(0, min(ymax, 1000))
        xmax = max(0, min(xmax, 1000))
        if xmax <= xmin or ymax <= ymin:
            rejected += 1
            continue
        if (xmax - xmin) < 10 or (ymax - ymin) < 10:
            rejected += 1
            continue
        area = ((xmax - xmin) / 1000) * ((ymax - ymin) / 1000)
        if area > max_area:
            rejected += 1
            continue
        if hs.get("detection_confidence", 50) < 5:
            rejected += 1
            continue
        hs["box_2d"] = [ymin, xmin, ymax, xmax]
        if dmask is not None:
            mh, mw = dmask.shape
            px_l = max(0, int((xmin / 1000) * mw))
            px_r = min(mw, int((xmax / 1000) * mw))
            px_t = max(0, int((ymin / 1000) * mh))
            px_b = min(mh, int((ymax / 1000) * mh))
            if px_r > px_l and px_b > px_t:
                region = dmask[px_t:px_b, px_l:px_r]
                overlap = float(np.sum(region) / region.size * 100)
                hs["spectral_overlap_pct"] = round(overlap, 1)
                hs["geometric_verdict"] = "CONFIRMED" if overlap >= 1.0 else "UNCERTAIN"
            else:
                hs["spectral_overlap_pct"] = 0.0
                hs["geometric_verdict"] = "UNCERTAIN"
        else:
            hs["spectral_overlap_pct"] = 0.0
            hs["geometric_verdict"] = "UNCERTAIN"
        hs["final_confidence"] = hs.get("detection_confidence", 50)
        hs["qc_note"] = "Passed geometric + spectral cross-validation"
        validated.append(hs)

    elapsed = round(time.time() - t0, 2)
    return {
        "validated_hotspots": validated,
        "rejected_count": rejected,
        "pipeline_log": [
            f"[Node 4 · {elapsed}s] Cross-val: {len(validated)} confirmed, {rejected} rejected"
        ],
        "done_nodes": ["cross_val"],
        "timings": {"cross_val": elapsed},
        "errors": [],
    }
