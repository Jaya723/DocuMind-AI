from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):

    # GROQ
    GROQ_API_KEY: str

    # MySQL
    DB_HOST:     str = "127.0.0.1"
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

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
