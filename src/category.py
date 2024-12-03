from tkinter import *
from tkinter.ttk import Treeview
from src.components.button import create_button

from src.database.categoryDB import (
    add_category,
    create_category_table,
    delete_category,
    show_category,
)


# Utility Functions
def create_label_entry_pair(parent, text, row, column, entry_var=None, width=20):
    """Create a label and an entry widget as a pair."""
    label = Label(parent, text=text, font=("Arial", 12), bg="#0F0C0C", fg="white")
    label.grid(row=row, column=column, padx=20, pady=10, sticky="w")
    entry = Entry(
        parent, font=("Arial", 12), bg="lightgray", textvariable=entry_var, width=width
    )
    entry.grid(row=row, column=column + 1, padx=20, pady=10)
    return entry


def treeview_data():
    category_records = show_category()

    category_treeview.delete(*category_treeview.get_children())
    for record in category_records:
        category_treeview.insert("", "end", values=record)


def clear_fields(id_entry, categoryName_entry, description_text, check=False):
    id_entry.delete(0, END)
    categoryName_entry.delete(0, END)
    description_text.delete(1.0, END)

    if check:
        category_treeview.selection_remove(category_treeview.selection())


def select_category(event, id, name, description, category_treeview):
    index = category_treeview.selection()
    content = category_treeview.item(index, "values")

    id.delete(0, END)
    name.delete(0, END)
    description.delete(1.0, END)

    id.insert(0, content[0])
    name.insert(0, content[1])
    description.insert(1.0, content[2])


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


def category_form(parent, employee_data):
    global logo
    global category_treeview
    create_category_table()

    category_frame = Frame(parent, bg="#0F0C0C", relief=SUNKEN, bd=1)
    category_frame.place(x=0, y=0, width=1020, height=620)

    # Header
    heading_label = Label(
        category_frame,
        text="Manage Category",
        font=("Arial", 16, "bold"),
        bg="#AF8F6F",
        fg="white",
    )
    heading_label.place(x=0, y=0, relwidth=1)

    # Back Button
    back_button = create_button(
        frame=category_frame,
        text="Back",
        command=lambda: category_frame.destroy(),
        font=("Arial", 10),
    )
    back_button.place(x=0, y=0)

    logo = PhotoImage(file="img/product_category.png")
    logo_label = Label(category_frame, image=logo, bg="#0F0C0C")
    logo_label.place(x=30, y=100)

    details_frame = Frame(category_frame, bg="#0F0C0C")
    details_frame.place(x=500, y=60, width=900, height=500)

    id_entry = create_label_entry_pair(details_frame, "ID.", 0, 0)
    categoryName_entry = create_label_entry_pair(details_frame, "Category Name", 1, 0)

    description_label = Label(
        details_frame, text="Address", font=("Arial", 12), bg="#0F0C0C", fg="white"
    )
    description_label.grid(row=3, column=0, padx=20, pady=10, sticky="nw")
    description_text = Text(
        details_frame,
        height=6,
        width=25,
        bd=2,
        background="lightgray",
    )
    description_text.grid(row=3, column=1, padx=20, pady=10)

    # button
    button_frame = Frame(details_frame, bg="#0F0C0C")
    button_frame.grid(row=4, columnspan=2)

    create_action_button(
        button_frame,
        "Add",
        lambda: add_category(
            id_entry.get(),
            categoryName_entry.get(),
            description_text.get(1.0, END),
            treeview_data,
        ),
        4,
        1,
    )
    create_action_button(
        button_frame,
        "Delete",
        lambda: delete_category(id_entry.get(), treeview_data),
        4,
        2,
    )
    create_action_button(
        button_frame,
        "Clear",
        lambda: clear_fields(id_entry, categoryName_entry, description_text, True),
        4,
        3,
    )

    tree_frame = Frame(details_frame, bg="red")
    tree_frame.grid(row=5, columnspan=2)

    # Table
    vertical_scrollbar = Scrollbar(tree_frame, orient="vertical")
    vertical_scrollbar.pack(side=RIGHT, fill=Y)

    horizontal_scrollbar = Scrollbar(tree_frame, orient="horizontal")
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)

    category_treeview = Treeview(
        tree_frame,
        columns=[str(i) for i in range(1, 4)],
        show="headings",
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    horizontal_scrollbar.config(command=category_treeview.xview)
    vertical_scrollbar.config(command=category_treeview.yview)

    category_treeview.pack(
        fill=BOTH,
        expand=1,
    )

    for i, heading in enumerate(["ID", "Name", "Description"], start=1):
        category_treeview.heading(str(i), text=heading)
        category_treeview.column(str(i), width=150)

    category_treeview.bind(
        "<ButtonRelease-1>",
        lambda event: select_category(
            event, id_entry, categoryName_entry, description_text, category_treeview
        ),
    )

    treeview_data()
