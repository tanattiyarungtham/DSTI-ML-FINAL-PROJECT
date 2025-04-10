#tests/back_end/database/test_seed_postgres.py

import pytest
from sqlalchemy import text
from pathlib import Path
from back_end.database.connect import DatabaseConnector
from back_end.database.seed_postgres import run_seed

@pytest.fixture(scope="module")
def db_connector():
    """
    Fixture that initializes the DatabaseConnector instance for test usage.

    It loads environment variables from the `.env.postgre` file and
    returns a connected SQLAlchemy engine wrapper.

    Returns:
        DatabaseConnector: Instance to interact with PostgreSQL database.
    """
    root_path = Path(__file__).resolve().parents[3]
    dotenv_path = root_path / "env_folder" / ".env.postgre"
    return DatabaseConnector(dotenv_path=str(dotenv_path))


def test_seed_data_inserted(db_connector):
    """
    Test that the `run_seed()` function correctly inserts all reference values into the database.

    This test ensures that predefined labels (e.g., 'male', 'vegan', 'beginner') are correctly
    inserted into their respective tables (`genders`, `diet_types`, `fitness_levels`, `goals`).

    Args:
        db_connector (DatabaseConnector): Provides access to the database.
    """
    db_connector.execute_schema()
    run_seed()
    session = db_connector.get_session()

    expected = {
        "genders": {"male", "female", "other"},
        "diet_types": {"vegetarian", "vegan", "keto", "none"},
        "fitness_levels": {"beginner", "intermediate", "advanced"},
        "goals": {"Lose weight", "Gain muscle", "Improve endurance", "Tone muscles"},
    }

    for table, expected_values in expected.items():
        result = session.execute(text(f"SELECT label FROM {table}"))
        labels = {row[0] for row in result.fetchall()}
        assert expected_values.issubset(labels), f"{table} does not contain expected values"

    session.close()


def test_seed_idempotency(db_connector):
    """
    Test that the `run_seed()` function is idempotent — meaning it doesn't insert duplicates.

    This is verified by recording the row counts before and after running the seed function a second time.
    The counts should remain unchanged.

    Args:
        db_connector (DatabaseConnector): Provides access to the database.
    """
    session = db_connector.get_session()

    initial_counts = {
        table: session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        for table in ["genders", "diet_types", "fitness_levels", "goals"]
    }

    run_seed()

    new_counts = {
        table: session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        for table in ["genders", "diet_types", "fitness_levels", "goals"]
    }

    assert initial_counts == new_counts, "Row counts changed after re-seeding"

    session.close()


def test_seed_tables_not_empty(db_connector):
    """
    Test that the seed operation results in non-empty tables.

    This provides a general check that all critical reference tables
    (`genders`, `diet_types`, `fitness_levels`, `goals`) contain at least one row after seeding.

    Args:
        db_connector (DatabaseConnector): Provides access to the database.
    """
    session = db_connector.get_session()

    for table in ["genders", "diet_types", "fitness_levels", "goals"]:
        count = session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        assert count > 0, f"{table} is empty after seeding."

    session.close()