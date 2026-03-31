import time


def node_carbon(state) -> dict:
    t0 = time.time()
    W, H = state.get("image_width", 1000), state.get("image_height", 1000)
    dp = state.get("damage_pct", 0.0)
    hotspots = state.get("validated_hotspots", [])
    total_ha = (W * H * 100) / 10_000
    px_frac = dp / 100.0
    if hotspots:
        hs_frac = sum(
            ((h["box_2d"][3] - h["box_2d"][1]) / 1000)
            * ((h["box_2d"][2] - h["box_2d"][0]) / 1000)
            for h in hotspots
        )
        dmg_frac = min(1.0, hs_frac * 0.60 + px_frac * 0.40)
    else:
        dmg_frac = px_frac
    dmg_ha = total_ha * dmg_frac
    CARBON_DENS = 380.0
    carbon_stock = total_ha * CARBON_DENS
    carbon_loss = dmg_ha * CARBON_DENS
    co2_eq = carbon_loss * 3.67
    econ_loss = co2_eq * 50.0 * 123.16
    defor_rate = dmg_frac * 100.0
    elapsed = round(time.time() - t0, 2)
    return {
        "total_ha": round(total_ha, 1),
        "damaged_ha": round(dmg_ha, 3),
        "carbon_stock": round(carbon_stock, 1),
        "carbon_loss": round(carbon_loss, 2),
        "co2_eq": round(co2_eq, 2),
        "econ_loss_bdt": round(econ_loss, 2),
        "defor_rate": round(defor_rate, 3),
        "pipeline_log": [
            f"[Node 5 · {elapsed}s] Carbon: {carbon_loss:.1f} tC lost · ৳{econ_loss:,.0f} BDT (IPCC Tier 1, ZERO AI)"
        ],
        "done_nodes": ["carbon"],
        "timings": {"carbon": elapsed},
        "errors": [],
    }
