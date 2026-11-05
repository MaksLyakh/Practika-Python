from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://clinic14:clinic14@localhost:5434/clinic14"
    async_database_url: str = "postgresql+asyncpg://clinic14:clinic14@localhost:5434/clinic14"
    redis_url: str = "redis://localhost:6380/0"
    jwt_secret: str = "development-only-secret-change-me"
    admin_username: str = "admin"
    admin_password: str = "ChangeMe123!"
    cache_ttl: int = 180
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
