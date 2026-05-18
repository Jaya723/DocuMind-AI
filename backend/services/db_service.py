from typing import List
from sqlalchemy.orm import Session
from backend.models.schema import User, ChatHistory
from backend.services.auth_service import hash_password


def create_user(db: Session, username: str,
                email: str, password: str) -> User:
    """
    Hash password → insert user → commit → return ORM object.
    """
    user = User(
        username=username,
        email=email,
        password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)    # loads auto-generated id + created_at
    return user


def save_chat(db: Session, user_id: int,
              question: str, answer: str,
              pdf_name: str = None) -> ChatHistory:
    """
    Persist one Q&A pair to the chat_history table.
    """
    chat = ChatHistory(
        user_id=user_id,
        question=question,
        answer=answer,
        pdf_name=pdf_name
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_user_chats(db: Session,
                   user_id: int,
                   limit: int = 50) -> List[ChatHistory]:
    """
    Fetch the most recent `limit` chats for a user,
    newest first.
    """
    return (
        db.query(ChatHistory)
          .filter(ChatHistory.user_id == user_id)
          .order_by(ChatHistory.created_at.desc())
          .limit(limit)
          .all()
    )


def delete_user_chats(db: Session, user_id: int) -> int:
    """
    Wipe all chat history for a user.
    Returns number of rows deleted.
    """
    count = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .delete()
    )
    db.commit()
    return count
