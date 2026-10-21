from chains import classify_chain

result1 = classify_chain.invoke({
    "report_text": "The package arrived broken."
})

print(result1)

from chains import escalate_chain

result2 = escalate_chain.invoke({
    "report_text": "The package arrived broken.",
    "classification": "damaged",
    "shipment_value": 10000,
    "amount": 3000,
    "reasoning": "30% compensation because the package was damaged.",
    "escalation_reason": "Compensation requires manager review."
})

print(result2)

from chains import draft_email_chain

result3 = draft_email_chain.invoke({
    "customer_type": "premium",
    "report_text": "The package arrived broken.",
    "classification": "damaged",
    "shipment_value": 10000,
    "amount": 3000,
    "reasoning": "30% compensation because the package was damaged.",
    "escalate": True
})

print(result3)