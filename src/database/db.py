from tkinter import messagebox
import pymysql


def connect_database():
    """Connect to the MySQL database and ensure the employee_data table exists."""
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3366,
            user="inventory_user",
            password="123",
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")

    except Exception as e:
        messagebox.showerror("Error", f"Database Connection Failed: {e}")
        return None, None

    return cursor, connection
