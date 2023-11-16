from langchain_app import get_few_shot_db_chain
import streamlit as st

st.title("Tesla Database Langchain Application")

question = st.text_input("Ask a question:")

if question: 
    chain = get_few_shot_db_chain()
    answer = chain.run(question)

    st.header("Answer:")
    st.write(answer)
