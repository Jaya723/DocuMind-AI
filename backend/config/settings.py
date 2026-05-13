from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    All config lives here.
    Values are read from a .env file automatically.
    Never hardcode secrets — always use environment variables.
    """

    # GROQ
    GROQ_API_KEY: str

    # MySQL
    DB_HOST:     str = "localhost"
    DB_PORT:     int = 3306
    DB_USER:     str = "root"
    DB_PASSWORD: str
    DB_NAME:     str = "rag_db"

    # JWT
    JWT_SECRET:    str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # App
    UPLOAD_DIR: str = "data/uploads"

    class Config:
        env_file = ".env"


settings = Settings()
