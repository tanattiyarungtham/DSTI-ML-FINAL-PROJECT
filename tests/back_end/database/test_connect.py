# tests/back_end/database/test_connect.py

import pytest
from sqlalchemy import inspect
from pathlib import Path
from back_end.database.connect import DatabaseConnector
from sqlalchemy import text

@pytest.fixture(scope="module")
def db_connector():
    """
    Fixture that provides a single instance of DatabaseConnector for all tests in the module.

    Returns:
        DatabaseConnector: An initialized instance used to interact with the PostgreSQL database.
    """
    root_path = Path(__file__).resolve().parents[3]
    dotenv_path = root_path / "env_folder" / ".env.postgre"
    return DatabaseConnector(dotenv_path=str(dotenv_path))

def test_connection_established(db_connector):
    """
    Test that ensures a successful connection to the PostgreSQL database.

    This verifies that the SQLAlchemy engine can connect and execute a basic SQL query (`SELECT 1`)
    without raising an exception.

    Args:
        db_connector (DatabaseConnector): Instance of the database connector.
    """
    engine = db_connector.engine
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1

def test_execute_schema_creates_tables(db_connector):
    """
    Test that the `execute_schema()` method successfully creates all expected tables.

    This uses SQLAlchemy's Inspector to retrieve the list of tables in the database
    after executing the schema file. You can adjust the `expected_tables` set to match
    your application's schema.

    Args:
        db_connector (DatabaseConnector): Instance used to run the schema and inspect DB state.
    """
    db_connector.execute_schema()
    inspector = inspect(db_connector.engine)
    tables = inspector.get_table_names()
    print("Tables trouvées :", tables)
    expected_tables = {"users", "genders", "goals", "diet_types", "fitness_levels", "user_goals"}
    assert expected_tables.issubset(set(tables))

def test_get_session_executes_query(db_connector):
    """
    Test that a session created using `get_session()` can execute SQL statements.

    This ensures that the session is valid, properly connected to the DB,
    and able to retrieve results from a simple query.

    Args:
        db_connector (DatabaseConnector): Instance of the database connector.
    """
    session = db_connector.get_session()
    result = session.execute(text("SELECT 1"))
    assert result.fetchone()[0] == 1
    session.close()

def test_get_db_generator(db_connector):
    """
    Test that the generator from `get_db()` yields a valid and operational SQLAlchemy session.

    This simulates how FastAPI would inject the session as a dependency.
    Ensures the yielded session is able to run queries and is properly closed afterwards.

    Args:
        db_connector (DatabaseConnector): Instance providing the session generator.
    """
    db = next(db_connector.get_db())
    result = db.execute(text("SELECT 1"))
    assert result.fetchone()[0] == 1
    db.close()