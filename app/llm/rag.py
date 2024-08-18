import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import app.errors.exceptions as exceptions 


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
    model_name='monologg/koelectra-base-v3-discriminator',
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
당신은 마이데이터 관련 정책과 기술 사양에 대해 전문적으로 답변하는 챗봇입니다. 
아래 제공된 공식 문서를 기반으로 사용자의 질문에 대해 신뢰할 수 있고 정확한 정보를 제공하세요. 
답변은 정책 및 기술적 측면 모두를 고려하여 작성되며, 가능한 한 명확하고 세부적으로 작성해 주세요. 
필요한 경우 관련 규정, 가이드라인, 기술 사양 등을 인용하거나 설명을 추가하여 사용자가 쉽게 이해할 수 있도록 해주세요. 
모든 답변은 한국어로 작성되어야 합니다.

참고 문서 내용:
{context}

사용자 질문: {question}

정확하고 구체적인 답변 (정책 및 기술 사양을 포함하여):
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
        raise exceptions.IncorrectKeywordError()
    return rag_chains[keyword]
