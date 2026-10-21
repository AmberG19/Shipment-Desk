
import gradio as gr

from pipeline import process_exception
from session import record, generate_daily_summary


def analyze_shipment(report_text, shipment_value, customer_type):
    """Process one shipment and return its results for the UI."""

    if not report_text or not report_text.strip():
        raise gr.Error("Please enter a shipment report.")

    if shipment_value is None or shipment_value < 0:
        raise gr.Error("Shipment value must be zero or greater.")

    try:
        result = process_exception(
            report_text=report_text.strip(),
            shipment_value=shipment_value,
            customer_type=customer_type
        )

        # Record only after the pipeline succeeds.
        record(result)

        classification = result["classification"].title()
        amount = result["compensation_amount"]
        escalation = (
            "Yes" if result["escalate"] else "No"
        )
        manager_note = (
            result["manager_note"]
            or "No manager escalation note required."
        )

        return (
            classification,
            f"₹{amount:,.2f}",
            result["compensation_reasoning"],
            escalation,
            result["escalation_reason"],
            manager_note,
            result["customer_email"],
            generate_daily_summary()
        )

    except gr.Error:
        raise
    except Exception as exc:
        raise gr.Error(
            f"Shipment processing failed: {exc}"
        ) from exc


with gr.Blocks(title="Shipment Exception Agent") as demo:

    gr.Markdown(
        """
        # Shipment Exception Agent
        ### AI-powered shipment triage and compensation assistant

        Enter a shipment report to classify the exception,
        calculate compensation, and generate the required messages.
        """
    )

    with gr.Row():
        with gr.Column():
            report_text = gr.Textbox(
                label="Shipment Report",
                placeholder=(
                    "Example: The package arrived damaged "
                    "and the contents are broken."
                ),
                lines=5
            )

            shipment_value = gr.Number(
                label="Shipment Value (₹)",
                value=10000,
                minimum=0,
                precision=2
            )

            customer_type = gr.Radio(
                choices=["standard", "premium"],
                value="standard",
                label="Customer Type"
            )

            analyze_button = gr.Button(
                "Analyze Shipment",
                variant="primary"
            )

        with gr.Column():
            classification = gr.Textbox(
                label="Classification"
            )

            compensation_amount = gr.Textbox(
                label="Compensation Amount"
            )

            compensation_reasoning = gr.Textbox(
                label="Compensation Reasoning",
                lines=3
            )

            escalation_required = gr.Textbox(
                label="Escalation Required"
            )

            escalation_reason = gr.Textbox(
                label="Escalation Reason",
                lines=2
            )

    manager_note = gr.Textbox(
        label="Manager Escalation Note",
        lines=5
    )

    customer_email = gr.Textbox(
        label="Draft Customer Email",
        lines=8
    )

    gr.Markdown("## Daily Triage Summary")

    daily_summary = gr.Textbox(
        label="Session Summary",
        value=generate_daily_summary(),
        lines=10,
        interactive=False
    )

    analyze_button.click(
        fn=analyze_shipment,
        inputs=[
            report_text,
            shipment_value,
            customer_type
        ],
        outputs=[
            classification,
            compensation_amount,
            compensation_reasoning,
            escalation_required,
            escalation_reason,
            manager_note,
            customer_email,
            daily_summary
        ]
    )


if __name__ == "__main__":
    demo.launch(share=True)
