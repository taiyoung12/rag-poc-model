from fastapi import APIRouter, status, Query 
from app.schemas.base import ResponseBase
import app.errors.exceptions as exceptions 
from app.llm.rag import get_rag_chain


router = APIRouter(tags=["rag"])

@router.get(
    "/rag",
    response_model=ResponseBase,
    responses={
        201: {"description": "Success Request To LLM Model"},
    },
    status_code=status.HTTP_201_CREATED,
    description="Test LLM Model With RAG",
    summary="RAG Request",
)
async def query_llm(
    keyword: str = Query(..., description="The keyword to identify the RAG chain"),
    prompt: str = Query(..., description="The prompt to send to the LLM"),
) -> ResponseBase:
    try:
        rag_chain = get_rag_chain(keyword)
    except ValueError:
        raise exceptions.IncorrectKeywordError()

    answer = rag_chain.invoke(prompt) 
    response = {"prompt": prompt, "answer": answer}

    return ResponseBase(
        code=status.HTTP_201_CREATED,
        message="Success LLM Model with RAG Test",
        data = response
    )