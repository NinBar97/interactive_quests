# user_interface.py

import tkinter as tk
from tkinter import ttk


class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Math Quest Game")
        self.root.geometry("800x600")
        self.player_name = tk.StringVar()
        self.player_points = tk.IntVar(value=0)
        self.start_quest_journey_callback = None  # Will be set by GameEngine
        
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TButton', font=('Helvetica', 14))
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('Title.TLabel', font=('Helvetica', 24))
        self.style.configure('Error.TLabel', foreground='red')

        self.get_player_name()

    def get_player_name(self):
        # Create a frame for the name entry
        self.name_frame = tk.Frame(self.root)
        self.name_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = ttk.Label(self.name_frame, text="Math Quest Game", style='Title.TLabel')
        title_label.pack(pady=20)

        ttk.Label(self.name_frame, text="Enter your name: ", style='TLabel').pack(pady=10)
        self.name_entry = tk.Entry(self.name_frame, textvariable=self.player_name)
        self.name_entry.pack(pady=5)

        ttk.Button(self.name_frame, text="Submit", command=self.submit_name).pack(pady=10)

    def submit_name(self):
        if self.player_name.get():
            self.name_frame.destroy()
            self.create_main_menu()
        else:
            ttk.Label(self.name_frame, text="Please enter a name.", style='Error.TLabel').pack()

    def create_main_menu(self):
        if not self.player_name.get():
            return
        # Create a frame for the main menu
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Scoreboard at the top
        scoreboard_frame = tk.Frame(self.main_menu_frame)
        scoreboard_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        ttk.Label(scoreboard_frame, text="Player:").pack(side=tk.LEFT, pady=5)
        ttk.Label(scoreboard_frame, textvariable=self.player_name).pack(side=tk.LEFT)
        ttk.Label(scoreboard_frame, text=" | Points:").pack(side=tk.LEFT, pady=5)
        ttk.Label(scoreboard_frame, textvariable=self.player_points).pack(side=tk.LEFT)

        # Main menu buttons
        menu_frame = tk.Frame(self.main_menu_frame)
        menu_frame.pack(expand=True)

        # Center the buttons vertically and horizontally
        button_style = {"width": 20}  # Removed "font" key
        ttk.Button(menu_frame, text="Start The Quest Journey", command=self.start_quest_journey, **button_style).pack(pady=10)
        ttk.Button(menu_frame, text="View Status", command=self.view_status, **button_style).pack(pady=10)
        ttk.Button(menu_frame, text="Exit", command=self.root.quit, **button_style).pack(pady=10)

    def start_quest_journey(self):
        # This method will be connected to the GameEngine
        if self.start_quest_journey_callback:
            self.start_quest_journey_callback()
        else:
            print("start_quest_journey_callback is not set.")

    def view_status(self):
        # Hide main menu frame
        self.main_menu_frame.pack_forget()

        # Create status frame
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(fill=tk.BOTH, expand=True)

        status = f"Player: {self.player_name.get()}\nPoints: {self.player_points.get()}"
        tk.Label(self.status_frame, text=status, font=("Helvetica", 16)).pack(pady=20)

        ttk.Button(self.status_frame, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def back_to_menu(self):
        # Hide status frame
        self.status_frame.pack_forget()
        # Show main menu
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

    def run(self):
        # self.get_player_name()
        self.root.mainloop()
