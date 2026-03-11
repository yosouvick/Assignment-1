

📊 Monday.com BI Agent
An AI-driven Business Intelligence agent that bridges the gap between messy Monday.com boards and executive-level decision-making. No stale data, no manual cleaning—just live insights.
## Quick Overview
This agent turns fragmented "real-world" data into a coherent narrative. It queries your Deals and Work Orders boards in real-time, handles missing values gracefully, and provides a visible "Thought Trace" of every API call it makes.
## Core Features
	•	Live GraphQL Integration: Zero caching. Every query fetches current board states.
	•	Data Resilience: Normalizes inconsistent sectors (e.g., "Energy" vs "energy") and messy date formats on the fly.
	•	Action Trace: A "debug" UI element shows the evaluator exactly which tools and boards are being hit.
	•	Founder-Level Reasoning: Interprets broad questions like "How’s the pipeline?" into specific revenue and volume metrics.
## Technical Stack
	•	Language: Python 3.10+
	•	Orchestration: LangChain (ReAct Agent)
	•	API: Monday.com GraphQL v2
	•	UI/UX: Streamlit (for the chat interface and action logs)
	•	Processing: Pandas (for transient data normalization)
## Setup Instructions
	1	Monday.com Setup: * Import Deals.csv and Work Orders.csv as new boards.
	•	Note the Board IDs from the URL.
	2	Environment Variables:
	•	Create a .env file with your MONDAY_API_TOKEN, DEALS_BOARD_ID, and WORK_ORDERS_ID.
	3	Execution:
	•	Run pip install -r requirements.txt
	•	Launch with streamlit run app.py
