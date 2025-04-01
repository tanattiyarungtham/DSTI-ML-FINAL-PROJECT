import duckdb
import os

DB_PATH = os.getenv("DUCKDB_PATH", "fitness_ai.duckdb")

# 🚀 Initial reference values
genders = ["male", "female", "other"]
diet_types = ["vegetarian", "vegan", "keto", "none"]
fitness_levels = ["beginner", "intermediate", "advanced"]
goals = ["Lose weight", "Gain muscle", "Improve endurance", "Tone muscles"]


def get_next_id(conn, table, id_column="id"):
    """
    Returns the next available ID for a table by selecting MAX(id_column) + 1.

    Parameters:
        - conn: DuckDB connection
        - table (str): table name
        - id_column (str): name of the ID column (default "id")
    """
    result = conn.execute(f"SELECT MAX({id_column}) FROM {table}").fetchone()[0]
    return (result or 0) + 1

def seed_table(conn, table, values, col_name="label", id_column="id"):
    """
    Insert unique reference values into a table with manual ID generation.

    Parameters:
        - conn: DuckDB connection
        - table (str): table name
        - values (list): list of labels to insert
        - col_name (str): column where the value goes (usually 'label')
        - id_column (str): column used as primary key (default: 'id')
    """
    for value in values:
        exists = conn.execute(f"SELECT 1 FROM {table} WHERE {col_name} = ?", (value,)).fetchone()
        if not exists:
            new_id = get_next_id(conn, table, id_column)
            conn.execute(f"INSERT INTO {table} ({id_column}, {col_name}) VALUES (?, ?)", (new_id, value))

def run_seed():
    conn = duckdb.connect(DB_PATH)

    # 👇 Ensure tables exist before seeding
    with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r") as f:
        conn.execute(f.read())

    print("🔁 Seeding reference tables...")

    seed_table(conn, "genders", genders)
    seed_table(conn, "diet_types", diet_types)
    seed_table(conn, "fitness_levels", fitness_levels)
    seed_table(conn, "goals", goals, id_column="goal_id")  # <- ICI

    conn.close()
    print("✅ Seeding completed.")

if __name__ == "__main__":
    run_seed()