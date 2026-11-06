import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    # Setting shared by every environment
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DB_SCHEMA = os.environ.get("DB_SCHEMA") # Optional
    REDIS_URL = os.environ.get("REDIS_URL")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024 # 1 MB, bigger bodies get 413
    JWT_PRIVATE_KEY_PATH = os.environ.get("JWT_PRIVATE_KEY_PATH")
    JWT_PUBLIC_KEY_PATH = os.environ.get("JWT_PUBLIC_KEY_PATH")
    JWT_ACCESS_TOKEN_MINUTES = int(os.environ.get("JWT_ACCESS_TOKEN_MINUTES", "15"))
    JWT_REFRESH_TOKEN_DAYS = int(os.environ.get("JWT_REFRESH_TOKEN_DAYS", "7"))


class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True  # Exceptions reach the test instead of becoming 500s
    REDIS_URL = os.environ.get("TEST_REDIS_URL")
    DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

class ProductionConfig(Config):
    pass

CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

def get_config(name:str | None = None) -> type[Config]:
    # Return the config class for "name", or for APP_ENV if not given
    name = name or os.environ.get("APP_ENV", "development")
    try:
        return CONFIGS[name]
    except KeyError:
        raise ValueError(f"Unknown APP_ENV '{name}'. Use one of. {list(CONFIGS)}") from None