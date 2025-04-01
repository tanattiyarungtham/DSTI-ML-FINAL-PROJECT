import psycopg2
import os

def get_connection():
    """
    Establishes a connection to a PostgreSQL database using environment variables.

    Returns:
    - psycopg2.connection: Active connection to the database
    """
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432)
    )

def execute_schema():
    """
    Reads and executes the schema.sql file to create necessary tables in the PostgreSQL database.
    Supports multiple CREATE TABLE statements.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            with open(schema_path, "r") as f:
                sql_commands = f.read().split(";")  # Split on semicolon
                for command in sql_commands:
                    command = command.strip()
                    if command:  # Skip empty strings
                        cur.execute(command)
        conn.commit()
        print("✅ Schema executed: all tables created (if not exist)")