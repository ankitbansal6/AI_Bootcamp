"""Streamlit chat interface for the PostgreSQL data analyst agent."""

import streamlit as st
from langchain_core.messages import HumanMessage

from myagent import build_agent


st.set_page_config(page_title="Database Analyst", page_icon="📊", layout="centered")


@st.cache_resource
def get_agent():
    return build_agent()


st.title("📊 Database Analyst")
st.caption("Ask questions about the data in your PostgreSQL database.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []

with st.sidebar:
    st.subheader("About")
    st.write("The assistant can inspect database tables and schemas, then run queries to answer your questions.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.agent_messages = []
        st.rerun()

for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

question = st.chat_input("Ask a question about your data...")
if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Analyzing your data..."):
                agent = get_agent()
                result = agent.invoke(
                    {"messages": [*st.session_state.agent_messages, HumanMessage(content=question)]}
                )
            st.session_state.agent_messages = result["messages"]
            answer = result["messages"][-1].text or "I couldn't produce a text answer."
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        except Exception as exc:
            st.error(f"I couldn't complete that request: {exc}")
