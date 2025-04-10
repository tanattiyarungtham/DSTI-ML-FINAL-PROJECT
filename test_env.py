import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path("env_folder/.env.postgre").resolve()
load_dotenv(dotenv_path)

print("POSTGRES_USER:", os.getenv("POSTGRES_USER"))
print("POSTGRES_PASSWORD:", os.getenv("POSTGRES_PASSWORD"))
print("POSTGRES_DB:", os.getenv("POSTGRES_DB"))
