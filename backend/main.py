# api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from db import MyDatabase
from sqlalchemy import URL
from sqlalchemy.exc import ProgrammingError

# CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = URL.create(
    drivername="mariadb+mariadbconnector",
    username="root",
    password="1234",
    host="127.0.0.1"
)
db = MyDatabase(url, "foobar")

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
    databases = db.show_databases()
    if databases is not None:
        return {"status": "ok", "data": databases}

@app.get("/databases/{database_name}")
async def read_database(database_name: str):
    """Get full information about database (tables)."""
    try:
        db.use_database(database_name)
        tables = db.show_tables()
        if tables is not None:
            return {"status": "ok", "data": tables}
    except ValueError as err:
        return {
            "status": "error",
            "desc": "ValueError occured.",
            "detail": err,
        }

    except ProgrammingError as err:
        return {
            "status": "error",
            "desc": "Query error occured.",
            "detail": err
        }

    except Exception as err:
        return {
            "status": "error",
            "desc": "Unexpected error occured.",
            "detail": err
        }

@app.get("/databases/{database_name}/tables")
async def show_database_tables(database_name: str):
    try:
        db.use_database(database_name)
        tables = db.show_tables()
        if tables is not None:
            return {"status": "ok", "data": tables}
    except ValueError as err:
        return {
            "status": "error",
            "desc": "ValueError occured.",
            "detail": err,
        }

    except ProgrammingError as err:
        return {
            "status": "error",
            "desc": "Query error occured.",
            "detail": err
        }

    except Exception as err:
        return {
            "status": "error",
            "desc": "Unexpected error occured.",
            "detail": err
        }

@app.get("/databases/{database_name}/desc")
async def show_database_description(database_name: str):
    try:
        db.use_database(database_name)
        desc = db.describe_me()
        if desc:
            return {"status": "ok", "data": desc}
    except ValueError as err:
        return {
            "status": "error",
            "desc": "ValueError occured.",
            "detail": err,
        }

    except ProgrammingError as err:
        return {
            "status": "error",
            "desc": "Query error occured.",
            "detail": err
        }

    except Exception as err:
        return {
            "status": "error",
            "desc": "Unexpected error occured.",
            "detail": err
        }

@app.get("/databases/{database_name}/tables/{table_name}/desc")
async def show_table_info(database_name: str, table_name: str):
    desc = db.describe_table(table_name)
    if desc:
        return {"status": "ok", "data": desc}

@app.get("/databases/{database_name}/tables/{table_name}/content")
async def select_rows_in_table(
    database_name: str,
    table_name: str,
    limit: int = 50,
    offset: int = 0
):
    db.use_database(database_name)
    rows = db.show_rows(table_name, limit=limit, offset=offset)
    if rows:
        return {"status": "ok", "data": rows}

# basic auth
# @app.post("/auth/login")
# async def authenticate_user()
