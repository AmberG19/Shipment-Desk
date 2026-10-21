Shipment Exception Handling AI Agent

An AI-powered application that analyzes shipment reports, identifies delivery exceptions, and estimates compensation using an LLM-based workflow.

Overview

Shipment issues such as delivery delays, damaged packages, and lost shipments require timely identification and appropriate handling.

This project uses Python and a Large Language Model (LLM) to process shipment reports, classify exceptions, and generate structured results for further processing.

Features

Exception Classification: Identifies shipment issues such as delays, damaged packages, and lost shipments.

LLM-Powered Analysis: Uses a language model to interpret shipment reports.

Compensation Estimation: Estimates compensation based on shipment information and applicable logic.

Structured Processing: Organizes the workflow into separate modules for easier maintenance.

Interactive Interface: Provides a Gradio-based interface for interacting with the application.

Tech Stack

Python

Groq API

OpenAI Python SDK

Gradio

Project Structure

Shipment-Desk/
├── app.py
├── chains.py
├── llm.py
├── main.py
├── pipeline.py
├── session.py
├── tools.py
├── requirements.txt
├── test_chains.py
├── test_pipeline.py
├── test_tools.py
├── .gitignore
└── README.md

Getting Started

1. Clone the repository

git clone https://github.com/AmberG19/Shipment-Desk.git
cd Shipment-Desk

2. Create a virtual environment

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure the API key

Create a .env file in the project root and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here

Replace the placeholder with your own API key.

5. Run the application

Run the entry point appropriate to your setup. If app.py launches the Gradio interface, use:

python app.py

Security

Keep API keys and other secrets in your local .env file.

Never upload .env or expose your API key in source code.

The repository's .gitignore excludes local secrets and development files.

About This Project

This project is part of an AI engineering learning journey, exploring LLM-powered workflows, modular Python code, and practical shipment exception handling.




