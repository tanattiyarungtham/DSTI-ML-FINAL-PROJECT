# back_end/database/repository/user_repository.py

from back_end.database.connect import get_connection

class UserRepository:
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def get_or_create_label_id(self, table, label, id_col="id"):
        self.cur.execute(f"SELECT {id_col} FROM {table} WHERE label = %s", (label,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        self.cur.execute(f"INSERT INTO {table} (label) VALUES (%s) RETURNING {id_col}", (label,))
        return self.cur.fetchone()[0]

    def get_or_create_goal_ids(self, goal_labels):
        ids = []
        for label in goal_labels:
            self.cur.execute("SELECT goal_id FROM goals WHERE label = %s", (label,))
            result = self.cur.fetchone()
            if result:
                ids.append(result[0])
            else:
                self.cur.execute("INSERT INTO goals (label) VALUES (%s) RETURNING goal_id", (label,))
                ids.append(self.cur.fetchone()[0])
        return ids

    def insert_user(self, age, gender, height, weight, target_weight, diet_type, fitness_level, goals):
        gender_id = self.get_or_create_label_id("genders", gender)
        diet_type_id = self.get_or_create_label_id("diet_types", diet_type)
        fitness_level_id = self.get_or_create_label_id("fitness_levels", fitness_level)
        goal_ids = self.get_or_create_goal_ids(goals)

        self.cur.execute("""
            INSERT INTO users (age, gender_id, height, weight, target_weight, diet_type_id, fitness_level_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id
        """, (age, gender_id, height, weight, target_weight, diet_type_id, fitness_level_id))
        user_id = self.cur.fetchone()[0]

        for goal_id in goal_ids:
            self.cur.execute(
                "INSERT INTO user_goals (user_id, goal_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (user_id, goal_id)
            )

        self.conn.commit()
        return user_id

    def close(self):
        self.cur.close()
        self.conn.close()