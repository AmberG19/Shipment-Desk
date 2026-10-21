DAILY_LOG = []


def record(final_state: dict) -> None:
    """Save one processed shipment exception in the daily log."""
    DAILY_LOG.append({
        "category": final_state["classification"],
        "compensation": final_state["compensation_amount"],
        "needs_approval": final_state["escalate"]
    })


def generate_daily_summary() -> str:
    """Generate an aggregated Daily Triage Summary."""

    if not DAILY_LOG:
        return "No exceptions processed yet today."

    # 1. Calculate total compensation.
    total_compensation = sum(
        e["compensation"] for e in DAILY_LOG
    )

    # 2. Find all exceptions requiring approval.
    escalated = [
        e for e in DAILY_LOG
        if e["needs_approval"]
    ]

    # 3. Calculate escalation rate as a percentage.
    escalation_rate = round(
        100 * len(escalated) / len(DAILY_LOG)
    )

    # 4. Aggregate compensation by category.
    by_category = {}

    for e in DAILY_LOG:
        category = e["category"]

        by_category[category] = (
            by_category.get(category, 0)
            + e["compensation"]
        )

    # 5. Find the costliest category by total compensation.
    costliest_category = (
        max(by_category, key=by_category.get)
        if by_category
        else "n/a"
    )

    # 6. Build the summary.
    lines = [
        f"Daily Triage Summary: "
        f"{len(DAILY_LOG)} exception(s) processed"
    ]

    for i, e in enumerate(DAILY_LOG, 1):
        status = (
            "ESCALATED"
            if e["needs_approval"]
            else "auto-resolved"
        )

        lines.append(
            f"{i}. [{e['category']}] "
            f"₹{e['compensation']:.2f} - {status}"
        )

    lines.append(
        f"\nTotal compensation: ₹{total_compensation:.2f}"
    )

    lines.append(
        f"Escalation rate: {escalation_rate}% "
        f"({len(escalated)}/{len(DAILY_LOG)})"
    )

    lines.append(
        f"Costliest category: {costliest_category} "
        f"(₹{by_category[costliest_category]:.2f})"
    )

    return "\n".join(lines)