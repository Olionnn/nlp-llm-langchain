from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import os 
from vectordb import initialize_vector_db
from llm import init_digi_bot, run_chain
from fastapi import FastAPI, Form
from typing import Annotated


ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")  # Default to localhost if not set
persist_dir = os.getenv("PERSIST_DIR", "./data/vector_db")  # Default to local folder if not set



app = FastAPI()
embedding_model = OllamaEmbeddings(model="llama3.2:1b", base_url=ollama_host)
persist_directory = persist_dir
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

