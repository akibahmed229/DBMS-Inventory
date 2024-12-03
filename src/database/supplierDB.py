from tkinter import messagebox
from src.database.db import connect_database


def create_supplier_table():
    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute(
            """
                create table if not exists supplier_data (
                    invoice int primary key,
                    empid int,
                    name varchar(50) not null,
                    contact varchar(15),
                    description text,
                    foreign key (empid) references employee_data(empid)
                )
            """
        )
    except Exception as e:
        messagebox.showerror("Error", f"Table creation failed: {e}")
        return
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
                primary key (supplier_id) references supplier_data(invoice),
                primary key (category_id) references category_data(id)
            );
            """
        )
    except Exception as e:
        messagebox.showerror("Error", f"Table creation failed: {e}")
        return
    finally:
        cursor.close()
        connection.close()


def add_supplier(
    empid,
    invoice,
    contact,
    supplierName,
    description,
    treeview_data,
):
    if (
        invoice == ""
        or contact == ""
        or supplierName == ""
        or description.strip() == ""
    ):
        messagebox.showerror("Error", "All fields are required")
    else:
        cursor, connection = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("select * from supplier_data where invoice=%s", (invoice,))

            if cursor.fetchone():
                messagebox.showerror("Error", "Invoice already exists")
                return

            cursor.execute(
                """
                insert into supplier_data (invoice, empid, name, contact, description)
                values (%s, %s, %s, %s, %s)
            """,
                (invoice, empid, supplierName, contact, description.strip()),
            )

            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Supplier added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Insertion failed: {e}")
            return
        finally:
            cursor.close()
            connection.close()


def show_supplier(empid):
    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute("select * from supplier_data where empid=%s", (empid,))
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Error in fetching data: {e}")
        return
    finally:
        cursor.close()
        connection.close()


def update_supplier(
    empid, invoice, contact, supplierName, description, treeview_data, supplier_treeview
):
    index = supplier_treeview.selection()

    if not index:
        messagebox.showerror("Error", "Select a row to update")
    elif (
        invoice == ""
        or contact == ""
        or supplierName == ""
        or description.strip() == ""
    ):
        messagebox.showerror("Error", "All fields are required")
    else:
        cursor, connection = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("select * from supplier_data where invoice=%s", (invoice,))

            current_invoice = cursor.fetchone()

            if current_invoice[1] != int(empid):
                messagebox.showerror(
                    "Error", "You are not authorized to update this data"
                )
                return

            new_data = (
                int(invoice),
                int(empid),
                supplierName,
                contact,
                description.strip(),
            )

            if current_invoice == new_data:
                messagebox.showerror("Error", "No changes made")
                return

            cursor.execute(
                """
                update supplier_data
                set name=%s, contact=%s, description=%s
                where invoice=%s
            """,
                (supplierName, contact, description.strip(), invoice),
            )

            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Supplier updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")
            return
        finally:
            cursor.close()
            connection.close()


def delete_supplier(invoice, treeview_data):
    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute("delete from supplier_data where invoice=%s", (invoice,))
        connection.commit()
        treeview_data()
        messagebox.showinfo("Success", "Supplier deleted successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Deletion failed: {e}")
        return
    finally:
        cursor.close()
        connection.close()


def search_supplier(invoice, treeview_data):
    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute("select * from supplier_data where invoice=%s", (invoice,))

        treeview_data()

        return cursor.fetchone()
    except Exception as e:
        messagebox.showerror("Error", f"Error in fetching data: {e}")
        return
    finally:
        cursor.close()
        connection.close()
