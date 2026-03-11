import streamlit as st
import pandas as pd
import requests
import json
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- CONFIGURATION ---
MONDAY_API_TOKEN = "YOUR_MONDAY_TOKEN"
DEALS_BOARD_ID = "YOUR_DEALS_ID"
WORK_ORDERS_ID = "YOUR_WORK_ORDERS_ID"
API_URL = "https://api.monday.com/v2"




def fetch_monday_data(board_type: str):
    """
    Fetches live data from Monday.com boards. 
    board_type must be 'deals' or 'work_orders'.
    """
    board_id = DEALS_BOARD_ID if board_type == 'deals' else WORK_ORDERS_ID
    
    query = """
    query {
      boards (ids: %s) {
        items_page {
          items {
            name
            column_values {
              text
              column { title }
            }
          }
        }
      }
    }
    """ % board_id

    headers = {"Authorization": MONDAY_API_TOKEN, "API-Version": "2023-10"}
    
    
    st.write(f" Querying Monday.com Board: {board_type} (ID: {board_id})")
    
    response = requests.post(API_URL, json={'query': query}, headers=headers)
    data = response.json()
    
    
    items = data['data']['boards'][0]['items_page']['items']
    rows = []
    for item in items:
      row = {"Item Name": item['name']}
      for val in item['column_values']:
        row[val['column']['title']] = val['text']
      rows.append(row)
    
    return pd.DataFrame(rows).to_dict()


def leadership_summary_formatter(data_snapshot: str):
    """
    Formats raw business data into a high-level executive summary 
    with Strengths, Risks, and Recommendations.
    """
    return f"Executive Synthesis requested for: {data_snapshot}"



llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [fetch_monday_data, leadership_summary_formatter]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Business Intelligence Agent for a CEO. "
               "You have access to Monday.com boards. Always show your logic. "
               "If data is missing, notify the user but provide the best possible estimate."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



st.set_page_config(page_title="Monday BI Agent", layout="wide")
st.title("📊 Founder's BI Agent")
st.info(f"Connected to Monday.com Boards: [Deals]({DEALS_BOARD_ID}), [Work Orders]({WORK_ORDERS_ID})")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How's our pipeline looking for the energy sector?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
        with st.status("Thinking & Querying Monday.com...", expanded=True) as status:
            response = agent_executor.invoke({"input": prompt, "chat_history": st.session_state.messages})
            status.update(label="Analysis Complete!", state="complete", expanded=False)
        
        st.markdown(response["output"])
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})