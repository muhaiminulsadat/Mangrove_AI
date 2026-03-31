import time
import numpy as np
from PIL import Image, ImageFilter


def node_spectral(state) -> dict:
    t0 = time.time()
    img = state["image"]
    arr = np.array(img.convert("RGB"), dtype=np.float32)
    R, G, B = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    eps = 1e-6
    ndvi = np.clip((G - R) / (G + R + eps), -1, 1)

    water = (
        ((G > 90) & (B > 80) & (G > R * 1.25) & (B > R * 1.1))
        | ((B > 100) & (B > R * 1.3) & (G > R * 1.1))
        | ((G > 130) & (B > 110) & (R < 110))
    )
    healthy = (ndvi > 0.03) & ~water
    brown_dmg = (ndvi < -0.05) & (R > 90) & ~water
    grey_dmg = (
        (np.abs(R.astype(int) - G.astype(int)) < 30)
        & (np.abs(G.astype(int) - B.astype(int)) < 30)
        & (R > 80)
        & (R < 215)
        & ~water
        & ~healthy
    )
    damage = brown_dmg | grey_dmg

    total = R.size
    hp = float(np.sum(healthy) / total * 100)
    dp = float(np.sum(damage) / total * 100)
    wp = float(np.sum(water) / total * 100)
    sp = min(99.0, 55.0 + dp * 1.8 + float(np.std(ndvi)) * 25)

    hmap = np.zeros((*ndvi.shape, 3), dtype=np.uint8)
    hmap[healthy] = [16, 185, 129]
    hmap[damage] = [239, 68, 68]
    hmap[water] = [56, 189, 248]
    hmap[~(healthy | damage | water)] = [71, 85, 105]
    heatmap = Image.fromarray(hmap, "RGB").filter(ImageFilter.GaussianBlur(radius=2))

    elapsed = round(time.time() - t0, 2)
    return {
        "ndvi_mean": round(float(np.mean(ndvi)), 4),
        "ndvi_std": round(float(np.std(ndvi)), 4),
        "damage_pct": round(dp, 2),
        "healthy_pct": round(hp, 2),
        "water_pct": round(wp, 2),
        "spectral_conf": round(sp, 1),
        "heatmap": heatmap,
        "damage_mask": damage,
        "pipeline_log": [
            f"[Node 2 · {elapsed}s] Spectral: healthy={hp:.1f}% damage={dp:.1f}% water={wp:.1f}% (ZERO AI)"
        ],
        "done_nodes": ["spectral"],
        "timings": {"spectral": elapsed},
        "errors": [],
    }
