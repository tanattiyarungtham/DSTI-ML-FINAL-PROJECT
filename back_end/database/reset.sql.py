# back_end/database/reset_db.py

from sqlalchemy import text
from back_end.database.connect import DatabaseConnector
from pathlib import Path

root_path = Path(__file__).resolve().parents[2]
dotenv_path = root_path / "env_folder" / ".env.postgre"
db = DatabaseConnector(dotenv_path=str(dotenv_path))

def reset_schema():
    print("🧨 Dropping all tables...")
    with db.engine.connect() as connection:
        connection.execute(text("""
            DROP TABLE IF EXISTS user_goals, users, genders, diet_types, fitness_levels, goals CASCADE;
        """))
    print("✅ Tables dropped.")

if __name__ == "__main__":
    reset_schema()