from enum import Enum
from os import environ

from pydantic import BaseSettings, PostgresDsn

env = environ.get("ENV", "dev")


class ENV(Enum):
    DEV: str = "dev"
    PRD: str = "prd"
    TEST: str = "test"


class Settings(BaseSettings):
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_DBNAME: str
    PG_HOST: str
    PG_PORT: int
    X_REQ_ID_HEADER: str = "x-request-id"
    APP_TITLE: str = "Weather API"
    APP_DESCRIPTION: str = ""
    APP_ID: str = "random-string"

    def get_env(self) -> ENV:
        value = env.lower().strip()
        if value == "dev":
            return ENV.DEV
        elif value == "test":
            return ENV.TEST
        else:
            return ENV.PRD

    def database_uri(self) -> PostgresDsn:
        rtn: PostgresDsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.PG_USERNAME,
            password=self.PG_PASSWORD,
            host=self.PG_HOST,
            path=f"/{self.PG_DBNAME}",
        )
        return rtn

    def sync_database_uri(self) -> PostgresDsn:
        """
        The sync_database_uri function returns a PostgresDsn object that is used to connect to the database.
        The function takes in no arguments and returns a PostgresDsn object for sync driver, this will be used
        especially for alembic.

        :return: A postgresdsn object.
        """

        rtn: PostgresDsn = PostgresDsn.build(
            scheme="postgresql",
            user=self.PG_USERNAME,
            password=self.PG_PASSWORD,
            host=self.PG_HOST,
            path=f"/{self.PG_DBNAME}",
        )
        return rtn

    class Config:
        env_file = f"{env}.env"
        env_file_encoding = "utf-8"


settings = Settings()
