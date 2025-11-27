# api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(req: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": {
                "error_code": exc.status_code,
                "error_desc": exc.detail,
                "path": req.url.path
            }
        },
    )

@app.get("/databases")
async def read_databases():
    """Get information about existing and accessable databases."""
    # return show_dbs()
    return {"status": "ok"}

@app.get("/databases/{database_name}")
async def read_database(database_name: str):
    """Get full information about database (metadata, tables)."""
    return {"status": "ok"}

# TODO auth
@app.post("/login")
async def login():
    """Authenticate a user with given login and password."""
    return {"status": "ok"}

@app.get("/users")
async def print_users():
    """Print all logins in the system."""
    return {"status": "ok"}

@app.get("/users/me")
async def print_my_user():
    """Print current user's login."""
    return {"status": "ok"}

@app.get("/users/{user_id}")
async def print_user(user_id: int):
    """Print specific user's login."""
    return {"status": "ok"}

