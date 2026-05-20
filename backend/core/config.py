from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Настройки приложения с поддержкой переменных окружения."""

    # === Application ===
    app_name: str = "Энергоэффективность МКД"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = Field(default="development", env="ENVIRONMENT")

    # === API ===
    api_prefix: str = "/api/v1"
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    max_request_size: int = 10 * 1024 * 1024  # 10MB

    # === Database (PostgreSQL + TimescaleDB) ===
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="diplom_db", env="DB_NAME")
    db_user: str = Field(default="postgres", env="DB_USER")
    db_password: str = Field(default="postgres", env="DB_PASSWORD")
    db_pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, env="DB_MAX_OVERFLOW")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def sync_database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # === Redis ===
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")

    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # === Message Broker (RabbitMQ/Kafka) ===
    broker_type: str = Field(default="rabbitmq", env="BROKER_TYPE")  # rabbitmq or kafka

    # RabbitMQ
    rabbitmq_host: str = Field(default="localhost", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field(default="guest", env="RABBITMQ_USER")
    rabbitmq_password: str = Field(default="guest", env="RABBITMQ_PASSWORD")
    rabbitmq_vhost: str = Field(default="/", env="RABBITMQ_VHOST")

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/{self.rabbitmq_vhost}"

    # Kafka
    kafka_bootstrap_servers: List[str] = Field(
        default=["localhost:9092"],
        env="KAFKA_BOOTSTRAP_SERVERS"
    )

    # === Celery ===
    celery_broker_url: Optional[str] = Field(default=None, env="CELERY_BROKER_URL")
    celery_result_backend: Optional[str] = Field(default=None, env="CELERY_RESULT_BACKEND")

    @property
    def effective_celery_broker(self) -> str:
        if self.celery_broker_url:
            return self.celery_broker_url
        if self.broker_type == "rabbitmq":
            return self.rabbitmq_url
        return f"redis://{self.redis_url}"

    # === MinIO (S3-compatible storage) ===
    minio_endpoint: str = Field(default="localhost:9000", env="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minioadmin", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", env="MINIO_SECRET_KEY")
    minio_bucket_raw: str = Field(default="raw-data", env="MINIO_BUCKET_RAW")
    minio_bucket_backups: str = Field(default="backups", env="MINIO_BUCKET_BACKUPS")
    minio_secure: bool = Field(default=False, env="MINIO_SECURE")

    # === Security & Auth ===
    jwt_secret_key: str = Field(default="CHANGE_ME_IN_PRODUCTION", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_EXPIRE_MIN")
    jwt_refresh_token_expire_days: int = Field(default=7, env="JWT_REFRESH_EXPIRE_DAYS")
    password_hash_rounds: int = Field(default=12, env="PASSWORD_HASH_ROUNDS")

    # === ML Models ===
    mlflow_tracking_uri: Optional[str] = Field(default=None, env="MLFLOW_TRACKING_URI")
    model_registry_uri: Optional[str] = Field(default=None, env="MODEL_REGISTRY_URI")
    default_model_horizon_hours: int = Field(default=24, env="DEFAULT_MODEL_HORIZON")

    # === External APIs ===
    weather_api_key: Optional[str] = Field(default=None, env="WEATHER_API_KEY")
    weather_api_url: str = Field(default="https://api.weather.gov", env="WEATHER_API_URL")
    gis_zkh_api_url: Optional[str] = Field(default=None, env="GIS_ZKH_API_URL")

    # === Monitoring ===
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # === Compliance ===
    gsop_base_year: int = Field(default=2020, env="GSOP_BASE_YEAR")
    compliance_pp_rf_354_enabled: bool = Field(default=True, env="COMPLIANCE_PP_RF_354")
    data_retention_years: int = Field(default=3, env="DATA_RETENTION_YEARS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Кэшированный экземпляр настроек."""
    return Settings()
