"""Streamlit interface for asking questions about the orders table."""

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from mydb import execute_query, get_schema


load_dotenv()

st.set_page_config(page_title="DataGPT", page_icon="📊", layout="wide")


@st.cache_data(show_spinner=False)
def load_schema(table_name: str):
    """Fetch the database schema once per Streamlit session."""
    return get_schema(table_name)


def generate_sql(question: str, schema: str) -> str:
    """Ask OpenAI to translate a question into a read-only PostgreSQL query."""
    client = OpenAI()
    prompt = f"""Generate one PostgreSQL SELECT query for the question below.

Use only the schema provided. Do not modify the database: no INSERT, UPDATE,
DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, or REVOKE statements.
Return SQL only, without Markdown code fences or explanation.

Schema:
{schema}

Question: {question}
"""
    response = client.responses.create(model="gpt-5.6-sol", input=prompt)
    return response.output_text.strip().removeprefix("```sql").removeprefix("```").removesuffix("```").strip()


st.title("📊 DataGPT")
st.caption("Ask questions about the `orders` table in plain English.")

try:
    schema = load_schema("orders")
except Exception as error:
    st.error("Could not connect to PostgreSQL. Check that the database is running and configured.")
    st.exception(error)
    st.stop()

with st.expander("View orders schema"):
    st.dataframe(schema, use_container_width=True, hide_index=True)

with st.form("question_form"):
    question = st.text_input(
        "What would you like to know?",
        placeholder="For example: Give me the top 5 states by sales",
    )
    submitted = st.form_submit_button("Run query", type="primary")

if submitted:
    if not question.strip():
        st.warning("Enter a question before running a query.")
        st.stop()

    try:
        with st.spinner("Generating SQL and querying the database..."):
            sql_query = generate_sql(question, schema.to_string(index=False))
            results = execute_query(sql_query)

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")
        st.subheader("Results")
        st.dataframe(results, use_container_width=True, hide_index=True)
        st.caption(f"{len(results):,} row(s) returned")
    except Exception as error:
        st.error("The query could not be completed.")
        st.exception(error)
