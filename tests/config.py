from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import NullPool

from src.config import BaseDatabaseConfig
from src.core.db_manager import DatabaseManager

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent


class TestDatabaseConfig(BaseDatabaseConfig):
    pass


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env-template",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_TEST_CONFIG__",
        extra="ignore",
    )
    db: TestDatabaseConfig


test_settings = TestSettings()
test_db_manager = DatabaseManager(
    url=test_settings.db.url,
    echo=test_settings.db.echo,
    echo_pool=test_settings.db.echo_pool,
    poolclass=NullPool,  # Warning! Don't delete this param!
)
