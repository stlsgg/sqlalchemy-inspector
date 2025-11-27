# api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

class DatabaseOptions(BaseModel):
    charset: str | None = None
    collation: str | None = None

class TableOptions(BaseModel):
    charset: str | None = None
    collation: str | None = None

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
def custom_http_exception_handler(req: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": {
                "error_desc": exc.detail,
                "path": req.url.path
            }
        },
    )

@app.get("/databases")
def read_databases():
    """Get information about existing and accessable databases."""
    # return show_dbs()
    return {"status": "ok"}

@app.post("/databases/{database_name}")
def create_database(database_name: str, options: DatabaseOptions):
    """Create a database with the given name and options."""
    # TODO response code 201 if created, and some body content
    # return create_db(database_name, options)
    return {"status": "ok"}

@app.get("/databases/{database_name}")
def read_database(database_name: str):
    """Get full information about database (metadata, tables)."""
    return {"status": "ok"}

# TODO auth
@app.post("/login")
def login():
    """Authenticate a user with given login and password."""
    return {"status": "ok"}

@app.get("/users")
def print_users():
    """Print all logins in the system."""
    return {"status": "ok"}

@app.get("/users/me")
def print_my_user():
    """Print current user's login."""
    return {"status": "ok"}

@app.get("/users/{user_id}")
def print_user(user_id: int):
    """Print specific user's login."""
    return {"status": "ok"}

