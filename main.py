import streamlit as st
import sqlalchemy
from sqlalchemy import create_engine
from langchain_app import get_few_shot_db_chain

# Connect to the PostgreSQL database
host = '127.0.0.1'
user = 'postgres'
password = '1'
database = 'tsla_db'
port = 5432
engine = create_engine("postgresql+psycopg2://user:password@host:port/database")

# Open a connection to the database
conn = engine.connect()

st.title("Tesla Database Langchain Application")

question = st.text_input("Ask a question:")

if question:
    # Combine the user's question with the SQL query
    combined_query = question + " " + "SQL Query: "

    # Use the Langchain model to generate an SQL query based on the combined text
    chain = get_few_shot_db_chain()
    sql_query = chain.run(combined_query)

    # Execute the SQL query against the PostgreSQL database
    results = conn.execute(sql_query)

    # Close the connection to the database
    conn.close()

    # Display the answer from the database
    st.header("Answer:")
    for row in results:
        st.write(row)
