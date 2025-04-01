# back-end/database/queries
import duckdb
import os

# Path to the local DuckDB file
DB_PATH = os.getenv("DUCKDB_PATH", "fitness_ai.duckdb")


# Utility to get or create an ID from a reference table (e.g., gender, diet_type)
def get_or_create_label_id(conn, table, label):
    """
    Retrieves the ID of a label from a reference table.
    If the label does not exist, it inserts it and returns the new ID.

    Parameters:
        - conn (duckdb.DuckDBPyConnection): Active DuckDB connection
        - table (str): Name of the reference table (e.g., "genders", "diet_types")
        - label (str): The label to look up or insert
    Returns:
        - int: The ID of the existing or newly inserted label
    """
    result = conn.execute(f"SELECT id FROM {table} WHERE label = ?", (label,)).fetchone()
    if result:
        return result[0]
    # Insert new label
    conn.execute(f"INSERT INTO {table} (label) VALUES (?)", (label,))
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]

# Utility to get or create goal IDs from list of labels
def get_or_create_goal_ids(conn, goal_labels):
    """
    Retrieves the IDs of a list of goal labels from the 'goals' table.
    If a label does not exist, it is inserted into the table and its new ID is returned.

    Parameters:
    - conn (duckdb.DuckDBPyConnection): Active DuckDB connection
    - goal_labels (list of str): List of goal descriptions (e.g., ["Lose 3kg", "Tone muscles"])

    Returns:
    - list of int: List of goal IDs corresponding to the provided labels
    """
    goal_ids = []
    for label in goal_labels:
        result = conn.execute("SELECT goal_id FROM goals WHERE label = ?", (label,)).fetchone()
        if result:
            goal_ids.append(result[0])
        else:
            conn.execute("INSERT INTO goals (label) VALUES (?)", (label,))
            new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            goal_ids.append(new_id)
    return goal_ids

# ➕ Insert a new user with references and goals
def insert_user(age, gender, height, weight, diet_type, fitness_level, goals):
    """
    Inserts a new user into the 'users' table along with associated reference values and goals.

    - If gender, diet_type, or fitness_level labels do not exist in their respective reference tables,
      they are created and linked via foreign key IDs.
    - Each goal is linked to the user through the 'user_goals' junction table.

    Parameters:
    - age (int): User's age
    - gender (str): Gender label (e.g., "female")
    - height (float): User's height in cm or meters
    - weight (float): User's weight in kg
    - diet_type (str): Diet preference label (e.g., "vegetarian")
    - fitness_level (str): Fitness level label (e.g., "intermediate")
    - goals (list of str): List of user goals (e.g., ["Lose 3kg", "Tone muscles"])

    Returns:
    - None: Prints confirmation after successful insertion
    """
    conn = duckdb.connect(DB_PATH)

    # 🧱 Ensure all tables exist (in case DB is fresh)
    with open("back_end/database/schema.sql", "r") as f:
        conn.execute(f.read())

    # 🔄 Get or create reference IDs
    gender_id = get_or_create_label_id(conn, "genders", gender)
    diet_type_id = get_or_create_label_id(conn, "diet_types", diet_type)
    fitness_level_id = get_or_create_label_id(conn, "fitness_levels", fitness_level)
    goal_ids = get_or_create_goal_ids(conn, goals)

    # 🧍 Insert user
    conn.execute("""
        INSERT INTO users (age, gender_id, height, weight, diet_type_id, fitness_level_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (age, gender_id, height, weight, diet_type_id, fitness_level_id))

    user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # 🎯 Link user to multiple goals
    for goal_id in goal_ids:
        conn.execute("""
            INSERT OR IGNORE INTO user_goals (user_id, goal_id)
            VALUES (?, ?)
        """, (user_id, goal_id))

    conn.close()
    print(f"✅ User {user_id} inserted with {len(goal_ids)} goal(s)")