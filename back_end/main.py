# Entry point to initialize the database structure

from database.connect import execute_schema

if __name__ == "__main__":
    execute_schema()  # Will create users table if it doesn't exist