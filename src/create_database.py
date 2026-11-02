
import mysql.connector
from dotenv import load_dotenv
import os

# 1. Load database credentials
load_dotenv()

connection = None
cursor = None

try:
    # 2. Connect to MySQL
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = connection.cursor()

    print("Connected to MySQL successfully!")

    # 3. Read the SQL schema file
    schema_path = os.path.join(
        os.path.dirname(__file__),
        "schema.sql"
    )

    with open(schema_path, "r") as file:
        schema = file.read()

    # 4. Execute each SQL statement
    for statement in schema.split(";"):
        if statement.strip():
            cursor.execute(statement)

    print("Database schema created successfully!")

except mysql.connector.Error as error:
    print("Database creation failed.")
    print("Error:", error)

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
