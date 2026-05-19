from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from backend.database.connection import Base


class User(Base):
    """
    Stores registered users.
    One user can have many chat history entries.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50),  unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    # bcrypt hashed password will be stored in the database for privacy
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # if user is deleted, delete their chat history too
    chats = relationship("ChatHistory", back_populates="user",
                         cascade="all, delete-orphan")


class ChatHistory(Base):
    """
    Stores every question + answer pair per user.
    """
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    pdf_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")

# Validations Checks


class SignupRequest(BaseModel):
    username: str
    email:    EmailStr
    password: str


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    username:     str


class UploadResponse(BaseModel):
    message:      str
    chunks_count: int
    filename:     str


class QueryRequest(BaseModel):
    question: str
    top_k:    Optional[int] = 5


class QueryResponse(BaseModel):
    answer:       str
    source_chunks: List[str]


class ChatHistoryItem(BaseModel):
    id:         int
    question:   str
    answer:     str
    pdf_name:   Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
