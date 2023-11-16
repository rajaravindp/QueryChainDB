from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
import sentence_transformers
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from dotenv import load_dotenv
import streamlit as st
import os
from few_shots import few_shots

# Load environment variables from .env file
load_dotenv()

def get_few_shot_db_chain():
    llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.2)
    host = '127.0.0.1'
    user = 'postgres'
    password = '1'
    database = 'tsla_db'
    port = 5432

    # Create a PostgreSQL connection
    engine = SQLDatabase.from_uri(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

    # Create embeddings
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    to_vectorize = [" ".join(x.values()) for x in few_shots]

    vector_store = Chroma.from_texts(to_vectorize, embedding=embedding, metadatas=few_shots)

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vector_store, k=2)
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer", ],
    #     template="\nQuestion:{Question}\nSQL Query: {SQLQuery}\nSQL Result: {SQLResult}\nAnswer: {Answer}"
        template="""\nQuestion:{Question}\nSQL Query: {SQLQuery}\nAnswer: {Answer}"""
    )
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"]
    )

    chain = SQLDatabaseChain.from_llm(llm, engine, prompt=few_shot_prompt, verbose=True)

    return chain


if __name__ == "__main__":
    chain = get_few_shot_db_chain()
    print(chain.run("What are the different das types available?"))

