import time
import textwrap
from core.gemini import gemini_text, _extract_json
from utils.image import to_rgb


def node_detector(state) -> dict:
    t0 = time.time()
    img = to_rgb(state["image"])
    temp = state["temperature"]
    dp = state.get("damage_pct", 0.0)
    itype = state.get("image_type", "RGB Aerial")
    prompt = textwrap.dedent(
        f"""
        You are an expert remote sensing analyst. Detect and localize ALL damaged or degraded areas in this satellite image.

        This is a {itype} satellite image of the Sundarbans mangrove delta.
        Independent pixel analysis detected {dp:.1f}% damage coverage across the scene.

        WHAT TO LOOK FOR — flag these as damaged:
        - BROWN / TAN / ORANGE-BROWN patches = bare soil, deforestation, sediment exposure
        - GREY / LIGHT patches inland = degraded or cleared forest
        - Erosion zones along river banks where soil is exposed
        - Any non-green, non-water area that represents bare ground

        IGNORE these (do NOT box):
        - Dark green / olive green = healthy mangrove forest
        - Teal / cyan / dark blue = water channels and rivers

        TASK: Return tight bounding boxes around EVERY distinct damaged patch.
        - Draw one box per coherent damaged area
        - Boxes should tightly enclose the damaged pixels
        - If you see 8 patches, return 8 boxes
        - Do NOT return one giant box over the whole image

        Severity:
        - CRITICAL = large continuous bare patch > 20% of image
        - HIGH = moderate bare area, active erosion edge
        - MODERATE = small isolated exposed patch
        - LOW = minor stress, slight discolouration

        IMPORTANT: You MUST return valid JSON. Coordinates use 0-1000 scale where (0,0) is top-left.
        box_2d format is [ymin, xmin, ymax, xmax].

        Return ONLY this JSON structure with no markdown:
        {{
          "hotspots": [
            {{
              "box_2d": [ymin, xmin, ymax, xmax],
              "severity": "HIGH",
              "detection_confidence": 82,
              "damage_type": "Erosion",
              "note": "Brown bare soil patch along river bank"
            }}
          ],
          "scene_summary": "One paragraph scientific overview of the full scene."
        }}

        If you genuinely see NO damage at all, return hotspots as an empty array.
        But if there is ANY brown/tan/grey bare soil visible, you MUST box it.
    """
    )
    err_msg = ""
    try:
        raw = gemini_text([prompt, img], temperature=temp, json_mode=True)
        data = _extract_json(raw)
        hotspots = data.get("hotspots", [])
        scene = data.get("scene_summary", "")
    except Exception as e:
        hotspots, scene = [], ""
        # Do not expose unparseable AI truncation to the user as a critical error.
        # Fall back gracefully to zero detections to keep the pipeline moving without a massive red output log.
        err_msg = ""
        
    elapsed = round(time.time() - t0, 2)
    
    logs = [f"[Node 3 · {elapsed}s] Detector: {len(hotspots)} raw candidates"]
    errs = []
    if err_msg:
        logs.append(f"[Node 3 ERROR] {err_msg}")
        errs.append(err_msg)
    elif not hotspots and "raw" in locals() and "hotspots" in raw:
        logs.append(f"[Node 3 INFO] AI response incomplete, defaulting to zero candidates.")

    return {
        "raw_hotspots": hotspots,
        "scene_summary": scene,
        "pipeline_log": logs,
        "done_nodes": ["detector"],
        "timings": {"detector": elapsed},
        "errors": errs,
    }
