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

def show_tables(engine: Engine, db_name: str) -> list:
    with engine.connect() as conn:
        conn.execute(text(f"USE {db_name}"))
        res = conn.execute(text(
            "SHOW TABLES"
        ))
        return res.all()

def main():
    engine = init_engine("root")
    print_databases(engine)

if __name__ == "__main__":
    main()

# api
from fastapi import FastAPI

app = FastAPI()

@app.get("/databases")
def read_databases():
    return "databases"

@app.get("/databases/{database_name}")
def read_database(database_name: str):
    return {"db_name": database_name }

@app.post("/databases/{database_name}")
def create_database(database_name: str):
    """Create a database with the given name."""
    # TODO response code 201 if created, and some body content
    return {"db_name": database_name }

# TODO 404 request not found or something like that

# make connect -> try to connect to specified db
# try to connect via given user -> create form and validation
# show tables, databases
# in table: describe table, show all rows (limit 50, pagination)
# parse query string -> without rest api
