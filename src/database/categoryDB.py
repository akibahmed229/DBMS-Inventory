from tkinter import messagebox
from src.database.db import connect_database


def create_category_table():
    cursor, connection = connect_database()

    if not cursor:
        return

    try:
        cursor.execute(
            """
            create table if not exists category_data (
                id int primary key,
                name varchar(100) not null,
                description varchar(200)
            )
            """
        )
    except Exception as e:
        messagebox.showerror("Error", f"Table Creation Failed: {e}")
    finally:
        cursor.close()
        connection.close()


def create_supplier_category_junction_table():
    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute(
            """
            create table if not exists supplier_category (
                supplier_id int,
                category_id int,
                primary key (supplier_id, category_id),
                foreign key (supplier_id) references supplier_data(invoice),
                foreign key (category_id) references category_data(id)
            );
            """
        )
    except Exception as e:
        messagebox.showerror("Error", f"Table creation failed: {e}")
        return
    finally:
        cursor.close()
        connection.close()


def add_category(id, name, description, supplier_invoice, treeview_data):
    if id == "" or name == "" or description == "":
        messagebox.showerror("Error", "All fields are required")
        return
    else:
        cursor, connection = connect_database()

        try:
            cursor.execute(
                """
                insert into category_data (id, name, description)
                values (%s, %s, %s)
                """,
                (id, name, description),
            )
            cursor.execute(
                """
                insert into supplier_category 
                values (%s, %s)
                """,
                (supplier_invoice, id),
            )
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Category Added Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Category Addition Failed: {e}")
        finally:
            cursor.close()
            connection.close()


def delete_category(id, treeview_data):
    if id == "":
        messagebox.showerror("Error", "Category ID is required")
        return
    else:
        cursor, connection = connect_database()

        try:
            cursor.execute("delete from category_data where id=%s", (id,))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Category Deleted Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Category Deletion Failed: {e}")
        finally:
            cursor.close()
            connection.close()


def show_category():
    cursor, connection = connect_database()

    if not cursor:
        return

    try:
        cursor.execute("select * from category_data")
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Category Data Fetch Failed: {e}")
    finally:
        cursor.close()
        connection.close()
