import time
import math


def node_ecosystem(state) -> dict:
    t0 = time.time()
    dmg_ha = state.get("damaged_ha", 0.0)
    total_ha = max(state.get("total_ha", 1.0), 1.0)

    SPECIES_PER_100HA = 341
    COASTAL_PROTECTION_RATIO = 0.5
    ANNUAL_SEQ_RATE = 6.1
    ECOSYSTEM_SERVICES_PER_HA = 37500 * 123.16
    NATURAL_RECOVERY_RATE = 0.08
    ASSISTED_RECOVERY_RATE = 0.22

    species_at_risk = int((dmg_ha / 100.0) * SPECIES_PER_100HA)
    habitat_loss_idx = round(dmg_ha / total_ha * 100, 2)
    coastal_km = round(dmg_ha * COASTAL_PROTECTION_RATIO, 3)
    recovery_natural = (
        round(-math.log(0.1) / NATURAL_RECOVERY_RATE, 1) if dmg_ha > 0 else 0.0
    )
    recovery_assisted = (
        round(-math.log(0.1) / ASSISTED_RECOVERY_RATE, 1) if dmg_ha > 0 else 0.0
    )
    annual_seq_loss = round(dmg_ha * ANNUAL_SEQ_RATE, 2)
    ecosystem_svc = round(dmg_ha * ECOSYSTEM_SERVICES_PER_HA, 2)
    projection = [round(annual_seq_loss * yr, 2) for yr in range(1, 6)]

    elapsed = round(time.time() - t0, 2)
    return {
        "species_at_risk": species_at_risk,
        "habitat_loss_index": habitat_loss_idx,
        "coastal_km_at_risk": coastal_km,
        "recovery_years_natural": recovery_natural,
        "recovery_years_assisted": recovery_assisted,
        "annual_seq_loss": annual_seq_loss,
        "ecosystem_services_bdt": ecosystem_svc,
        "carbon_5yr_projection": projection,
        "pipeline_log": [
            f"[Node 6 · {elapsed}s] Ecosystem: {species_at_risk} species at risk · "
            f"{coastal_km:.2f} km coastline · {recovery_natural:.0f}yr natural recovery (ZERO AI)"
        ],
        "done_nodes": ["ecosystem"],
        "timings": {"ecosystem": elapsed},
        "errors": [],
    }
