from tkinter import PhotoImage


ICONS = {}  # Global storage for images


def load_image(path):
    """Load an image and store it globally to prevent garbage collection."""
    if path not in ICONS:
        try:
            ICONS[path] = PhotoImage(file=path)
        except Exception as e:
            print(f"Error loading image '{path}': {e}")
            ICONS[path] = None
    return ICONS[path]
