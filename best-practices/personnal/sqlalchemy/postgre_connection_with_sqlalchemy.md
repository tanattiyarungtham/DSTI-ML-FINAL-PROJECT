# 📂 PostgreSQL Connection with SQLAlchemy

This document explains, line by line, how the file `back_end/database/connect.py` works using **SQLAlchemy** to manage a PostgreSQL connection in a Python project.

---

## 🔄 Prerequisites

Before diving into the code, make sure you have the necessary dependencies installed:

```bash
pip install sqlalchemy psycopg2 python-dotenv
```

- `sqlalchemy`: ORM and DB toolkit for Python
- `psycopg2`: PostgreSQL database adapter
- `python-dotenv`: Loads environment variables from a `.env` file

---

## 📁 File: `back_end/database/connect.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
```

### ✅ Explanation:
- `sqlalchemy.create_engine`: Establishes a connection to your PostgreSQL DB.
- `sqlalchemy.orm.sessionmaker`: Creates a factory for database sessions.
- `dotenv.load_dotenv`: Loads environment variables defined in `.env`.
- `os`: Accesses environment variables from the system.

---

## ⚖️ Load Environment Variables

```python
load_dotenv()
```
Loads the `.env` file, so that credentials and configuration can be accessed securely.

---

## 🌐 Define `DATABASE_URL`

```python
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', 5432)}/{os.getenv('POSTGRES_DB')}"
)
```

### ✅ Explanation:
Constructs the full PostgreSQL connection string dynamically using the values in the `.env` file.

**Example resulting URI:**
```
postgresql+psycopg2://postgres:your_password@localhost:5432/fitnessdb
```

---

## 🚀 Create Engine & Session Factory

```python
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### ✅ Explanation:
- `engine`: Represents the core DB connection; used to issue raw SQL or connect ORM models.
- `SessionLocal`: Each instance is a DB session, used in API endpoints or scripts to interact with the database.
- `autocommit=False`: Manual commit needed (`session.commit()`).
- `autoflush=False`: You control when DB is flushed (pushed) with `flush()`.

---

## 🧱 Dependency for Session Access

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### ✅ Explanation:
- Yields a DB session for use in FastAPI or script.
- Ensures proper closing of the session after use.

#### 📅 Step-by-step Breakdown

1. `SessionLocal()`:
   - Creates a new SQLAlchemy session from the pre-configured session factory.
   - This represents a single DB connection for the current context.

2. `yield db`:
   - Provides the session to the calling function (like a route or a service).
   - `yield` makes this a generator, allowing FastAPI to manage the session lifecycle.

3. `finally: db.close()`:
   - Ensures the session is closed properly after use.
   - Prevents connection leaks and keeps the application efficient.

- Can be used in FastAPI endpoints:
```python
@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM users").fetchall()
```

### ✅ Benefits
- Clean separation of database logic
- Automatic session handling
- Essential for scalable FastAPI apps

---

## 🔧 Execute Schema

```python
def execute_schema():
    with engine.connect() as connection:
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            sql_commands = f.read().split(";")
            for command in sql_commands:
                command = command.strip()
                if command:
                    connection.execute(command)
        print("Schema executed: all tables created (if not exist)")
```

### ✅ Explanation:
- Connects to the DB using the SQLAlchemy engine.
- Reads all SQL commands from `schema.sql`, splits by `;` (one command per statement).
- Executes each valid SQL command to create tables if they don't exist.

This method is helpful to **bootstrap your database schema** in one command.

#### 🔄 Process Breakdown

1. **Connect to DB**:
   - `engine.connect()` opens a raw connection to the PostgreSQL database.

2. **Load Schema File**:
   - Finds the `schema.sql` file relative to the script's path.
   - Reads the entire content into memory.

3. **Execute Commands**:
   - Splits the content into commands using `;`.
   - Executes each non-empty SQL command one by one.

4. **Feedback**:
   - Logs confirmation when the schema setup completes.
---

## 📄 .env File Example
```
POSTGRES_DB=fitnessdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

> ⚠️ Remember to add `.env` to `.gitignore` so it is not committed:
```
# .gitignore
.env
```

---

## 🔹 Usage in CLI or Script
```python
from back_end.database.connect import execute_schema

if __name__ == "__main__":
    execute_schema()
```

---

## 📊 Summary
| Concept | Description |
|--------|-------------|
| `SQLAlchemy Engine` | Core DB connection object |
| `SessionLocal` | Factory to produce transactional sessions |
| `get_db()` | Dependency to inject DB sessions in apps or scripts |
| `execute_schema()` | Loads and runs schema SQL file on PostgreSQL |

---

✅ You’re now ready to integrate `SQLAlchemy` into your backend with clean architecture and production-ready configuration.

Let me know if you want to integrate Alembic (for migrations) or define your tables with SQLAlchemy ORM!

-------
