from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os 
from vectordb import initialize_vector_db
from llm import init_digi_bot, run_chain
from fastapi import FastAPI, Form
from typing import Annotated
app = FastAPI()
embedding_model = OllamaEmbeddings(model="llama3.2:3b")
persist_directory = "./data/vector_db"
vector_db = None
chain = None
if os.path.exists(persist_directory):
    vector_db = Chroma(
        collection_name="digi-ai",
        persist_directory=persist_directory, 
        embedding_function=embedding_model)
    
    chain = init_digi_bot(vector_db)
    
else:
    vector_db = initialize_vector_db(embedding_model, persist_directory)
    print("Vector database initialized.")


# while True:
#     question = input("Tanya Aku Apa Saja: ")
#     result = run_chain(chain, question)
    
#     if question == "exit":
#         break



async def get_answer(question: str):
    result = run_chain(chain, question)
    return result, question


@app.get("/")
async def root():
    return {"message": "Hello World"}
    
    
@app.post("/generate")
async def generate(question: Annotated[str, Form()]):
    result, question = await get_answer(question)
    return {"question": question, "answer": result}

