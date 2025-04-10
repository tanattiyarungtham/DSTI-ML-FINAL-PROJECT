**PostgreSQL Setup — Running via Docker**

  

To run PostgreSQL locally using Docker, follow the instructions below.

---

**Step-by-Step: How to Launch PostgreSQL**

1. **Make sure Docker is installed and running**

• Download it from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

• Start the Docker Desktop app

2. **Start the PostgreSQL container**

In your project root (where your docker-compose.yml is located), run:

```
docker-compose up -d
```

This command:

• Downloads the official postgres:15 image if needed

• Starts a container named fitness-postgres

• Exposes port 5432 locally

• Loads environment variables defined in the YAML

• Creates a volume pg_data to persist data

---

**Stopping PostgreSQL**

  

To stop the container (without losing data):

```
docker-compose down
```

> If you also want to delete the volume (⚠️ data loss):

```
docker-compose down -v
```

  

---

**Important Note**

  

Your application will **not** connect to the database unless Docker is running and the PostgreSQL container is active.

  

You can check if PostgreSQL is running with:

```
docker ps
```

  

---

**✅ Verifying the Connection (Optional)**

  

If you want to check if PostgreSQL is accepting connections:

```
docker exec -it fitness-postgres psql -U postgres -d fitnessdb
```

Or run:

```
pg_isready -h localhost -p 5432
```

(Install the postgresql-client package if not available)

---

Let me know if you want this turned into a markdown file or added into your project’s README.md!