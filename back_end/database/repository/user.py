# back-end/database/repository/user.py
import duckdb
import os

DB_PATH = os.getenv("DUCKDB_PATH", "fitness_ai.duckdb")

class UserRepository:
    """
    Repository class to manage user interactions in DuckDB.
    Includes methods for inserting and retrieving user data.
    """

    def __init__(self, db_path: str = DB_PATH):
        """
        Initializes the repository by connecting to the DuckDB database.

        Parameters:
        - db_path (str): Path to the DuckDB file (default: from env or 'fitness_ai.duckdb')
        """
        self.conn = duckdb.connect(db_path)

    def get_next_id(self, table: str, id_column: str = "id") -> int:
        """
        Returns the next available ID for a table using MAX + 1 logic.

        Parameters:
        - table (str): Table name (e.g., 'genders')
        - id_column (str): Name of the ID column (default: 'id')

        Returns:
        - int: Next available ID
        """
        max_id = self.conn.execute(f"SELECT MAX({id_column}) FROM {table}").fetchone()[0]
        return (max_id or 0) + 1

    def get_or_create_label_id(self, table: str, label: str, id_column: str = "id") -> int:
        """
        Retrieves or inserts a label in a reference table and returns its ID.

        Parameters:
        - table (str): Name of the reference table (e.g., 'genders', 'diet_types')
        - label (str): Label to find or insert
        - id_column (str): Name of the ID column (default: 'id')

        Returns:
        - int: ID of the existing or newly created label
        """
        result = self.conn.execute(f"SELECT {id_column} FROM {table} WHERE label = ?", (label,)).fetchone()
        if result:
            return result[0]

        new_id = self.get_next_id(table, id_column)
        self.conn.execute(f"INSERT INTO {table} ({id_column}, label) VALUES (?, ?)", (new_id, label))
        return new_id

    def get_or_create_goal_ids(self, labels: list[str]) -> list[int]:
        """
        Retrieves or inserts a list of goal labels in the 'goals' table and returns their IDs.

        Parameters:
        - labels (list of str): List of goal descriptions

        Returns:
        - list of int: List of goal IDs (existing or newly inserted)
        """
        ids = []
        for label in labels:
            result = self.conn.execute("SELECT goal_id FROM goals WHERE label = ?", (label,)).fetchone()
            if result:
                ids.append(result[0])
            else:
                new_id = self.get_next_id("goals", "goal_id")
                self.conn.execute("INSERT INTO goals (goal_id, label) VALUES (?, ?)", (new_id, label))
                ids.append(new_id)
        return ids

    def insert_user(self, age, gender, height, weight, target_weight, diet_type, fitness_level, goals: list[str]):
        """
        Inserts a new user into the 'users' table with all associated reference values and goals.

        Parameters:
        - age (int): User's age
        - gender (str): Gender label (e.g., 'female')
        - height (float): Height in cm or meters
        - weight (float): Current weight in kg
        - target_weight (float): Desired weight in kg
        - diet_type (str): Dietary preference (e.g., 'vegan')
        - fitness_level (str): Fitness level (e.g., 'intermediate')
        - goals (list of str): List of user goals

        Returns:
        - None: Prints confirmation after successful insertion
        """
        user_id = self.get_next_id("users", "user_id")
        gender_id = self.get_or_create_label_id("genders", gender)
        diet_type_id = self.get_or_create_label_id("diet_types", diet_type)
        fitness_level_id = self.get_or_create_label_id("fitness_levels", fitness_level)
        goal_ids = self.get_or_create_goal_ids(goals)

        self.conn.execute("""
            INSERT INTO users (user_id, age, gender_id, height, weight, target_weight, diet_type_id, fitness_level_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, age, gender_id, height, weight, target_weight, diet_type_id, fitness_level_id))

        for goal_id in goal_ids:
            self.conn.execute("INSERT OR IGNORE INTO user_goals (user_id, goal_id) VALUES (?, ?)", (user_id, goal_id))

        print(f"✅ User {user_id} inserted with {len(goal_ids)} goal(s)")

    def get_user_progress(self, user_id: int):
        """
        Retrieves current and target weight for a user, and calculates the difference.

        Parameters:
        - user_id (int): ID of the user

        Returns:
        - dict: A dictionary with weight, target, and kg to lose/gain
        - None: If the user does not exist
        """
        result = self.conn.execute("""
            SELECT user_id, weight, target_weight, (weight - target_weight) AS kg_to_lose
            FROM users WHERE user_id = ?
        """, (user_id,)).fetchone()

        if result:
            return {
                "user_id": result[0],
                "current_weight": result[1],
                "target_weight": result[2],
                "kg_to_lose": result[3]
            }
        return None

    def close(self):
        """
        Closes the DuckDB database connection.
        """
        self.conn.close()