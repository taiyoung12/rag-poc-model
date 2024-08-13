from pydantic import BaseSettings

class ApplicationSettings(BaseSettings):
    PROJECT_NAME: str = "RAG POC MODEL"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "RAG Poc Model Server"

settings = ApplicationSettings()