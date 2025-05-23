from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, create_sql_query_chain

# Load the local SQLite database file
def load_db():
    return SQLDatabase.from_uri("sqlite:///real_estate.db")

# Create the SQL generation chain using Groq's Gemma model
def chain_create(db):
    llm = ChatGroq(model="gemma-7b-it", api_key=os.getenv("GROQ_API_KEY"))
    return create_sql_query_chain(llm, db)

# Generate the SQL, run it, and use Groq to produce an answer
def sql_infer(db, chain, user_question):
    sql_query = chain.invoke({"question": user_question})
    result = db.run(sql_query + " LIMIT 10")

    st.code(sql_query, language="sql")
    st.dataframe(result)

    prompt = PromptTemplate.from_template(
        """Given the following user question, SQL query, and SQL result, generate a natural language answer.

        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer:"""
    )

    llm_model = ChatGroq(model="mixtral-8x7b-32768", api_key=os.getenv("GROQ_API_KEY"))
    llm = LLMChain(llm=llm_model, prompt=prompt)

    result_text = str(result)[:3000]  # Prevent token overload
    answer = llm.invoke({
        "question": user_question,
        "query": sql_query,
        "result": result_text
    })

    return answer["text"]

# Streamlit UI
def main():
    st.set_page_config(page_title="Real Estate Q&A", layout="wide", page_icon="🏠")
    st.title("🏡 Real Estate AI Assistant (SQLite + LangChain + Groq)")

    try:
        db = load_db()
        chain = chain_create(db)

        with st.expander("📋 Table Names"):
            st.code(db.get_usable_table_names())

        with st.expander("📑 Table Schemas"):
            st.code(db.get_table_info())

        question = st.text_input("Ask a question about your real estate data:")

        if st.button("Get Answer") and question:
            try:
                answer = sql_infer(db, chain, question)
                st.success("✅ Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    except Exception as e:
        st.error(f"❌ Failed to load database: {e}")

if __name__ == "__main__":
    main()
