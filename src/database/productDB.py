from tkinter import messagebox
from src.database.db import connect_database


def create_product_table():
    cursor, connection = connect_database()

    if not cursor:
        return

    try:
        cursor.execute(
            """
            create table if not exists product_data (
                id int primary key auto_increment,
                category_id int not null,
                supplier_id int not null,
                category_name varchar(100) not null,
                supplier_name varchar(100) not null,
                name varchar(100) not null,
                price decimal(10, 2),
                quantity int,
                status varchar(20),
                check (status in ('Active', 'Inactive')),
                foreign key (category_id) references category_data(id),
                foreign key (supplier_id) references supplier_data(invoice)
            )
            """
        )
    except Exception as e:
        print(f"Error creating product table: {e}")
        messagebox.showerror("Error", "Error creating product table")
    finally:
        cursor.close()
        connection.close()


def add_product(
    category_id,
    supplier_id,
    category_name,
    supplier_name,
    name,
    price,
    quantity,
    status,
    treeview_data,
):
    if (
        not category_id
        or not supplier_id
        or category_name == "Select"
        or supplier_name == "Select"
        or name == ""
        or price == ""
        or quantity == ""
        or status == "Select"
    ):
        messagebox.showerror("Error", "All fields are required")
        return
    else:
        cursor, connection = connect_database()

        if not cursor:
            return

        try:
            cursor.execute(
                """
                insert into product_data (
                    category_id,
                    supplier_id,
                    category_name,
                    supplier_name,
                    name,
                    price,
                    quantity,
                    status
                ) values (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    category_id,
                    supplier_id,
                    category_name,
                    supplier_name,
                    name,
                    price,
                    quantity,
                    status,
                ),
            )

            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Product added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding product: {e}")
        finally:
            cursor.close()
            connection.close()


def show_product():
    cursor, connection = connect_database()

    if not cursor:
        return

    try:
        cursor.execute("select * from product_data")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching product data: {e}")
        messagebox.showerror("Error", "Error fetching product data")
    finally:
        cursor.close()
        connection.close()


def update_product(
    category_id,
    supplier_id,
    category_name,
    supplier_name,
    name,
    price,
    quantity,
    status,
    treeview_data,
):
    if (
        category_name == "Select"
        or supplier_name == "Select"
        or name == ""
        or price == ""
        or quantity == ""
        or status == "Select"
    ):
        messagebox.showerror("Error", "All fields are required")
        return
    else:
        cursor, connection = connect_database()

        if not cursor:
            return

        try:
            cursor.execute(
                """
                update product_data set
                    category_name = %s,
                    supplier_name = %s,
                    name = %s,
                    price = %s,
                    quantity = %s,
                    status = %s
                where category_id = %s and supplier_id = %s
                """,
                (
                    category_name,
                    supplier_name,
                    name,
                    price,
                    quantity,
                    status,
                    category_id,
                    supplier_id,
                ),
            )

            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Product updated successfully")
        except Exception as e:
            print(f"Error updating product: {e}")
            messagebox.showerror("Error", f"Error updating product: {e}")
        finally:
            cursor.close()
            connection.close()


def delete_product(
    category_id,
    supplier_id,
    treeview_data,
):
    if not category_id or not supplier_id:
        messagebox.showerror("Error", "Category and supplier are required")
        return
    else:
        cursor, connection = connect_database()

        if not cursor:
            return

        try:
            cursor.execute(
                "delete from product_data where category_id = %s and supplier_id = %s",
                (category_id, supplier_id),
            )

            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Product deleted successfully")
        except Exception as e:
            print(f"Error deleting product: {e}")
            messagebox.showerror("Error", f"Error deleting product: {e}")
        finally:
            cursor.close()
            connection.close()


def search_product(search_by, search_text, product_treeview):
    if search_by == "Search By":
        messagebox.showerror("Error", "Please select a search criteria.")
        return
    elif not search_text:
        messagebox.showerror("Error", "Please enter a search text.")
        return
    else:
        search_by = search_by.replace(" ", "_")

        cursor, connection = connect_database()
        if not cursor:
            return

        try:
            cursor.execute(
                f"select * from product_data where {search_by.lower()} like %s",
                (f"%{search_text}%",),
            )
            records = cursor.fetchall()

            if not records:
                messagebox.showinfo("Info", "No records found!")
                return

            product_treeview.delete(*product_treeview.get_children())
            for record in records:
                product_treeview.insert("", "end", values=record)

        except Exception as e:
            messagebox.showerror("Error", f"Error in fetching data: {e}")
        finally:
            cursor.close()
            connection.close()
