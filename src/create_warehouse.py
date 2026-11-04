
import mysql.connector
import os

from pathlib import Path
from dotenv import load_dotenv


# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load database credentials
load_dotenv(BASE_DIR / ".env")


# Database connection settings
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
}


# Find the warehouse schema file
SCHEMA_FILE = BASE_DIR / "sql" / "warehouse" / "schema.sql"


def create_warehouse():

    # Connect to MySQL without selecting a database
    connection = mysql.connector.connect(**DB_CONFIG)

    cursor = connection.cursor()

    try:
        # Read the SQL schema
        with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
            schema = file.read()

        # Execute each SQL statement
        for statement in schema.split(";"):

            statement = statement.strip()

            if statement:
                cursor.execute(statement)

        connection.commit()

        print("Data warehouse created successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_warehouse()
