from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os 
from vectordb import initialize_vector_db
from llm import init_llm, run_chain

embedding_model = OllamaEmbeddings(model="llama3.2:3b")
persist_directory = "./data/vector_db"
vector_db = None
chain = None
if os.path.exists(persist_directory):
    vector_db = Chroma(
        collection_name="digi-ai",
        persist_directory=persist_directory, 
        embedding_function=embedding_model)
    
    chain = init_llm(vector_db)
    
else:
    vector_db = initialize_vector_db(embedding_model, persist_directory)
    print("Vector database initialized.")


while True:
    question = input("Tanya Aku Apa Saja: ")
    result = run_chain(chain, question)
    
    if question == "exit":
        break




    