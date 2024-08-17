import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 키워드와 PDF 파일 매핑
keyword_to_pdf = {
    "마이데이터": "./app/resources/마이데이터.pdf",
    "마이데이터_API": "./app/resources/마이데이터_API.pdf"
}

# 각 키워드에 대한 검색 객체와 RAG 체인 생성
model = None
rag_chains = {}
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
embeddings = HuggingFaceEmbeddings(
    model_name='BAAI/bge-m3',
    model_kwargs={'device':'cpu'},
)

def get_model(model_name: str, temperature: float):
    global model
    if model is None:
        try:
            model = ChatOllama(model=model_name, temperature=temperature)
            print("model success")
        except Exception as e:
            print(f"Error initializing Ollama model: {e}")
            raise
    return model

template = '''
당신은 친절한 챗봇입니다. 아래 제공된 문서를 참고하여 최대한 정확하고 상세한 답변을 제공해 주세요. 모든 답변은 한국어로 작성되어야 합니다.

문서 내용:
{context}

질문: {question}

답변:
'''

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return '\n\n'.join([d.page_content for d in docs])

def initialize_rag_chains():
    global rag_chains
    for keyword, pdf_file in keyword_to_pdf.items():
        vectorstore_path = f'vectorstore_{os.path.basename(pdf_file)}'
        
        if os.path.exists(vectorstore_path):
            print(f"Loading existing vectorstore for {keyword}")
            vectorstore = Chroma(persist_directory=vectorstore_path, embedding_function=embeddings)
        else:
            print(f"Creating new vectorstore for {keyword}")
            loader = PyMuPDFLoader(pdf_file)
            pages = loader.load()
            docs = text_splitter.split_documents(pages)
            vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=vectorstore_path)
            vectorstore.persist()
        
        retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
        model = get_model("llama3-ko", 0.7) 
        
        rag_chain = (
            {'context': retriever | format_docs, 'question': RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        rag_chains[keyword] = rag_chain

def get_rag_chain(keyword: str):
    if keyword not in rag_chains:
        raise ValueError(f"Keyword {keyword} not found in RAG chains.")
    return rag_chains[keyword]
