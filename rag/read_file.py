from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader

def read_file_extention(file_path):
    return file_path.split('.')[-1]


def read_file(file_path):
    extention = read_file_extention(file_path)
    if extention == 'pdf':
        data = read_pdfs(file_path)
        return data
    elif extention == 'csv':
        data = read_csvs(file_path)
        return data
    else:
        raise ValueError(f"Unsupported file type: {extention}")
    
def read_pdfs(file_path):
    loader = PyPDFLoader(file_path=file_path)
    data = loader.load()
    return data
    



def read_csvs(file_path):
    loader = CSVLoader(file_path=file_path)
    data = loader.load()
    return data


