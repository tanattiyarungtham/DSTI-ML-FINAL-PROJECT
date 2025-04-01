import os
import tempfile
import pytest
import duckdb
from pathlib import Path
from back_end.database.repository.user import UserRepository
from back_end.database.seed_duckdb import run_seed

@pytest.fixture
def temp_db_path():
    """
    Creates a temporary directory and returns a valid path for a DuckDB file.
    The file will be created by DuckDB (not pre-created).

    Yields:
        str: Path to the DuckDB database file
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.duckdb")
        yield db_path

@pytest.fixture
def repo(temp_db_path):
    """
    Instantiates a UserRepository with a fresh schema and seeded reference tables.

    Args:
        temp_db_path (str): Path to the temporary DuckDB file

    Returns:
        UserRepository: A configured instance ready for testing
    """
    repo = UserRepository(temp_db_path)

    # Load schema
    SCHEMA_PATH = Path(__file__).resolve().parents[4] / "back_end" / "database" / "schema.sql"
    with open(SCHEMA_PATH, "r") as f:
        repo.conn.execute(f.read())

    # Seed predefined values (gender, goals, etc.)
    run_seed()

    return repo

def test_insert_user_and_get_progress(repo):
    """
    Test inserting a user and retrieving weight loss progress.

    Asserts that:
    - The weight and target weight are correctly stored.
    - The kg to lose is properly computed.
    """
    repo.insert_user(
        age=30,
        gender="female",
        height=165,
        weight=65.0,
        target_weight=58.0,
        diet_type="vegetarian",
        fitness_level="intermediate",
        goals=["Lose weight", "Tone muscles"]
    )

    progress = repo.get_user_progress(1)

    assert progress["current_weight"] == 65.0
    assert progress["target_weight"] == 58.0
    assert progress["kg_to_lose"] == pytest.approx(7.0)