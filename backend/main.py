

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
