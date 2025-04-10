# back_end/database/seed_postgres.py

from back_end.database.connect import DatabaseConnector
from sqlalchemy.orm import Session
from sqlalchemy import text
from pathlib import Path

# Reference values
GENDERS = ["male", "female", "other"]
DIET_TYPES = ["vegetarian", "vegan", "keto", "none"]
FITNESS_LEVELS = ["beginner", "intermediate", "advanced"]
GOALS = ["Lose weight", "Gain muscle", "Improve endurance", "Tone muscles"]


# Auto-detect .env location
root_path = Path(__file__).resolve().parents[2]
dotenv_path = root_path / "env_folder" / ".env.postgre"
db_connector = DatabaseConnector(dotenv_path=str(dotenv_path))

def insert_unique_values(db: Session, table: str, values: list[str], label_col="label"):
    """
    Inserts values into a reference table if they do not already exist.

    Args:
        db (Session): SQLAlchemy database session
        table (str): Name of the reference table (e.g., 'genders')
        values (list): List of labels to insert
        label_col (str): The column containing the label (default: 'label')
    """
    for value in values:
        exists = db.execute(
            text(f"SELECT 1 FROM {table} WHERE {label_col} = :val"),
            {"val": value}
        ).fetchone()
        if not exists:
            db.execute(
                text(f"INSERT INTO {table} ({label_col}) VALUES (:val)"),
                {"val": value}
            )


def run_seed():
    """
    Seeds PostgreSQL with reference data for genders, diet types, fitness levels, and goals.
    """
    print("🌱 Seeding PostgreSQL reference tables...")

    db = db_connector.get_session()
    try:
        insert_unique_values(db, "genders", GENDERS)
        insert_unique_values(db, "diet_types", DIET_TYPES)
        insert_unique_values(db, "fitness_levels", FITNESS_LEVELS)
        insert_unique_values(db, "goals", GOALS, label_col="label")
        db.commit()  # 💥 SUPER IMPORTANT
        print("✅ Seeding complete.")
    except Exception as e:
        db.rollback()
        print("❌ Error during seeding:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()