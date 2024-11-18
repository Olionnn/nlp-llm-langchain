from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


local_model = "llama3.2:3b"  
llm = ChatOllama(model=local_model)


def init_llm(vector_db):
    # Query prompt template
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate 2
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    # Set up retriever
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), 
        llm,
        prompt=QUERY_PROMPT,
    )
    
    
    template = """Answer the question based ONLY on the following context with Bahasa Indonesia language.:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    
    
    chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )

    return chain



def run_chain(chain, question):
    result = chain.invoke({"question": question})
    print(result)
    return result