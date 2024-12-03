from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date

from src.components.button import create_button
from src.database.employeeDB import (
    delete_employee,
    update_employee,
    create_employee_table,
    add_employee,
    show_employee,
    delete_employee,
    search_employee,
)


def treeview_data():
    employee_records = show_employee()

    employee_treeview.delete(*employee_treeview.get_children())
    for record in employee_records:
        employee_treeview.insert("", "end", values=record)


def show_all(search_combobox, search_entry):
    treeview_data()

    search_combobox.set("Search By")
    search_entry.delete(0, END)


def clear_employee_form(
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
    check=False,
):
    empid.delete(0, END)
    name.delete(0, END)
    email.delete(0, END)
    gender.set("Select")
    dob.set_date(date.today())
    contact.delete(0, END)
    emp_type.set("Select")
    education.set("Select")
    work_shift.set("Select")
    address.delete("1.0", END)
    doj.set_date(date.today())
    salary.delete(0, END)
    user_type.set("Select User Type")
    password.delete(0, END)

    if check:
        employee_treeview.selection_remove(employee_treeview.selection())


def select_employee(
    event,
    empid_entry,
    name_entry,
    email_entry,
    gender_combobox,
    dob_entry,
    contact_entry,
    emp_type_combobox,
    education_combobox,
    work_shift_combobox,
    address_text,
    doj_entry,
    salary_entry,
    user_type_combobox,
    password_entry,
):
    index = employee_treeview.selection()
    content = employee_treeview.item(index)

    row = content["values"]

    clear_employee_form(
        empid_entry,
        name_entry,
        email_entry,
        gender_combobox,
        dob_entry,
        contact_entry,
        emp_type_combobox,
        education_combobox,
        work_shift_combobox,
        address_text,
        doj_entry,
        salary_entry,
        user_type_combobox,
        password_entry,
        check=False,
    )

    empid_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    emp_type_combobox.set(row[6])
    education_combobox.set(row[7])
    work_shift_combobox.set(row[8])
    address_text.insert(END, row[9])
    doj_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    user_type_combobox.set(row[12])
    password_entry.insert(0, row[13])


# Utility Functions
def create_label_entry_pair(parent, text, row, column, entry_var=None, width=20):
    """Create a label and an entry widget as a pair."""
    label = Label(parent, text=text, font=("Arial", 12), bg="#0F0C0C", fg="white")
    label.grid(row=row, column=column, padx=20, pady=10)
    entry = Entry(
        parent, font=("Arial", 10), bg="lightgray", textvariable=entry_var, width=width
    )
    entry.grid(row=row, column=column + 1, padx=20, pady=10)
    return entry


def create_label_combobox_pair(parent, text, row, column, values, default="Select"):
    """Create a label and a combobox widget as a pair."""
    label = Label(parent, text=text, font=("Arial", 12), bg="#0F0C0C", fg="white")
    label.grid(row=row, column=column, padx=20, pady=10)
    combobox = ttk.Combobox(
        parent, values=values, state="readonly", font=("Arial", 10), width=18
    )
    combobox.set(default)
    combobox.grid(row=row, column=column + 1, padx=20, pady=10)
    return combobox


def create_action_button(parent, text, command, row, column):
    """Create a button for performing actions."""
    button = create_button(
        parent,
        text=text,
        font=("Arial", 10),
        bg="#AF8F6F",
        width=8,
        command=command,
    )
    button.grid(row=row, column=column, padx=10, pady=10)


# GUI Components
def employee_form(parent, employee_data):
    global employee_treeview
    create_employee_table()

    """Render the Employee Management form."""
    employee_frame = Frame(parent, bg="#251E1E", relief=RIDGE, bd=2)
    employee_frame.place(x=0, y=0, width=1020, height=620)

    # Header
    heading_label = Label(
        employee_frame,
        text="Employee Management",
        font=("Arial", 16, "bold"),
        bg="#AF8F6F",
        fg="white",
    )
    heading_label.place(x=0, y=0, relwidth=1)

    # Back Button
    back_button = create_button(
        frame=employee_frame,
        text="Back",
        command=lambda: employee_frame.destroy(),
        font=("Arial", 10),
    )
    back_button.place(x=0, y=0)

    # Top Frame - Search and TreeView
    top_frame = Frame(employee_frame, bg="#0F0C0C")
    top_frame.place(x=0, y=40, relwidth=1, height=300)

    search_frame = Frame(top_frame, bg="#0F0C0C")
    search_frame.pack()

    search_combobox = ttk.Combobox(
        search_frame,
        values=["Name", "Email", "Contact", "EmpId", "Emp Type"],
        state="readonly",
        font=("Arial", 10),
        width=12,
    )
    search_combobox.set("Search By")
    search_combobox.grid(row=0, column=0, padx=10, pady=10)
    search_entry = Entry(search_frame, font=("Arial", 12), bg="lightgray")
    search_entry.grid(row=0, column=1, padx=10, pady=10)
    search_button = Button(
        search_frame,
        text="Search",
        font=("Arial", 10),
        bg="#AF8F6F",
        fg="white",
        width=8,
        cursor="hand2",
        activebackground="#C5705D",
        command=lambda: search_employee(
            search_combobox.get(), search_entry.get(), employee_treeview
        ),
    )
    search_button.grid(row=0, column=2, padx=10, pady=10)
    show_all_button = Button(
        search_frame,
        text="Show All",
        font=("Arial", 10),
        bg="#AF8F6F",
        fg="white",
        width=8,
        cursor="hand2",
        activebackground="#C5705D",
        command=lambda: show_all(search_combobox, search_entry),
    )
    show_all_button.grid(row=0, column=3, padx=10, pady=10)

    # TreeView for employee data
    horizontal_scrollbar = Scrollbar(top_frame, orient="horizontal")
    vertical_scrollbar = Scrollbar(top_frame, orient="vertical")

    employee_treeview = ttk.Treeview(
        top_frame,
        columns=[str(i) for i in range(1, 14)],
        show="headings",
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
        height=10,
    )
    horizontal_scrollbar.pack(side="bottom", fill="x")
    vertical_scrollbar.pack(side="right", fill="y")
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(fill="both", expand=True)

    for i, heading in enumerate(
        [
            "EmpID",
            "Name",
            "Email",
            "Gender",
            "DOB",
            "Contact",
            "Emp Type",
            "Education",
            "Work Shift",
            "Address",
            "Date of Joining",
            "Salary",
            "User Type",
        ],
        start=1,
    ):
        employee_treeview.heading(i, text=heading)
        employee_treeview.column(i, width=120)

    treeview_data()  # Fetch data from the database

    # Bottom Frame - Employee Details
    details_frame = Frame(employee_frame, bg="#0F0C0C")
    details_frame.place(x=0, y=340, relwidth=1, height=280)

    # Employee Details Input Fields
    empid_entry = create_label_entry_pair(details_frame, "Emp ID", 0, 0)
    name_entry = create_label_entry_pair(details_frame, "Name", 0, 2)
    email_entry = create_label_entry_pair(details_frame, "Email", 0, 4)

    gender_combobox = create_label_combobox_pair(
        details_frame, "Gender", 1, 0, ["Male", "Female"]
    )
    dob_label = Label(
        details_frame, text="DOB", font=("Arial", 12), bg="#0F0C0C", fg="white"
    )
    dob_label.grid(row=1, column=2, padx=20, pady=10)

    dob_entry = DateEntry(
        details_frame,
        font=("Arial", 10),
        width=18,
        bg="lightgray",
        state="readonly",
        date_pattern="YYYY-MM-DD",
    )
    dob_entry.grid(row=1, column=3, padx=20, pady=10)

    contact_entry = create_label_entry_pair(details_frame, "Contact", 1, 4)
    emp_type_combobox = create_label_combobox_pair(
        details_frame, "Emp Type", 2, 0, ["Full Time", "Part Time"]
    )
    education_combobox = create_label_combobox_pair(
        details_frame,
        "Education",
        2,
        2,
        ["High School", "Diploma", "Graduate", "Post Graduate"],
    )
    work_shift_combobox = create_label_combobox_pair(
        details_frame, "Work Shift", 2, 4, ["Morning", "Evening", "Night"]
    )

    address_label = Label(
        details_frame, text="Address", font=("Arial", 12), bg="#0F0C0C", fg="white"
    )
    address_label.grid(row=3, column=0, padx=20, pady=10)
    address_text = Text(
        details_frame, font=("Arial", 10), bg="lightgray", width=19, height=3
    )
    address_text.grid(row=3, column=1, padx=20, pady=10, rowspan=2)
    doj_label = Label(
        details_frame,
        text="Date Join",
        font=("Arial", 12),
        bg="#0F0C0C",
        fg="white",
    )
    doj_label.grid(row=3, column=2, padx=20, pady=10)
    doj_entry = DateEntry(
        details_frame,
        font=("Arial", 10),
        bg="lightgray",
        width=18,
        state="readonly",
        date_pattern="YYYY-MM-DD",
    )
    doj_entry.grid(row=3, column=3, padx=20, pady=10)

    salary_label = Label(
        details_frame, text="Salary", font=("Arial", 12), bg="#0F0C0C", fg="white"
    )
    salary_label.grid(row=3, column=4, padx=20, pady=10)
    salary_entry = Entry(details_frame, font=("Arial", 10), bg="lightgray")
    salary_entry.grid(row=3, column=5, padx=20, pady=10)

    user_type_label = Label(
        details_frame, text="User Type", font=("Arial", 12), bg="#0F0C0C", fg="white"
    )
    user_type_label.grid(row=4, column=2, padx=20, pady=10)
    user_type_combobox = ttk.Combobox(
        details_frame,
        values=["Admin", "Employee"],
        state="readonly",
        font=("Arial", 10),
        width=18,
    )
    user_type_combobox.set(value="Select User Type")
    user_type_combobox.grid(row=4, column=3, padx=20, pady=10)

    password_label = Label(
        details_frame, text="Password", font=("Arial", 12), bg="#0F0C0C", fg="white"
    )
    password_label.grid(row=4, column=4, padx=20, pady=10)
    password_entry = Entry(details_frame, font=("Arial", 10), bg="lightgray")
    password_entry.grid(row=4, column=5, padx=20, pady=10)

    # Buttons
    create_action_button(
        details_frame,
        "Add",
        lambda: add_employee(
            empid_entry.get(),
            name_entry.get(),
            email_entry.get(),
            gender_combobox.get(),
            dob_entry.get(),
            contact_entry.get(),
            emp_type_combobox.get(),
            education_combobox.get(),
            work_shift_combobox.get(),
            address_text.get("1.0", END),
            doj_entry.get(),
            salary_entry.get(),
            user_type_combobox.get(),
            password_entry.get(),
            treeview_data,
        ),
        5,
        1,
    )
    create_action_button(
        details_frame,
        "Update",
        lambda: update_employee(
            empid_entry.get(),
            name_entry.get(),
            email_entry.get(),
            gender_combobox.get(),
            dob_entry.get(),
            contact_entry.get(),
            emp_type_combobox.get(),
            education_combobox.get(),
            work_shift_combobox.get(),
            address_text.get("1.0", END),
            doj_entry.get(),
            salary_entry.get(),
            user_type_combobox.get(),
            password_entry.get(),
            employee_treeview,
            treeview_data,
        ),
        5,
        2,
    )
    create_action_button(
        details_frame,
        "Delete",
        lambda: delete_employee(
            empid_entry.get(),
            employee_treeview,
            treeview_data,
        ),
        5,
        3,
    )
    create_action_button(
        details_frame,
        "Clear",
        lambda: clear_employee_form(
            empid_entry,
            name_entry,
            email_entry,
            gender_combobox,
            dob_entry,
            contact_entry,
            emp_type_combobox,
            education_combobox,
            work_shift_combobox,
            address_text,
            doj_entry,
            salary_entry,
            user_type_combobox,
            password_entry,
            check=True,
        ),
        5,
        4,
    )

    employee_treeview.bind(
        "<ButtonRelease-1>",
        lambda event: select_employee(
            event,
            empid_entry,
            name_entry,
            email_entry,
            gender_combobox,
            dob_entry,
            contact_entry,
            emp_type_combobox,
            education_combobox,
            work_shift_combobox,
            address_text,
            doj_entry,
            salary_entry,
            user_type_combobox,
            password_entry,
        ),
    )
