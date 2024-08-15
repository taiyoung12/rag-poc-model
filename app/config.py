from pydantic import BaseSettings

class ApplicationSettings(BaseSettings):
    PROJECT_NAME: str = "RAG POC MODEL"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "RAG Poc Model Server"

    EXCEPT_PATH_LIST: list[str] = ["/health", "/openapi.json"]

settings = ApplicationSettings()