from tkinter import LEFT, Button


def create_button(
    frame, text, command, image=None, font=("Arial", 12), bg="#1D1C1A", **kwargs
):
    return Button(
        frame,
        text=text,
        image=image,
        compound=LEFT,
        command=command,
        font=font,
        bg=bg,
        fg="white",
        anchor="w",
        padx=20,
        bd=0,
        cursor="hand2",
        activebackground="#493B3B",
        activeforeground="white",
        **kwargs,
    )
