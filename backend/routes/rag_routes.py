from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.services.rag_service import query_document
from backend.services.auth_service import decode_access_token, get_user_by_email
from backend.services.db_service import save_chat, get_user_chats, delete_user_chats
from backend.models.schema import (
    QueryRequest, QueryResponse,
    ChatHistoryItem
)

router = APIRouter(prefix="/rag", tags=["rag"])
bearer = HTTPBearer()


def get_current_user(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    db:    Annotated[Session, Depends(get_db)]
):
    email = decode_access_token(creds.credentials)
    if not email:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token.")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


@router.post("/query", response_model=QueryResponse, responses={400: {"description": "Invalid query or document processing error"}, 500: {"description": "Query failed"}})
def query(
    body: QueryRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[object, Depends(get_current_user)]
):
    """
    Main RAG endpoint.
    1. Validates JWT
    2. Runs RAG pipeline (retrieve + generate)
    3. Saves Q&A to chat history
    4. Returns answer + source chunks
    """
    try:
        result = query_document(body.question, top_k=body.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    save_chat(
        db=db,
        user_id=current_user.id,
        question=body.question,
        answer=result["answer"]
    )

    return QueryResponse(
        answer=result["answer"],
        source_chunks=result["source_chunks"]
    )


@router.get("/history", response_model=list[ChatHistoryItem])
def history(
    db:           Annotated[Session, Depends(get_db)],
    current_user: Annotated[object, Depends(get_current_user)]
):
    return get_user_chats(db, current_user.id)


@router.delete("/history")
def clear_history(
    db:           Annotated[Session, Depends(get_db)],
    current_user: Annotated[object, Depends(get_current_user)]
):
    """
    Wipes all chat history for the logged-in user.
    """
    count = delete_user_chats(db, current_user.id)
    return {"message": f"Deleted {count} chat records."}
