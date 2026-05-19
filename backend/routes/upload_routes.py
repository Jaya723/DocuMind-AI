import os
import shutil

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.services.rag_service import ingest_file
from backend.services.auth_service import decode_access_token, get_user_by_email
from backend.models.schema import UploadResponse
from backend.config.settings import settings

router = APIRouter(prefix="/upload", tags=["upload"])
bearer = HTTPBearer()

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".csv", ".docx"}
SUPPORTED_DISPLAY = "PDF, TXT, CSV, DOCX"


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db:    Session = Depends(get_db)
):
    """
    Reusable dependency — validates JWT and returns the User object.
    Raises 401 if token is missing, expired, or invalid.
    """
    email = decode_access_token(creds.credentials)
    if not email:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token.")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


@router.post(
    "/",
    response_model=UploadResponse,
    responses={
        400: {"description": "Invalid file type"},
        500: {"description": "Failed to process PDF"},
    },
)
async def upload_file(
    file:         Annotated[UploadFile, File(...)],
    _current_user: Annotated[object, Depends(get_current_user)]
):
    """
    Accepts file upload → validates → saves to data/uploads/ → ingests.
    Supported types: PDF, TXT, CSV, DOCX

    Flow:
    1. Validate file extension
    2. Save file to data/uploads/ on disk
       (locally = your project folder)
       (on Streamlit Cloud = ephemeral container storage)
    3. Pass file path to rag_service.ingest_file()
    4. Return chunk count + filename to frontend
    """

    # 1. Validate file type
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{file_extension}'. "
                f"Supported types: {SUPPORTED_DISPLAY}"
            )
        )

    # 2. Save file to directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"[upload] Saved → {save_path}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    # 3. Ingest into FAISS
    try:
        chunks_count = ingest_file(save_path)
    except ValueError as e:
        # file loaded but had no readable content
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )

    return UploadResponse(
        message="File uploaded and indexed successfully.",
        chunks_count=chunks_count,
        filename=file.filename
    )


def get_supported_types():
    """
    Returns list of supported file types.
    Frontend can use this to restrict the file picker.
    """
    return {
        "supported_extensions": list(SUPPORTED_EXTENSIONS),
        "display": SUPPORTED_DISPLAY
    }
