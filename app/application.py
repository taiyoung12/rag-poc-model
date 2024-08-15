from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import rag
from app.config import settings
from app.middlewares.request import base_http_middleware
from app.schemas.base import ResponseBase
from app.llm.rag import initialize_rag_chains

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=base_http_middleware)

app.include_router(rag.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    initialize_rag_chains()

@app.get(
    "/health",
    response_model=ResponseBase,
    responses={
        200: {"description": "Server Health Check"},
    },
    status_code=status.HTTP_200_OK,
    description="Health Check API",
    summary="Health Check",
)
async def health_check() -> ResponseBase:
    return ResponseBase(
        code=status.HTTP_200_OK,
        message="Server Alive",
        data={"status": "alive"},
    )
