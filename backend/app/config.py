from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- App ---
    APP_NAME: str = "SynapsBranch"
    APP_ENV: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000"

    # --- Database ---
    DATABASE_URL: str

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- JWT ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- OAuth ---
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""

    # --- Email (Resend) ---
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "SynapsBranch <reports@synapsbranch.app>"

    # --- AI ---
    AI_PROVIDER: str = "claude"
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # --- Frontend ---
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"
    NEXTAUTH_SECRET: str = ""
    NEXTAUTH_URL: str = "http://localhost:3000"


settings = Settings()
