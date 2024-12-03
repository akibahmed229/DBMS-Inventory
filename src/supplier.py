from tkinter import *
from tkinter.ttk import Treeview
from src.components.button import create_button

from src.database.supplierDB import (
    add_supplier,
    create_supplier_table,
    delete_supplier,
    search_supplier,
    show_supplier,
    update_supplier,
)


# Utility Functions
def treeview_data():
    supplier_records = show_supplier(currentEmpID)

    supplier_treeview.delete(*supplier_treeview.get_children())
    for record in supplier_records:
        supplier_treeview.insert("", "end", values=record)


def clear_fields(
    invoice_entry,
    supplierName_entry,
    contact_entry,
    description_text,
    check=False,
):
    invoice_entry.delete(0, END)
    supplierName_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)

    if check:
        supplier_treeview.selection_remove(supplier_treeview.selection())


def select_supplier(
    event,
    invoice_entry,
    supplierName_entry,
    contact_entry,
    description_text,
    supplier_treeview,
):
    index = supplier_treeview.selection()
    content = supplier_treeview.item(index, "values")

    invoice_entry.delete(0, END)
    supplierName_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)

    invoice_entry.insert(0, content[0])
    supplierName_entry.insert(0, content[2])
    contact_entry.insert(0, content[3])
    description_text.insert(1.0, content[4])


def create_label_entry_pair(parent, text, row, column, entry_var=None, width=20):
    """Create a label and an entry widget as a pair."""
    label = Label(parent, text=text, font=("Arial", 12), bg="#0F0C0C", fg="white")
    label.grid(row=row, column=column, padx=20, pady=10, sticky="w")
    entry = Entry(
        parent, font=("Arial", 12), bg="lightgray", textvariable=entry_var, width=width
    )
    entry.grid(row=row, column=column + 1, padx=20, pady=10)
    return entry


def create_action_button(parent, text, command, row, column):
    """Create a button for performing actions."""
    button = create_button(
        parent,
        text=text,
        font=("Arial", 8),
        bg="#AF8F6F",
        width=6,
        command=command,
    )
    button.grid(row=row, column=column, padx=10, pady=10)


def supplier_form(parent, employee_data):
    global supplier_treeview
    global currentEmpID
    currentEmpID = employee_data[0][0]
    create_supplier_table()

    supplier_frame = Frame(parent, bg="#0F0C0C", relief=SUNKEN, bd=1)
    supplier_frame.place(x=0, y=0, width=1020, height=620)

    # Header
    heading_label = Label(
        supplier_frame,
        text="Manage Supplier",
        font=("Arial", 16, "bold"),
        bg="#AF8F6F",
        fg="white",
    )
    heading_label.place(x=0, y=0, relwidth=1)

    # Back Button
    back_button = create_button(
        frame=supplier_frame,
        text="Back",
        command=lambda: supplier_frame.destroy(),
        font=("Arial", 10),
    )
    back_button.place(x=0, y=0)

    left_frame = Frame(supplier_frame, bg="#0F0C0C")
    left_frame.place(x=10, y=50)

    invoice_entry = create_label_entry_pair(left_frame, "Invoice No.", 0, 0)
    supplierName_entry = create_label_entry_pair(left_frame, "Supplier Name", 1, 0)
    contact_entry = create_label_entry_pair(left_frame, "Contact", 2, 0)

    description_label = Label(
        left_frame, text="Address", font=("Arial", 12), bg="#0F0C0C", fg="white"
    )
    description_label.grid(row=3, column=0, padx=20, pady=10, sticky="nw")
    description_text = Text(
        left_frame,
        height=6,
        width=25,
        bd=2,
        background="lightgray",
    )
    description_text.grid(row=3, column=1, padx=20, pady=10)

    # button
    button_frame = Frame(left_frame, bg="#0F0C0C")
    button_frame.grid(row=4, columnspan=2)

    create_action_button(
        button_frame,
        "Add",
        lambda: add_supplier(
            employee_data[0][0],
            invoice_entry.get(),
            contact_entry.get(),
            supplierName_entry.get(),
            description_text.get(1.0, END).strip(),
            treeview_data,
        ),
        4,
        0,
    )
    create_action_button(
        button_frame,
        "Update",
        lambda: update_supplier(
            employee_data[0][0],
            invoice_entry.get(),
            contact_entry.get(),
            supplierName_entry.get(),
            description_text.get(1.0, END).strip(),
            treeview_data,
            supplier_treeview,
        ),
        4,
        1,
    )
    create_action_button(
        button_frame,
        "Delete",
        lambda: delete_supplier(invoice_entry.get(), treeview_data),
        4,
        2,
    )
    create_action_button(
        button_frame,
        "Clear",
        lambda: clear_fields(
            invoice_entry,
            supplierName_entry,
            contact_entry,
            description_text,
            True,
        ),
        4,
        3,
    )

    # Right frame
    right_frame = Frame(supplier_frame, bg="#0F0C0C")
    right_frame.place(x=500, y=50, width=500, height=450)

    search_frame = Frame(right_frame, bg="#0F0C0C")
    search_frame.pack(fill=X, pady=10)

    number_entry = create_label_entry_pair(search_frame, "Invoice No.", 0, 0, width=12)

    search_button = create_button(
        search_frame,
        text="Search",
        font=("Arial", 8),
        bg="#AF8F6F",
        command=lambda: search_supplier(invoice_entry.get(), treeview_data),
        width=6,
    )
    search_button.grid(row=0, column=2, padx=10, pady=10)
    show_button = create_button(
        search_frame,
        text="Show All",
        font=("Arial", 8),
        bg="#AF8F6F",
        command=lambda: print("Show All"),
        width=6,
    )
    show_button.grid(row=0, column=3, padx=10, pady=10)

    # Table
    vertical_scrollbar = Scrollbar(right_frame, orient="vertical")
    vertical_scrollbar.pack(side=RIGHT, fill=Y)

    horizontal_scrollbar = Scrollbar(right_frame, orient="horizontal")
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)

    supplier_treeview = Treeview(
        right_frame,
        columns=[str(i) for i in range(1, 6)],
        show="headings",
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    horizontal_scrollbar.config(command=supplier_treeview.xview)
    vertical_scrollbar.config(command=supplier_treeview.yview)

    supplier_treeview.pack(
        fill=BOTH,
        expand=1,
    )

    for i, heading in enumerate(
        ["Invoice ID", "EmpID", "Supplier Name", "Contact", "Description"], start=1
    ):
        supplier_treeview.heading(str(i), text=heading)
        supplier_treeview.column(str(i), width=150)

    supplier_treeview.bind(
        "<ButtonRelease-1>",
        lambda event: select_supplier(
            event,
            invoice_entry,
            supplierName_entry,
            contact_entry,
            description_text,
            supplier_treeview,
        ),
    )

    treeview_data()
