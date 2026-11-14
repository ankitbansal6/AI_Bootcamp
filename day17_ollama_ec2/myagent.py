"""LangChain agent for answering questions about the local PostgreSQL database."""

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import execute_query, get_schema, list_tables


def build_agent():
    """Create and return the data analyst agent."""
    model = ChatOllama(model="qwen3:8b")
    return create_agent(
        model=model,
        tools=[execute_query, list_tables, get_schema],
        system_prompt="You are a data analyst. Use the tools when required to work with PostgreSQL.",
    )


def ask_agent(question: str) -> str:
    """Run one question through the agent and return its final answer."""
    response = build_agent().invoke({"messages": [question]})
    return response["messages"][-1].text


if __name__ == "__main__":
    print(ask_agent(input("Ask a question: ")))
