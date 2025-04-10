import pytest
import sys
from pathlib import Path
from sqlalchemy import text

# 🛠️ Ajoute proprement la racine du projet au PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

print("✅ PYTHONPATH includes:")
for p in sys.path:
    print("  -", p)

# ✅ Import après ajout du bon chemin
from back_end.database.connect import DatabaseConnector

@pytest.fixture(autouse=True)
def reset_db():
    """
    Automatically resets all relevant database tables before each test.

    This fixture:
    1. Drops all normalized reference and user-related tables.
    2. Reapplies the database schema using the `execute_schema` method.
    """
    dotenv_path = PROJECT_ROOT / "env_folder" / ".env.postgre"
    db = DatabaseConnector(dotenv_path=str(dotenv_path))

    with db.engine.connect() as conn:
        conn.execute(text("""
            DROP TABLE IF EXISTS user_goals, users, genders, diet_types, fitness_levels, goals CASCADE;
        """))
        print("♻️ Tables dropped.")

    db.execute_schema()
    print("🔁 Schema reapplied.")