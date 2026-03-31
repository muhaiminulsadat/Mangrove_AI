import time
import textwrap
from core.gemini import gemini_text, _extract_json
from utils.image import to_rgb


def node_validator(state) -> dict:
    t0 = time.time()
    img = to_rgb(state["image"])
    prompt = textwrap.dedent(
        """
        Look at this image. Return ONLY a JSON object:
        {
          "is_satellite": true or false,
          "image_type": "RGB Aerial | False Color Infrared | NDVI | Multispectral | Unknown",
          "confidence": 0-100,
          "note": "one sentence"
        }
        Accept: satellite photos, aerial imagery, FCI, NDVI, Google Earth exports, any overhead view of land or water.
    """
    )
    err_msg = ""
    try:
        raw = gemini_text([prompt, img], temperature=0.1, json_mode=True)
        data = _extract_json(raw)
        valid = bool(data.get("is_satellite", False))
        img_type = str(data.get("image_type", "Unknown"))
        conf = int(data.get("confidence", 0))
        note = str(data.get("note", ""))
    except Exception as e:
        valid, img_type, conf, note = False, "Unknown", 0, ""
        err_msg = f"Validator API Error: {str(e)[:150]}"
        
    elapsed = round(time.time() - t0, 2)
    
    logs = [f"[Node 1 · {elapsed}s] Validator: {img_type} valid={valid} conf={conf}%"]
    errs = []
    
    if not valid and not err_msg:
        errs.append(f"Image rejected: {note}")
        
    if err_msg:
        logs.append(f"[Node 1 ERROR] {err_msg}")
        errs.append(err_msg)

    return {
        "is_valid": valid,
        "image_type": img_type,
        "validator_conf": conf,
        "validator_note": note,
        "pipeline_log": logs,
        "done_nodes": ["validator"],
        "timings": {"validator": elapsed},
        "errors": errs,
    }
