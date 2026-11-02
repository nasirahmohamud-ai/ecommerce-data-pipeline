
import os
import mysql.connector
from dotenv import load_dotenv

# Load database settings from the .env file
load_dotenv()

config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "ecommerce_dw"),
}

connection = None

try:
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        print("Successfully connected to MySQL!")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()

        print("Connected database:", result[0])
        cursor.close()

except mysql.connector.Error as error:
    print("MySQL connection failed.")
    print("Error:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
