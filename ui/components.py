from PIL import Image, ImageDraw, ImageFont

SEV_FILL = {
    "CRITICAL": (239, 68, 68, 160),
    "HIGH": (249, 115, 22, 140),
    "MODERATE": (234, 179, 8, 120),
    "LOW": (34, 197, 94, 100),
}
SEV_STROKE = {
    "CRITICAL": (248, 113, 113, 255),
    "HIGH": (253, 186, 116, 255),
    "MODERATE": (253, 224, 71, 255),
    "LOW": (134, 239, 172, 255),
}
SEV_COLOR = {
    "CRITICAL": "#ef4444",
    "HIGH": "#f97316",
    "MODERATE": "#eab308",
    "LOW": "#22c55e",
}
RISK_BG = {
    "CRITICAL": "#450a0a",
    "HIGH": "#431407",
    "MODERATE": "#422006",
    "LOW": "#052e16",
}
RISK_BORDER = {
    "CRITICAL": "#991b1b",
    "HIGH": "#9a3412",
    "MODERATE": "#854d0e",
    "LOW": "#14532d",
}
RISK_TEXT = {
    "CRITICAL": "#fca5a5",
    "HIGH": "#fdba74",
    "MODERATE": "#fde047",
    "LOW": "#86efac",
}
HEALTH_COLOR = {
    "Healthy": "#34d399",
    "Moderate Concern": "#fbbf24",
    "At Risk": "#fb923c",
    "Degraded": "#f87171",
    "Critical": "#f87171",
}

NODES_META = [
    ("validator", "N1", "Validator"),
    ("spectral", "N2", "Spectral"),
    ("detector", "N3", "Detector"),
    ("cross_val", "N4", "Cross-Val"),
    ("carbon", "N5", "Carbon"),
    ("ecosystem", "N6", "Ecosystem"),
    ("report", "N7", "Reporter"),
    ("scorer", "N8", "Scorer"),
]


def draw_boxes(base: Image.Image, hotspots: list) -> Image.Image:
    img = base.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    W, H = img.width, img.height

    try:
        fsize = max(18, int(W * 0.015))
        fsize_large = max(24, int(W * 0.02))
        font = ImageFont.truetype("arial.ttf", fsize)
        font_large = ImageFont.truetype("arial.ttf", fsize_large)
    except IOError:
        font = ImageFont.load_default()
        font_large = font

    for i, hs in enumerate(hotspots):
        ymin, xmin, ymax, xmax = hs["box_2d"]
        l = (xmin / 1000) * W
        t = (ymin / 1000) * H
        r = (xmax / 1000) * W
        b = (ymax / 1000) * H
        sev = hs.get("severity", "MODERATE").upper()
        conf = hs.get("final_confidence", hs.get("detection_confidence", "?"))
        
        box_width = max(3, int(W * 0.003))
        draw.rectangle(
            [l, t, r, b], fill=SEV_FILL.get(sev), outline=SEV_STROKE.get(sev), width=box_width
        )
        
        label = f" {sev[:3]} {conf}% "
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        pad_x, pad_y = 6, 4
        rect_w = text_w + (pad_x * 2)
        rect_h = text_h + (pad_y * 2)
        
        tl = max(0, t - rect_h)
        draw.rectangle([l, tl, l + rect_w, tl + rect_h], fill=SEV_STROKE.get(sev))
        draw.text((l + pad_x, tl + pad_y), label, fill=(15, 23, 42), font=font)
        
        zone = f"SB-{chr(65 + i)}{i + 1:02d}"
        zbox = draw.textbbox((0, 0), zone, font=font_large)
        zw = zbox[2] - zbox[0]
        zh = zbox[3] - zbox[1]
        
        draw.text((max(l + pad_x, r - zw - pad_x), max(t + pad_y, b - zh - pad_y)), zone, fill=(255, 255, 255), font=font_large)
        
    return Image.alpha_composite(img, overlay)



def pipeline_svg(done: list, active: str = "") -> str:
    n, W = len(NODES_META), 900
    svg = (
        f'<svg width="{W}" height="52" xmlns="http://www.w3.org/2000/svg" '
        f'style="overflow:visible;display:block;margin:auto">'
    )
    svg += (
        '<defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        "</filter></defs>"
    )
    cx = [int(W * (i + 0.5) / n) for i in range(n)]
    cy = 22
    for i in range(n - 1):
        d = NODES_META[i][0] in done
        c = "#059669" if d else "#334155"
        dash = "" if d else 'stroke-dasharray="4 3"'
        svg += f'<line x1="{cx[i]+16}" y1="{cy}" x2="{cx[i+1]-16}" y2="{cy}" stroke="{c}" stroke-width="2" {dash}/>'
    for i, (key, num, name) in enumerate(NODES_META):
        d = key in done
        ac = key == active
        if d:
            fill, stroke, tc, nc = "#064e3b", "#34d399", "#6ee7b7", "#a7f3d0"
        elif ac:
            fill, stroke, tc, nc = "#1e3a8a", "#60a5fa", "#bfdbfe", "#93c5fd"
        else:
            fill, stroke, tc, nc = "#0f172a", "#475569", "#94a3b8", "#64748b"
        gf = 'filter="url(#glow)"' if ac else ""
        svg += f'<circle cx="{cx[i]}" cy="{cy}" r="15" fill="{fill}" stroke="{stroke}" stroke-width="2" {gf}/>'
        if d:
            svg += f'<text x="{cx[i]}" y="{cy+5}" text-anchor="middle" font-size="12" fill="{tc}">✓</text>'
        else:
            svg += f'<text x="{cx[i]}" y="{cy+4}" text-anchor="middle" font-size="10" font-family="system-ui" fill="{tc}" font-weight="700">{num}</text>'
        svg += f'<text x="{cx[i]}" y="{cy+30}" text-anchor="middle" font-size="10" font-family="system-ui" fill="{nc}" font-weight="500">{name}</text>'
        if ac:
            svg += (
                f'<circle cx="{cx[i]}" cy="{cy}" r="20" fill="none" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.8">'
                f'<animateTransform attributeName="transform" type="rotate" from="0 {cx[i]} {cy}" to="360 {cx[i]} {cy}" dur="3s" repeatCount="indefinite"/></circle>'
            )
    svg += "</svg>"
    return svg
