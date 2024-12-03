from tkinter import messagebox
from src.database.db import connect_database


def create_employee_table():
    cursor, connection = connect_database()

    if not cursor:
        return

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employee_data (
                empid INT PRIMARY KEY, 
                name VARCHAR(100) NOT NULL, 
                email VARCHAR(100) UNIQUE,
                gender VARCHAR(50),
                dob DATE,
                contact VARCHAR(20),
                emp_type VARCHAR(50),
                education VARCHAR(50),
                work_shift VARCHAR(50),
                address VARCHAR(200),
                doj DATE,
                salary INT CHECK (salary >= 0),
                user_type VARCHAR(50) CHECK (user_type IN ('Admin', 'Employee')),
                password VARCHAR(50),
                CHECK (emp_type IN ('Full Time', 'Part Time'))
                )
            """
        )
    except Exception as e:
        messagebox.showerror("Error", f"Table Creation Failed: {e}")
    finally:
        cursor.close()
        connection.close()


def add_employee(
    empid,
    name,
    email,
    gender,
    dob,
    contact,
    emp_type,
    education,
    work_shift,
    address,
    doj,
    salary,
    user_type,
    password,
    treeview_data,
):
    if (
        empid == ""
        or name == ""
        or email == ""
        or gender == "Select"
        or contact == ""
        or emp_type == "Select"
        or education == "Select"
        or work_shift == "Select"
        or address == "\n"
        or salary == ""
        or user_type == "Select User Type"
        or password == ""
    ):
        messagebox.showerror("Error", "All fields are required!")
        return
    else:
        cursor, connection = connect_database()
        if not cursor:
            return

        try:
            empid_exist = cursor.execute(
                "select empid from employee_data where empid=%s", (empid,)
            )
            if empid_exist:
                messagebox.showerror("Error", "Employee ID already exists!")
                return

            address = address.strip()  # Remove leading and trailing whitespaces

            cursor.execute(
                """
                insert into employee_data value (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    empid,
                    name,
                    email,
                    gender,
                    dob,
                    contact,
                    emp_type,
                    education,
                    work_shift,
                    address.strip(),
                    doj,
                    salary,
                    user_type,
                    password,
                ),
            )

            connection.commit()
            treeview_data()

            messagebox.showinfo("Success", "Employee added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error in insertion: {e}")
        finally:
            cursor.close()
            connection.close()


def show_employee():
    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute("select * from employee_data")
        data = cursor.fetchall()
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Error in fetching data: {e}")
    finally:
        cursor.close()
        connection.close()


def update_employee(
    empid,
    name,
    email,
    gender,
    dob,
    contact,
    emp_type,
    education,
    work_shift,
    address,
    doj,
    salary,
    user_type,
    password,
    employee_treeview,
    treeview_data,
):
    selected = employee_treeview.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a record to update!")
        return
    else:
        cursor, connection = connect_database()

        if not cursor:
            return

        try:
            cursor.execute(
                """
                select * from employee_data where empid=%s
                """,
                (empid,),
            )
            current_data = cursor.fetchone()
            current_data = list(current_data[1:])
            current_data[3] = current_data[3].strftime("%Y-%m-%d")
            current_data[9] = current_data[9].strftime("%Y-%m-%d")

            current_data = tuple(current_data)

            address = address.strip()

            new_data = (
                name,
                email,
                gender,
                dob,
                contact,
                emp_type,
                education,
                work_shift,
                address.strip(),
                doj,
                int(salary),
                user_type,
                password,
            )

            if current_data == new_data:
                messagebox.showerror("Error", "No changes made to the record!")
                return

            cursor.execute(
                """
                update employee_data set 
                    name=%s,
                    email=%s,
                    gender=%s,
                    dob=%s,
                    contact=%s,
                    emp_type=%s,
                    education=%s,
                    work_shift=%s,
                    address=%s,
                    doj=%s,
                    salary=%s,
                    user_type=%s,
                    password=%s
                where empid=%s
            """,
                (
                    name,
                    email,
                    gender,
                    dob,
                    contact,
                    emp_type,
                    education,
                    work_shift,
                    address,
                    doj,
                    salary,
                    user_type,
                    password,
                    empid,
                ),
            )
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Employee record updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error in updating record: {e}")
        finally:
            cursor.close()
            connection.close()


def delete_employee(
    empid,
    employee_treeview,
    treeview_data,
):
    selectd = employee_treeview.selection()

    if not selectd:
        messagebox.showerror("Error", "Please select a record to delete!")
        return
    else:
        result = messagebox.askyesno(
            "Cnfirmation", "Do you want to delete this record?"
        )

        if result:
            cursor, connection = connect_database()

            if not cursor:
                return

            try:
                cursor.execute(
                    """
                    delete from employee_data where empid=%s
                    """,
                    (empid,),
                )
                connection.commit()
                treeview_data()

                messagebox.showinfo("Success", "Record deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Error in deletion: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            return


def search_employee(search_by, search_text, employee_treeview):
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
                f"select * from employee_data where {search_by.lower()} like %s",
                (f"%{search_text}%",),
            )
            records = cursor.fetchall()

            if not records:
                messagebox.showinfo("Info", "No records found!")
                return

            employee_treeview.delete(*employee_treeview.get_children())
            for record in records:
                employee_treeview.insert("", "end", values=record)

        except Exception as e:
            messagebox.showerror("Error", f"Error in fetching data: {e}")
        finally:
            cursor.close()
            connection.close()


def login_employee(email):
    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute(
            f"select * from employee_data where email=%s",
            (email,),
        )
        records = cursor.fetchall()

        if not records:
            return None
        else:
            return records

    except Exception as e:
        messagebox.showerror("Error", f"Error in fetching data: {e}")
    finally:
        cursor.close()
        connection.close()
