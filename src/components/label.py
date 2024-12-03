from tkinter import Label


def create_label(
    frame,
    text="",
    font=("Arial", 15),
    bg="#021526",
    fg="white",
    image=None,
    compound=None,
):
    """Reusable function to create a label."""
    return Label(
        frame, text=text, font=font, bg=bg, fg=fg, image=image, compound=compound
    )
