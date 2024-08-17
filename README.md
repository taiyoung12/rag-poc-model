# rag-poc-model

이 프로젝트는 MacOS에서 LangChain을 사용하여 Ollama 모델을 로드하고 Streamlit으로 웹 인터페이스를 로드합니다. Ollama 설치, 모델 다운로드, 그리고 Python 패키지 설치 및 웹 애플리케이션 실행 과정을 다룹니다.

## 프로젝트 구조

```bash
rag-poc-model/
├── app/
│   ├── api/
│   ├── errors/
│   ├── llm/
│   ├── middlewares/
│   ├── resources/
│   ├── schemas/
│   ├── application.py
│   └── config.py
├── vectorstore_마이데이터_API.pdf
├── vectorstore_마이데이터.pdf
├── Modelfile
├── README.md
├── requirements.txt
└── web.py
```

## 1. Ollama 설치

### MacOS에 Ollama 설치

Ollama는 MacOS에서 사용할 수 있는 AI 모델 로딩 및 추론 도구입니다. 아래 링크에서 Ollama를 다운로드하고 설치할 수 있습니다.

```bash
https://ollama.com/download
```

## 2.모델 파일 다운로드 
Hugging Face에서 제공하는 Llama-3-Open-Ko-8B 모델 파일을 다운로드합니다.

```bash
wget https://huggingface.co/teddylee777/Llama-3-Open-Ko-8B-gguf/resolve/main/Llama-3-Open-Ko-8B-Q8_0.gguf
``` 

## 3. 모델 생성 
```bash
ollama create llama3-ko -f Modelfile
``` 

## 4. Python 패키지 설치
이 프로젝트는 Python과 여러 패키지를 사용하여 웹 애플리케이션을 실행합니다. 모든 패키지는 requirements.txt 파일에 정의되어 있으며, 아래 명령어를 사용하여 설치할 수 있습니다.

```bash
pip3 install -r requirements.txt
``` 

requirements
```
fastapi==0.112.0
starlette==0.37.2
pydantic==1.10.14
sentence-transformers==3.0.1
pymupdf==1.24.9
langchain==0.2.12
langchain_community==0.2.11
chromadb==0.5.3
faiss-cpu==1.8.0.post1
uvicorn==0.30.5
h5py==3.8.0
numpy==1.26.4
torch==2.4.0
huggingface-hub==0.24.5
scipy==1.14.0
requests==2.31.0
streamlit==1.37.1
streamlit-autorefresh==1.0.1
```
## 5. 서버 실행 
```bash
uvicorn app.application:app --host 0.0.0.0 --port 8001
localhost:8001/docs ( Swagger )
``` 

## 6. 화면 실행  
```bash
streamlit run web.py
localhost:8501 ( 화면 )
``` 
