from tkinter import *
from tkinter import messagebox
from src.database.employeeDB import login_employee
from src.dashboard import my_dashboard


WINDOW_TITLE = "Dashboard"
WINDOW_SIZE = "1270x720+0+0"
BG_COLOR = "#191919"
TITLE_BG_COLOR = "#0F0E0E"
SIDEBAR_BG_COLOR = "#1D1C1A"
CONTENT_BG_COLOR = "#021526"


# Main application window
window = Tk()
window.title(WINDOW_TITLE)
window.geometry(WINDOW_SIZE)
window.configure(bg=BG_COLOR)
window.resizable(0, 0)


def check_login(email, password):
    if email == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        employee_data = login_employee(email)

        if (
            not employee_data
            or employee_data[0][2] != email
            and employee_data[0][13] != password
        ):
            messagebox.showerror("Error", "Invalid email or password")
        else:
            my_dashboard(window, employee_data)


def login_page():
    login_frame = Frame(window, bg=BG_COLOR)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    email_label = Label(login_frame, text="Email", bg=BG_COLOR, fg="white")
    email_label.grid(row=0, column=0, padx=10, pady=10)

    email_entry = Entry(login_frame, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = Label(login_frame, text="Password", bg=BG_COLOR, fg="white")
    password_label.grid(row=1, column=0, padx=10, pady=10)

    password_entry = Entry(login_frame, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = Button(
        login_frame,
        text="Login",
        bg="green",
        fg="white",
        width=20,
        command=lambda: check_login(email_entry.get(), password_entry.get()),
    )
    login_button.grid(
        row=2,
        column=0,
        columnspan=2,
        padx=10,
        pady=10,
    )


login_page()
# my_dashboard(window, None)


# setup login page using email and password fields and login login button in the center of the window

window.mainloop()
