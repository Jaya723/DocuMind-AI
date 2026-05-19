from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.services.auth_service import (
    verify_password,
    create_access_token,
    get_user_by_email,
    get_user_by_username
)
from backend.services.db_service import create_user
from backend.models.schema import SignupRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse,
             status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Email already registered or username already taken"}})
def signup(body: SignupRequest, db: Annotated[Session, Depends(get_db)]):
    if get_user_by_email(db, body.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )
    if get_user_by_username(db, body.username):
        raise HTTPException(
            status_code=400,
            detail="Username already taken."
        )

    user = create_user(db, body.username, body.email, body.password)
    token = create_access_token({"sub": user.email})

    return TokenResponse(access_token=token, username=user.username)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = get_user_by_email(db, body.email)

    if not user or not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, username=user.username)
