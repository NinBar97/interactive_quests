# ui_utils.py

from tkinter import ttk

def setup_styles():
    """
    Configures all custom styles used in the application.
    """
    style = ttk.Style()
    style.theme_use('default')  # Use a base theme

    # Labels
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))
    style.configure('Error.TLabel', font=('Helvetica', 12), foreground='red')
    style.configure('Quest.TLabel', font=('Helvetica', 12))
    style.configure('Quest.Title.TLabel', font=('Helvetica', 16, 'bold'))

    # Buttons
    style.configure('TButton', font=('Helvetica', 14), padding=5)
    style.configure('Quest.TButton', font=('Helvetica', 14, 'bold'), padding=10)

    # Completion labels
    style.configure('Complete.Title.TLabel', font=('Helvetica', 24, 'bold'))
    style.configure('Complete.TLabel', font=('Helvetica', 16))

    # Other customizations can go here
    # Example: style.configure('YourCustomStyleName', options...)

