from tkinter import *
from src.category import category_form
from src.employee import employee_form
from src.supplier import supplier_form
from src.product import product_form
from src.components.image import load_image
from src.components.label import create_label
from src.components.button import create_button

from src.database.dashboardDB import get_total_count


# Constants for global settings
WINDOW_TITLE = "Dashboard"
WINDOW_SIZE = "1270x720+0+0"
BG_COLOR = "#191919"
TITLE_BG_COLOR = "#0F0E0E"
SIDEBAR_BG_COLOR = "#1D1C1A"
CONTENT_BG_COLOR = "#021526"

# Paths to resources
IMG_PATHS = {
    "logo": "./img/logo.png",
    "inventory": "./img/inventory.png",
    "employee": "./img/employee.png",
    "supplier": "./img/supplier.png",
    "category": "./img/category.png",
    "product": "./img/product.png",
    "sales": "./img/sales.png",
    "exit": "./img/exit.png",
    "total_emp": "./img/total_emp.png",
    "total_sup": "./img/total_sup.png",
    "total_cat": "./img/total_cat.png",
    "total_prod": "./img/total_prod.png",
    "total_sales": "./img/total_sales.png",
}


def setup_sidebar(parent, employee_data):
    """Create the sidebar."""
    sidebar = Frame(parent, bg=SIDEBAR_BG_COLOR, width=300)
    sidebar.grid_propagate(False)

    # Sidebar logo
    logo_img = load_image(IMG_PATHS["logo"])
    create_label(sidebar, image=logo_img).pack()

    # Sidebar menu
    menu_label = create_label(sidebar, text="Menu", font=("Arial", 15), bg="#493B3B")
    menu_label.pack(fill=X, pady=10)

    menu_items = [
        (
            "Employee",
            load_image(IMG_PATHS["employee"]),
            lambda: employee_form(right_frame, employee_data),
        ),
        (
            "Supplier",
            load_image(IMG_PATHS["supplier"]),
            lambda: supplier_form(right_frame, employee_data),
        ),
        (
            "Category",
            load_image(IMG_PATHS["category"]),
            lambda: category_form(right_frame, employee_data),
        ),
        (
            "Product",
            load_image(IMG_PATHS["product"]),
            lambda: product_form(right_frame, employee_data),
        ),
        ("Sales", load_image(IMG_PATHS["sales"]), None),
        ("Exit", load_image(IMG_PATHS["exit"]), parent.quit),
    ]

    for text, img_path, command in menu_items:
        create_button(sidebar, text, command, image=img_path).pack(fill=X)

    return sidebar


def create_summary_frame(parent, x, y, title, icon_path, count):
    frame = Frame(parent, bg=CONTENT_BG_COLOR, relief=RIDGE, bd=2)
    frame.place(x=x, y=y, width=350, height=200)

    icon = load_image(icon_path)
    if icon:
        create_label(frame, image=icon).pack(pady=10)
    else:
        print(f"Icon missing for {title} at {icon_path}")

    create_label(frame, text=title, font=("Arial", 15)).pack()
    create_label(frame, text=str(count), font=("Arial", 20, "bold")).pack()

    return frame


def my_dashboard(window, employee_data):
    global right_frame
    total_emp, total_sup, total_cat, total_prod = get_total_count()

    # Dashboard Title
    title_img = load_image(IMG_PATHS["inventory"])
    title_label = create_label(
        window,
        text=" Inventory Management System",
        font=("Arial", 30, "bold"),
        bg=TITLE_BG_COLOR,
        fg="white",
        image=title_img,
        compound=LEFT,
    )
    title_label.place(x=0, y=0, relwidth=1)

    logout_button = create_button(
        window, "Logout", window.quit, font=("Arial", 15), bg=TITLE_BG_COLOR
    ).place(x=1150, y=10)

    # Subtitle
    create_label(
        window,
        text="Welcome Admin\t\t Date: 24-11-2024",
        font=("Arial", 12),
        bg="#322C2B",
    ).place(x=0, y=70, relwidth=1)

    # Sidebar
    sidebar = setup_sidebar(window, employee_data)
    sidebar.place(x=0, y=100, width=250)

    # Main content area
    right_frame = Frame(window, bg=TITLE_BG_COLOR)
    right_frame.place(x=250, y=100, relwidth=1, relheight=1)

    # Dashboard Summary Sections
    create_summary_frame(
        right_frame, 90, 20, "Total Employee", IMG_PATHS["total_emp"], total_emp
    )
    create_summary_frame(
        right_frame, 450, 20, "Total Supplier", IMG_PATHS["total_sup"], total_sup
    )
    create_summary_frame(
        right_frame, 90, 230, "Total Category", IMG_PATHS["total_cat"], total_cat
    )
    create_summary_frame(
        right_frame, 450, 230, "Total Product", IMG_PATHS["total_prod"], total_prod
    )

    # Sales Section
    sales_frame = Frame(right_frame, bg=CONTENT_BG_COLOR, relief=RIDGE, bd=2)
    sales_frame.place(x=90, y=450, width=710, height=150)
    sales_icon = load_image(IMG_PATHS["total_sales"])
    create_label(sales_frame, image=sales_icon).pack(pady=10)
    create_label(sales_frame, text="Total Sales", font=("Arial", 15)).pack()
    create_label(sales_frame, text="50", font=("Arial", 20, "bold")).pack()
