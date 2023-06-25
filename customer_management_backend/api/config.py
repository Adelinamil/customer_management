from dataclasses import dataclass
from datetime import timedelta

from envparse import Env


@dataclass
class DatabaseConfig:
    host: str
    password: str
    username: str
    database: str
    RDBMS: str = 'postgresql'
    driver: str = 'asyncpg'

    @property
    def make_url(self):
        return f'{self.RDBMS}+{self.driver}://{self.username}:' \
               f'{self.password}@{self.host}/{self.database}'


@dataclass
class AuthConfig:
    secret_key: str
    token_expire: timedelta


@dataclass
class Config:
    db: DatabaseConfig
    auth: AuthConfig


def load_config() -> Config:
    env = Env()
    env.read_envfile()

    return Config(
        db=DatabaseConfig(
            host=env.str('PG_HOST', default='0.0.0.0:5432'),
            username=env.str('PG_USERNAME', default='postgres'),
            password=env.str('PG_PASSWORD', default='postgres'),
            database=env.str('PG_DATABASE', default='postgres'),
        ),
        auth=AuthConfig(
            secret_key=env.str('SECRET_KEY'),
            token_expire=timedelta(days=365)
        )
    )
