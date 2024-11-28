# user_interface.py
import tkinter as tk
from tkinter import ttk
from ui_utils import setup_styles  # Centralized styling utility


class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Math Quest Game")
        self.root.geometry("800x600")

        # Initialize variables with self.root as the master
        self.player_name = tk.StringVar(self.root)
        self.player_points = tk.IntVar(self.root, value=0)
        self.start_quest_journey_callback = None  # Will be set by GameEngine
        self.game_engine = None  # Will be set by GameEngine

        self.error_label = None  # Initialize error_label here

        setup_styles()  # Apply styles after root is created

        # Create a content frame to hold all other frames
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.get_player_name()

    def get_player_name(self):
        # Destroy any existing widgets in content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.name_frame = tk.Frame(self.content_frame)
        self.name_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.name_frame, text="Math Quest Game", style='Title.TLabel').pack(pady=20)
        ttk.Label(self.name_frame, text="Enter your name:", style='TLabel').pack(pady=10)
        self.name_entry = ttk.Entry(self.name_frame, textvariable=self.player_name)
        self.name_entry.pack(pady=5)
        ttk.Button(self.name_frame, text="Submit", command=self.submit_name).pack(pady=10)

    def submit_name(self):
        if self.player_name.get().strip():
            if self.error_label:
                self.error_label.destroy()  # Remove existing error message
            self.name_frame.destroy()
            self.create_main_menu()
        else:
            if not self.error_label:
                self.error_label = ttk.Label(self.name_frame, text="Please enter a name.", style='Error.TLabel')
                self.error_label.pack()
            else:
                # If the error label already exists, do nothing or update if needed
                pass

    def create_main_menu(self):
        # Destroy any existing widgets in content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.main_menu_frame = tk.Frame(self.content_frame)
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)

        # Scoreboard
        scoreboard = tk.Frame(self.main_menu_frame)
        scoreboard.pack(side=tk.TOP, fill=tk.X, pady=10)
        ttk.Label(scoreboard, text="Player:").pack(side=tk.LEFT, pady=5)
        ttk.Label(scoreboard, textvariable=self.player_name).pack(side=tk.LEFT)
        ttk.Label(scoreboard, text=" | Points:").pack(side=tk.LEFT, pady=5)
        ttk.Label(scoreboard, textvariable=self.player_points).pack(side=tk.LEFT)

        # Main menu buttons
        menu_frame = tk.Frame(self.main_menu_frame)
        menu_frame.pack(expand=True)

        total_quests = len(self.game_engine.quests)
        current_quest = self.game_engine.current_quest_index + 1
        button_text = (
            "Start The Quest Journey" if self.game_engine.current_quest_index == 0 else
            f"Continue to Quest {current_quest}" if current_quest <= total_quests else
            "All Quests Completed")

        ttk.Button(menu_frame, text=button_text, command=self.start_quest_journey).pack(pady=10)
        ttk.Button(menu_frame, text="View Status", command=self.view_status).pack(pady=10)
        ttk.Button(menu_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def start_quest_journey(self):
        if self.start_quest_journey_callback:
            # Hide the main menu frame
            self.main_menu_frame.pack_forget()
            self.start_quest_journey_callback()

    def show_completion_message(self):
        # Destroy any existing widgets in content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        completion_frame = tk.Frame(self.content_frame)
        completion_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(completion_frame, text="Congratulations!", style='Complete.Title.TLabel').pack(pady=20)
        ttk.Label(completion_frame, text="You have completed all quests.", style='Complete.TLabel').pack(pady=10)
        ttk.Button(completion_frame, text="View Status", command=self.view_status).pack(pady=10)
        ttk.Button(completion_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def view_status(self):
        # Destroy any existing widgets in content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.status_frame = tk.Frame(self.content_frame)
        self.status_frame.pack(fill=tk.BOTH, expand=True)

        status = f"Player: {self.player_name.get()}\nPoints: {self.player_points.get()}"
        tk.Label(self.status_frame, text=status, font=("Helvetica", 16)).pack(pady=20)

        ttk.Button(self.status_frame, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def back_to_menu(self):
        self.create_main_menu()

    def run(self):
        self.root.mainloop()
