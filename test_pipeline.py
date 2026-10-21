from pipeline import process_exception
from session import record, generate_daily_summary

result = process_exception(
    report_text="The package arrived broken and damaged.",
    shipment_value=1000,
    customer_type="premium"
)

record(result)

print(generate_daily_summary())