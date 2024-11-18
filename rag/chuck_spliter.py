from langchain_text_splitters import RecursiveCharacterTextSplitter

def chuck_spliter(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(text)
    return chunks

