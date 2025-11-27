from sqlalchemy import *
import re

class DBMSInitError(Exception):
    pass

class DBInitError(Exception):
    pass

class MyDBMS:
    """
    Database Management System class that provides:
    1. Establishing a connection to a DBMS through SQLAlchemy.
    2. Listing existing databases.
    3. Performing CRUD operations on databases. (WIP)
    """
    def validate_db_name(name):
        if not re.match(r"^[a-zA-Z0-9_]+$", name):
            raise ValueError(f"Invalid identifier: {name}")
        return name

    def __init__(
        self,
        db_conn_url: URL
    ):
        """Initialize connection to DBMS with a given URL object."""

        required = {
            "dialect": db_conn_url.get_dialect().name,
            "driver": db_conn_url.get_dialect().driver,
            "user": db_conn_url.username,
            "password": db_conn_url.password,
            "addr": db_conn_url.host,
        }

        for arg, val in required.items():
            if val is None or val == "":
                raise DBMSInitError(f"empty argument given: {arg} is empty.")

        self.engine = create_engine(db_conn_url)

        # test connection
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 'ping pong'"))

    def show_databases(self):
        """Show all databases on current user scope (accessable)."""
        with self.engine.connect() as conn:
            return [row[0] for row in conn.execute(text("SHOW DATABASES")).all()]

    def use_database(self, db_name: str):
        MyDBMS.validate_db_name(db_name)
        with self.engine.connect() as conn:
            return conn.execute(text(f"USE {db_name}"))

class MyDatabase(MyDBMS):
    """
    Database class that provides:
    1. Connecting to the specific database through the DBMS class.
    2. Listing all tables within the database.
    3. Performing CRUD operations on tables. (WIP)
    """
    def __init__(self, dbms_conn_url: URL, db_name: str) -> None:

        """Initialize connection to database with a given URL object."""
        super().__init__(dbms_conn_url)
        self.name = MyDBMS.validate_db_name(db_name)
        self.metadata = MetaData()
        with self.engine.connect() as conn:
            conn.execute(text(f"USE {self.name}"))

    def show_tables(self) -> list:
        """List all tables in a database."""
        with self.engine.connect() as conn:
            return [
                row[0] for row in conn.execute(
                    text("SHOW TABLES")
                ).fetchall()
            ]

    def describe_table(self, table_name: str) -> list[dict]:
        """Describe fields in a table."""
        with self.engine.connect() as conn:
            return conn.execute(text(f"DESCRIBE {table_name}")).mappings().all()

    def show_rows(
        self,
        table_name: str,
        limit: int,
        offset: int
    ) -> list[dict]:
        """Select all rows in a table."""
        table = Table(table_name, self.metadata, autoload_with=self.engine)

        with self.engine.connect() as conn:
            stmt = select(table).limit(limit).offset(offset)
            return conn.execute(stmt).mappings().fetchall()

    def describe_me(self):
        """Describe database: charset, collation."""
        query = text(f"""
                SELECT
                  SCHEMA_NAME AS Name,
                  DEFAULT_CHARACTER_SET_NAME AS Charset,
                  DEFAULT_COLLATION_NAME AS Collation,
                  SCHEMA_COMMENT AS Comment

                FROM information_schema.schemata
                WHERE SCHEMA_NAME = :db_name;
                """)

        with self.engine.connect() as conn:
            return conn.execute(
                query,
                {"db_name": self.name}
            ).mappings().fetchone()

