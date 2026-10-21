DELAY_KEYWORDS = ["urgent","critical","asap","time sensitive"]

DAMAGED_KEYWORDS = ["damaged","broken","cracked","defective"]

LOST_KEYWORDS = ["lost","missing","not found","never arrived"]

def calculate_delay_compensation(shipment_value: float, report_text: str)-> dict:
    
    """
    Calculate compensation for a delay-related exception.

    Args:
        shipment_value (float): Monetary value of the shipment.
        report_text (str): Text describing the shipment exception.

    Returns:
        dict: Compensation amount and reasoning.
    """
    report = report_text.lower()

    for word in DELAY_KEYWORDS:
        if word in report:
            amount = shipment_value * 0.10
            return {
                "amount": round(amount, 2),
                "reasoning": (
                    f"Matched urgency keyword '{word}'. "
                    "Compensation is 10% of shipment value."
                )
            }

   
def calculate_damage_compensation(shipment_value, report_text):
    """
    Calculate compensation for a damaged-shipment exception.

    Args:
        shipment_value (float): Monetary value of the shipment.
        report_text (str): Text describing the shipment exception.

    Returns:
        dict: Compensation amount and reasoning.
    """
    report = report_text.lower()

    for word in DAMAGED_KEYWORDS:
        if word in report:
            amount = shipment_value * 0.30
            return {
                "amount": round(amount, 2),
                "reasoning": (
                    f"Matched damage keyword '{word}'. "
                    "Compensation is 30% of shipment value."
                )
            }

    return {
        "amount": 0,
        "reasoning": "No damage-related keyword was found."
    }


def calculate_lost_compensation(shipment_value, report_text):
    """
    Calculate compensation for a lost-shipment exception.

    Args:
        shipment_value (float): Monetary value of the shipment.
        report_text (str): Text describing the shipment exception.

    Returns:
        dict: Compensation amount and reasoning.
    """
    report = report_text.lower()

    for word in LOST_KEYWORDS:
        if word in report:
            amount = shipment_value
            return {
                "amount": round(amount, 2),
                "reasoning": (
                    f"Matched loss keyword '{word}'. "
                    "Compensation is 100% of shipment value."
                )
            }

    