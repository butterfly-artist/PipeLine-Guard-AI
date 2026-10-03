from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PipeGuard AI"
    environment: str = "development"
    api_v1_prefix: str = "/api"
    
    # Gemma / AI Configuration Placeholders
    gemma_model_name: str = "gemma-2-9b-it"
    gemma_api_base: str = "http://localhost:11434"
    gemma_api_key: str = ""

    # Ingestion Settings
    max_upload_size_mb: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
