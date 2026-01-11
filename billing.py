def calculate_bills(readings, total_tanker_cost):
    total_usage = sum(r["usage"] for r in readings)
    cost_per_unit = total_tanker_cost / total_usage if total_usage else 0

    for r in readings:
        r["water_charge"] = round(r["usage"] * cost_per_unit, 2)

    return readings, round(cost_per_unit, 2)
