
from chains import (
    classify_chain,
    escalate_chain,
    draft_email_chain
)

from tools import (
    calculate_delay_compensation,
    calculate_damage_compensation,
    calculate_lost_compensation
)


def process_exception(report_text, shipment_value, customer_type):
    """
    Classify a shipment exception, calculate compensation,
    decide whether to escalate, and generate the required notes.
    """

    customer_type = customer_type.lower().strip()

    if customer_type not in ("standard", "premium"):
        raise ValueError(
            "customer_type must be 'standard' or 'premium'."
        )

    if shipment_value < 0:
        raise ValueError("shipment_value cannot be negative.")

    # 1. Classify the shipment report.
    classification_result = classify_chain.invoke({
        "report_text": report_text
    })

    classification = classification_result.strip().lower()

    # 2. Calculate compensation using the matching tool.
    compensation_functions = {
        "delayed": calculate_delay_compensation,
        "damaged": calculate_damage_compensation,
        "lost": calculate_lost_compensation
    }

    if classification in compensation_functions:
        compensation_result = compensation_functions[classification](
            shipment_value, report_text
        )
    else:
        classification = "unknown"
        compensation_result = {
            "amount": 0,
            "reasoning": (
                "Unknown exception; manual review is required."
            )
        }

    amount = compensation_result["amount"]
    reasoning = compensation_result["reasoning"]

    # 3. Apply the customer's escalation threshold.
    threshold = 100 if customer_type == "premium" else 200

    if classification == "unknown":
        escalate = True
        escalation_reason = (
            "Unknown classification requires manual review."
        )
    elif amount > threshold:
        escalate = True
        escalation_reason = (
            f"Compensation of {amount} exceeds the "
            f"{customer_type} threshold of {threshold}."
        )
    else:
        escalate = False
        escalation_reason = (
            "Compensation does not exceed the escalation threshold."
        )

    # 4. Draft a manager note only when escalation is required.
    manager_note = None

    if escalate:
        manager_note = escalate_chain.invoke({
            "report_text": report_text,
            "classification": classification,
            "shipment_value": shipment_value,
            "amount": amount,
            "reasoning": reasoning,
            "escalation_reason": escalation_reason
        })

    # 5. Draft the customer email.
    customer_email = draft_email_chain.invoke({
        "customer_type": customer_type,
        "report_text": report_text,
        "classification": classification,
        "shipment_value": shipment_value,
        "amount": amount,
        "reasoning": reasoning,
        "escalate": escalate
    })

    # 6. Return structured data for session-level aggregation.
    return {
        "report_text": report_text,
        "classification": classification,
        "shipment_value": shipment_value,
        "customer_type": customer_type,
        "compensation_amount": amount,
        "compensation_reasoning": reasoning,
        "escalate": escalate,
        "escalation_reason": escalation_reason,
        "manager_note": manager_note,
        "customer_email": customer_email
    }


