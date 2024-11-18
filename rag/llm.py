from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

local_model = "llama3.2:3b"  
llm = ChatOllama(model=local_model)

WHITELIST = [
    # "What are your capabilities?",
    # "How do you work?",
    # "Explain AI functions.",
    # "Topik politik sensitif",
    # "Debat agama",
    # "Pertanyaan pribadi atau menyerang",
]

BLACKLIST = [
    # "Sensitive political topics",
    # "Religious debates",
    # "Personal attacks or harmful content",
    # "Layanan apa yang ditawarkan Digipoint untuk klien?",
    # "Ceritakan tentang klien Digipoint.",
    # "Jelaskan profil klien Digipoint.",
]

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are Digi-Bot, an AI language model assistant developed by Digipoint. Your primary purpose is to answer questions related to the company's clients, such as their profiles, services used, or other relevant inquiries. Your task is to:
    1. Generate 2 alternative versions of the given user question to retrieve relevant documents from a vector database.
    2. If the question is unrelated to company clients or forbidden (as per a blacklist), adapt your response or refuse to answer.

    Provide alternative questions separated by newlines.

    Original question: {question}"""
)

template = """
Anda adalah Digi-Bot, asisten AI yang dibuat oleh Digipoint. Tujuan Anda adalah menjawab pertanyaan terkait klien perusahaan, seperti profil mereka, layanan yang digunakan, atau kebutuhan mereka.

Jawab pertanyaan HANYA berdasarkan konteks berikut dalam Bahasa Indonesia:
{context}

Aturan Tambahan:
1. Jika pengguna bertanya tentang biodata Anda (contoh: "Siapa kamu?" atau "Apa kemampuanmu?"), berikan jawaban berikut:
   - **Nama**: Digi-Bot
   - **Organisasi**: Digipoint
   - **Tujuan**: Menjawab pertanyaan tentang klien perusahaan.
2. Jika pertanyaan sesuai dengan kategori whitelist, berikan jawaban sesuai konteks.
3. Jika pertanyaan tidak sesuai dengan tujuan (atau masuk kategori blacklist), jawab dengan sopan bahwa Anda tidak bisa menjawabnya.
4. Gunakan tanggapan khusus untuk topik berikut:
   - **Layanan klien**: Jelaskan layanan yang ditawarkan kepada klien.
   - **Pertanyaan umum**: Berikan penjelasan singkat dan relevan tentang operasi Digipoint.
   - Jika pertanyaan tidak jelas, mintalah klarifikasi dari pengguna.

Pertanyaan: {question}
"""

def is_whitelisted(question):
    return any(phrase.lower() in question.lower() for phrase in WHITELIST)

def is_blacklisted(question):
    return any(phrase.lower() in question.lower() for phrase in BLACKLIST)


def init_digi_bot(vector_db):
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(),
        llm,
        prompt=QUERY_PROMPT,
    )
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # def custom_logic(input_data):
    #     question = input_data["question"]
        
    #     if is_blacklisted(question):
    #         return "Maaf, saya tidak dapat menjawab pertanyaan ini karena topiknya sensitif atau tidak relevan dengan tujuan saya."
        
    #     if is_whitelisted(question):
    #         return f"Pertanyaan Anda sesuai dengan tujuan saya. Berikut adalah jawaban untuk: {question}"
        
    #     if "who are you" in question.lower() or "what are your capabilities" in question.lower():
    #         return (
    #             "Halo! Saya Digi-Bot, asisten AI dari Digipoint. "
    #             "Tujuan saya adalah membantu menjawab pertanyaan tentang klien perusahaan, "
    #             "seperti profil mereka, layanan yang digunakan, atau kebutuhan mereka."
    #         )
        
    #     return chain.invoke(input_data)
    
    def custom_logic_in_indonesian(input_data):
        question = input_data["question"]
        
        if is_blacklisted(question):
            return "Maaf, saya tidak dapat menjawab pertanyaan ini karena topiknya sensitif atau tidak relevan dengan tujuan saya."
        
        if is_whitelisted(question):
            return f"Pertanyaan Anda sesuai dengan tujuan saya. Berikut adalah jawaban untuk: {question}"
        
        # if "siapa kamu" in question.lower() or "apa kemampuanmu" in question.lower():
        #     return (
        #         "Halo! Saya Digi-Bot, asisten AI dari Digipoint. "
        #         "Tujuan saya adalah membantu menjawab pertanyaan tentang klien perusahaan, "
        #         "seperti profil mereka, layanan yang digunakan, atau kebutuhan mereka."
        #     )
        
        return chain.invoke(input_data)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return {"chain": chain, "custom_logic": custom_logic_in_indonesian}

def run_chain(chain, question):
    result = chain["custom_logic"]({"question": question})
    print(result)
    return result