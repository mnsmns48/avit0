from dataclasses import dataclass

from environs import Env


@dataclass
class Hidden:
    link: str
    pages: int
    db_username: str
    db_password: str
    db_local_port: int
    db_name: str
    db_echo: bool


def load_hidden_vars(path: str):
    env = Env()
    env.read_env()

    return Hidden(
        link=env.str("LINK"),
        pages=env.int("PAGES"),
        db_username=env.str("DB_USERNAME"),
        db_password=env.str("DB_PASSWORD"),
        db_local_port=env.int("DB_LOCAL_PORT"),
        db_name=env.str("DB_NAME"),
        db_echo=env.bool("DB_ECHO")
    )


hidden = load_hidden_vars(path='.env')
