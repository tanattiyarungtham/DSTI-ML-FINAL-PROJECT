# back_end/database/connect.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pprint import pprint


class DatabaseConnector:
    """
    Handles PostgreSQL connection using SQLAlchemy and provides utilities
    such as session management and schema execution.
    """

    def __init__(self, dotenv_path: str = None):
        # Load environment variables from .env.postgre file
        load_dotenv(dotenv_path)
        required_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"]
        missing = {var: os.getenv(var) for var in required_vars if not os.getenv(var)}
        if missing:
            pprint(missing)
            raise ValueError("❌ Missing required environment variables.")
        self.database_url = (
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', 5432)}/{os.getenv('POSTGRES_DB')}"
        )

        # Create SQLAlchemy engine and session factory
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        """
        Provides a session object. Meant for use in script or FastAPI dependency injection.
        """
        return self.SessionLocal()

    def get_db(self):
        """
        FastAPI-compatible generator dependency to yield a session.
        Ensures proper cleanup with `finally: db.close()`.
        """
        db = self.get_session()
        try:
            yield db
        finally:
            db.close()

    def execute_schema(self, schema_path: str = None):
        """
        Executes all SQL commands in the schema.sql file to bootstrap the DB.

        Args:
            schema_path (str): Optional path to a custom schema file.
                               Defaults to `schema.sql` in the same folder.
        """
        if not schema_path:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

        # 🔥 begin() crée une transaction et la commit automatiquement à la fin
        with self.engine.begin() as connection:
            with open(schema_path, "r") as f:
                sql_commands = f.read().split(";")
                for command in sql_commands:
                    command = command.strip()
                    if command:
                        connection.execute(text(command))

        print("✅ Schema executed: all tables created (if not exist).")