from tkinter import messagebox
from src.database.db import connect_database


def get_total_count():
    cursor, connection = connect_database()

    if not cursor:
        return

    try:
        cursor.execute("SELECT COUNT(*) FROM employee_data")
        total_emp = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM supplier_data")
        total_sup = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM category_data")
        total_cat = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM product_data")
        total_prod = cursor.fetchone()[0]

        return total_emp, total_sup, total_cat, total_prod
    except Exception as e:
        print(f"Error getting total count: {e}")
        messagebox.showerror("Error", "Error getting total count")
    finally:
        cursor.close()
        connection.close()
