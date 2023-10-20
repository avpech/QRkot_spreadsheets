from typing import Optional

from pydantic import BaseModel, BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки приложения."""
    app_title: str = 'QRKot'
    description: str = 'Фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    jwt_lifetime: int = 3000
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    locale: str = 'ru_RU'

    class Config:
        env_file = '.env'


class LogConfig(BaseModel):
    """Конфигурация логгирования."""
    LOGGER_NAME: str = 'main_logger'
    LOG_FORMAT: str = '%(levelprefix)s %(asctime)s %(message)s'
    LOG_LEVEL: str = 'INFO'

    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    }
    handlers = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }
    loggers = {
        LOGGER_NAME: {'handlers': ['default'], 'level': LOG_LEVEL},
    }


settings = Settings()
