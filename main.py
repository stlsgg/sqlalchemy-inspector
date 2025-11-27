import sqlalchemy as alchemy
from sqlalchemy import text, create_engine, Engine
from dotenv import load_dotenv
import os

# load .env variables
load_dotenv()

def init_engine(user: str, passwd: str=None) -> Engine:
    # dialect+driver://username:password@host:port/database

    if not passwd:
        passwd = os.getenv("MARIADB_ROOT_PASSWORD", None)

        if passwd is None:
            passwd = "1234" # TODO выкидываем ошибку подключения

    url = f"mariadb+mariadbconnector://{user}:{passwd}@127.0.0.1/"
    engine = create_engine(url)
    return engine

def print_databases(engine: Engine) -> list:
    with engine.connect() as conn:
        res = conn.execute(text(
            "SHOW DATABASES"
        ))
        return res.all()


def main():
    engine = init_engine("root")
    print_databases(engine)

if __name__ == "__main__":
    main()
