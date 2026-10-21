from llm import llm

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (StrOutputParser,JsonOutputParser)


classify_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Classify the shipment report into exactly one category:
        delayed, damaged, lost, or unknown.

        fit any of these and reply with one word only,nothing else

        Choose unknown if the report does not clearly describe
        a recognised shipment exception.
        """
    ),
    ("human", "{report_text}")
])

classify_chain = classify_prompt | llm | StrOutputParser()

escalate_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Draft a concise internal note for a manager about
        a shipment exception requiring escalation.

        Include the report, classification, shipment value,
        compensation amount, and reason for escalation.
        Do not invent facts.
        """
    ),
    (
        "human",
        """
        Report: {report_text}
        Classification: {classification}
        Shipment value: {shipment_value}
        Compensation amount: {amount}
        Compensation reasoning: {reasoning}
        Escalation reason: {escalation_reason}
        """
    )
])

escalate_chain = (
    escalate_prompt
    | llm
    | StrOutputParser()
)
email_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Draft a professional and empathetic email to a customer
        about their shipment exception.

        Explain the issue and compensation outcome clearly.
        Do not invent facts, delivery dates, or policy details.
        Do not promise compensation beyond the amount provided.
        """
    ),
    (
        "human",
        """
        Customer type: {customer_type}
        Report: {report_text}
        Classification: {classification}
        Shipment value: {shipment_value}
        Compensation amount: {amount}
        Compensation reasoning: {reasoning}
        Escalation required: {escalate}
        """
    )
])

draft_email_chain = (
    email_prompt
    | llm
    | StrOutputParser()
)
