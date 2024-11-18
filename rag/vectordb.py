from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from read_file import read_file
from chuck_spliter import chuck_spliter
import os






def initialize_vector_db(embedding_model, persist_directory):
    file_pdf = "./data/digipoin.pdf"
    file_csv = "./data/company.csv"

    data_pdf = read_file(file_pdf)
    data_csv = read_file(file_csv)

    chunks1 = chuck_spliter(data_pdf)
    chunks2 = chuck_spliter(data_csv)
    
    chunks = chunks1 + chunks2
    
    # vector_db = Chroma(collection_name="digi-ai", embedding=embedding_model)
    # vector_db.add_documents(documents=chunks)
    # vector_db.persist(persist_directory)
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name="digi-ai",
        persist_directory=persist_directory
    )
    print(f"Added {len(chunks)} chunks to the vector database.")
    
    return vector_db
    
def add_document_to_vector_db(vector_db, file_path, persist_directory):
    data = read_file(file_path)
    chunks = chuck_spliter(data)

    vector_db.add_documents(documents=chunks)

    vector_db.persist(persist_directory)
    print(f"Added {len(chunks)} chunks to the vector database.")
