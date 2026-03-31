import numpy as np
from PIL import Image


def to_rgb(img: Image.Image) -> Image.Image:
    return img.convert("RGB")


def calculate_temporal_diff(img_base: Image.Image, img_curr: Image.Image):
    if img_base.size != img_curr.size:
        img_base = img_base.resize(img_curr.size)
    arr_b = np.array(img_base.convert("RGB"), dtype=np.float32)
    arr_c = np.array(img_curr.convert("RGB"), dtype=np.float32)

    def get_mask(arr):
        R, G, B = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        return (G > R * 1.05) & (G > B * 1.05) & (G > 50)

    m_b = get_mask(arr_b)
    m_c = get_mask(arr_c)
    loss = m_b & (~m_c)
    pct = float(np.sum(loss) / max(np.sum(m_b), 1) * 100)
    diff_map = np.zeros((*m_b.shape, 4), dtype=np.uint8)
    diff_map[loss] = [239, 68, 68, 220]
    return pct, Image.fromarray(diff_map, "RGBA")
