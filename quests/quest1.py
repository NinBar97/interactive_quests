# quests/quest1.py

from quests.quest import Quest
import tkinter as tk
from tkinter import ttk
from math import sqrt
from visualization import Visualization

class Quest1(Quest):
    def __init__(self, ui):
        super().__init__(quest_id=1, description="Calculate the hypotenuse of a right-angled triangle.", difficulty=1)
        self.ui = ui
        self.completion_callback = None  # Will be set by GameEngine
        self.a_value = tk.DoubleVar(value=3.0) # Starting value for a
        self.b_value = tk.DoubleVar(value=4.0) # Starting value for b

        self.style = ttk.Style()
        self.style.configure('Quest.TLabel', font=('Helvetica', 12))
        self.style.configure('Quest.TButton', font=('Helvetica', 14))

    def start(self):
        # Hide main menu
        self.ui.main_menu_frame.pack_forget()

        # Create quest frame
        self.quest_frame = tk.Frame(self.ui.root)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)

        # Display description
        tk.Label(self.quest_frame, text=self.description, font=("Helvetica", 16)).pack(pady=10)

        controls_frame = tk.Frame(self.quest_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Sliders for sides a and b
        ttk.Label(controls_frame, text="Adjust side a:", style='Quest.TLabel').pack(pady=5)
        self.a_slider = tk.Scale(controls_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.a_value, command=self.update_plot, length=200, resolution=0.1)
        self.a_slider.pack(pady=5)

        ttk.Label(controls_frame, text="Adjust side b:", style='Quest.TLabel').pack(pady=5)
        self.b_slider = tk.Scale(controls_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.b_value, command=self.update_plot, length=200, resolution=0.1)
        self.b_slider.pack(pady=5)

        # Plot area
        self.plot_frame = tk.Frame(self.quest_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initial plot
        self.plot_widget = None
        self.update_plot()

        # Complete Quest Button
        ttk.Button(self.quest_frame, text="Complete Quest", command=self.complete_quest, style='Quest.TButton').pack(pady=10)

    def update_plot(self, event=None):
        a = self.a_value.get()
        b = self.b_value.get()

        # Remove existing plot if any
        if self.plot_widget:
            self.plot_widget.get_tk_widget().destroy()

        # Create new plot
        self.plot_widget = Visualization.plot_triangle(self.plot_frame, a, b)

    def complete_quest(self):
        # Calculate hypotenuse
        a = self.a_value.get()
        b = self.b_value.get()
        c = sqrt(a**2 + b**2)

        # Display result in the quest frame
        result_text = f"The hypotenuse is: {c:.2f}"
        if hasattr(self, 'result_label'):
            self.result_label.config(text=result_text)
        else:
            self.result_label = tk.Label(self.quest_frame, text=result_text, font=("Helvetica", 14), fg='green')
            self.result_label.pack(pady=5)

        # Inform the GameEngine that the quest is completed
        if self.completion_callback:
            self.completion_callback(self.quest_id, self.difficulty)

        # Hide quest frame and show main menu after a delay
        self.ui.root.after(2000, self.end_quest)

    def end_quest(self):
        self.quest_frame.pack_forget()
        self.ui.create_main_menu()
