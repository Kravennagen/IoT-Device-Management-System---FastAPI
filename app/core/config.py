from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./iot_db.db"
    redis_url: str = "redis://localhost:6379"
    mqtt_broker: str = "localhost"
    mqtt_port: int = 1883
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()