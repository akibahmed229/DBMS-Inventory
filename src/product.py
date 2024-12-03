from tkinter import *
from tkinter.ttk import Treeview, Combobox
from src.components.button import create_button

from src.database.categoryDB import show_category
from src.database.supplierDB import show_supplier
from src.database.productDB import (
    create_product_table,
    add_product,
    delete_product,
    search_product,
    show_product,
    update_product,
)


# Utility Functions
def treeview_data():
    product_records = show_product()

    product_treeview.delete(*product_treeview.get_children())
    for record in product_records:
        product_treeview.insert("", "end", values=record)


def showAll_product(search_label, treeview_data):
    treeview_data()

    search_label.set("Search By")


def clear_fields(
    category_label,
    supplier_label,
    name_entry,
    price_entry,
    quantity_entry,
    status_label,
):
    category_label.set("Select")
    supplier_label.set("Select")
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    status_label.set("Select")


def select_product(
    event,
    category_label,
    supplier_label,
    name_entry,
    price_entry,
    quantity_entry,
    status_label,
):
    index = product_treeview.selection()
    content = product_treeview.item(index, "values")

    category_label.set(content[3])
    supplier_label.set(content[4])
    name_entry.delete(0, END)
    name_entry.insert(0, content[5])
    price_entry.delete(0, END)
    price_entry.insert(0, content[6])
    quantity_entry.delete(0, END)
    quantity_entry.insert(0, content[7])
    status_label.set(content[8])


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


def create_label_combobox_pair(parent, text, row, column, values, default="Select"):
    """Create a label and a combobox widget as a pair."""
    label = Label(parent, text=text, font=("Arial", 12), bg="#0F0C0C", fg="white")
    label.grid(row=row, column=column, padx=20, pady=10, sticky="w")

    combobox = Combobox(
        parent, values=values, state="readonly", font=("Arial", 12), width=18
    )
    combobox.set(default)
    combobox.grid(row=row, column=column + 1, padx=20, pady=10)
    return combobox


def extract_id(data, name_to_find):
    for name, value in data:
        if name == name_to_find:
            return value


def product_form(parent, employee_data):
    global product_treeview
    create_product_table()

    product_frame = Frame(parent, bg="#0F0C0C", relief=SUNKEN, bd=1)
    product_frame.place(x=0, y=0, width=1020, height=620)

    # Header
    heading_label = Label(
        product_frame,
        text="Manage Product",
        font=("Arial", 16, "bold"),
        bg="#AF8F6F",
        fg="white",
    )
    heading_label.place(x=0, y=0, relwidth=1)

    # Back Button
    back_button = create_button(
        frame=product_frame,
        text="Back",
        command=lambda: product_frame.destroy(),
        font=("Arial", 10),
    )
    back_button.place(x=0, y=0)

    left_frame = Frame(product_frame, bg="#0F0C0C", bd=2, relief=RIDGE)
    left_frame.place(x=20, y=100)

    category_data = [(item[1], item[0]) for item in show_category()]

    category_label = create_label_combobox_pair(
        left_frame,
        "Category",
        1,
        0,
        [item[0] for item in category_data],
    )

    supplier_data = [
        (item[2].strip(), item[0]) for item in show_supplier(employee_data[0][0])
    ]
    supplier_label = create_label_combobox_pair(
        left_frame, "Supplier", 2, 0, [item[0] for item in supplier_data]
    )
    name_entry = create_label_entry_pair(left_frame, "Name", 3, 0)
    price_entry = create_label_entry_pair(left_frame, "Price", 4, 0)
    quantity_entry = create_label_entry_pair(left_frame, "Quantity", 5, 0)
    status_label = create_label_combobox_pair(
        left_frame, "Status", 6, 0, ["Active", "Inactive"]
    )

    # button
    button_frame = Frame(left_frame, bg="#0F0C0C")
    button_frame.grid(row=7, columnspan=2, pady=20)

    create_action_button(
        button_frame,
        "Add",
        lambda: add_product(
            extract_id(category_data, category_label.get()),
            extract_id(supplier_data, supplier_label.get()),
            category_label.get(),
            supplier_label.get(),
            name_entry.get(),
            price_entry.get(),
            quantity_entry.get(),
            status_label.get(),
            treeview_data,
        ),
        7,
        0,
    )
    create_action_button(
        button_frame,
        "Update",
        lambda: update_product(
            extract_id(category_data, category_label.get()),
            extract_id(supplier_data, supplier_label.get()),
            category_label.get(),
            supplier_label.get(),
            name_entry.get(),
            price_entry.get(),
            quantity_entry.get(),
            status_label.get(),
            treeview_data,
        ),
        7,
        1,
    )
    create_action_button(
        button_frame,
        "Delete",
        lambda: delete_product(
            extract_id(category_data, category_label.get()),
            extract_id(supplier_data, supplier_label.get()),
            treeview_data,
        ),
        7,
        2,
    )
    create_action_button(
        button_frame,
        "Clear",
        lambda: clear_fields(
            category_label,
            supplier_label,
            name_entry,
            price_entry,
            quantity_entry,
            status_label,
        ),
        7,
        3,
    )

    search_frame = LabelFrame(
        product_frame,
        text="Search Product",
        bg="#0F0C0C",
        fg="white",
        font=("Arial", 12, "bold"),
    )
    search_frame.place(x=450, y=90)

    search_label = Combobox(
        search_frame,
        values=["Category Name", "Supplier Name", "Name", "Status"],
        state="readonly",
        font=("Arial", 10),
        width=16,
    )
    search_label.set("Search By")
    search_label.grid(row=0, column=0, padx=20, pady=10)
    search_entry = Entry(search_frame, font=("Arial", 10), bg="lightgray", width=16)
    search_entry.grid(row=0, column=1, padx=20, pady=10)
    search_button = create_button(
        search_frame,
        text="Search",
        font=("Arial", 8),
        bg="#AF8F6F",
        width=6,
        command=lambda: search_product(
            search_label.get(), search_entry.get(), product_treeview
        ),
    )
    search_button.grid(row=0, column=2, padx=10, pady=10)
    show_all_button = create_button(
        search_frame,
        text="Show All",
        font=("Arial", 8),
        bg="#AF8F6F",
        width=6,
        command=lambda: showAll_product(search_label, treeview_data),
    )
    show_all_button.grid(row=0, column=3, padx=10, pady=10)

    # Treeview
    tree_frame = Frame(product_frame, bg="#0F0C0C")
    tree_frame.place(x=450, y=180, width=530, height=400)

    # Table
    vertical_scrollbar = Scrollbar(tree_frame, orient="vertical")
    vertical_scrollbar.pack(side=RIGHT, fill=Y)

    horizontal_scrollbar = Scrollbar(tree_frame, orient="horizontal")
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)

    product_treeview = Treeview(
        tree_frame,
        columns=[str(i) for i in range(1, 10)],
        show="headings",
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    horizontal_scrollbar.config(command=product_treeview.xview)
    vertical_scrollbar.config(command=product_treeview.yview)

    product_treeview.pack(
        fill=BOTH,
        expand=1,
    )

    for i, heading in enumerate(
        [
            "ID",
            "C_ID",
            "S_ID",
            "Category",
            "Supplier",
            "Name",
            "Price",
            "Quantity",
            "Status",
        ],
        start=1,
    ):
        product_treeview.heading(str(i), text=heading)
        product_treeview.column(str(i), width=100)

    product_treeview.bind(
        "<ButtonRelease-1>",
        lambda event: select_product(
            event,
            category_label,
            supplier_label,
            name_entry,
            price_entry,
            quantity_entry,
            status_label,
        ),
    )

    treeview_data()
