# quests/quest1.py
from quests.quest import Quest
from math import sqrt
from visualization import Visualization
import tkinter as tk
from tkinter import ttk


class Quest1(Quest):
    def __init__(self, ui):
        super().__init__(quest_id=1, description="Calculate the hypotenuse of a right-angled triangle.", difficulty=1, ui=ui)
        self.a_value = tk.DoubleVar(value=3.0)
        self.b_value = tk.DoubleVar(value=4.0)
        self.c_value = tk.StringVar()
        self.a_max_value = 20.00
        self.b_max_value = 20.00
        self.a_min_value = 1.00
        self.b_min_value = 1.00

    def start(self):
        # Destroy any existing widgets in content_frame
        for widget in self.ui.content_frame.winfo_children():
            widget.destroy()

        self.quest_frame = tk.Frame(self.ui.content_frame)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.quest_frame, text=self.description, style="Quest.Title.TLabel").pack(pady=20)

        self.control_frame = tk.Frame(self.quest_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        ttk.Label(self.control_frame, text="Adjust side a:", style="Quest.TLabel").pack(pady=5)
        self.a_slider = tk.Scale(self.control_frame, from_=self.a_min_value, to=self.a_max_value, orient=tk.HORIZONTAL, variable=self.a_value, command=self.update_plot, length=200, resolution=0.1).pack(pady=5)
    
        ttk.Label(self.control_frame, text="Adjust side b:", style="Quest.TLabel").pack(pady=5)
        self.b_slider = tk.Scale(self.control_frame, from_=self.b_min_value, to=self.b_max_value, orient=tk.HORIZONTAL, variable=self.b_value, command=self.update_plot, length=200, resolution=0.1).pack(pady=5)

        ttk.Label(self.control_frame, text="Enter the hypotenuse value:", style="Quest.TLabel").pack(pady=10)
        ttk.Entry(self.control_frame, textvariable=self.c_value).pack(pady=5)

        ttk.Button(self.control_frame, text="Submit Answer", command=self.check_answer, style="Quest.TButton").pack(pady=10)

        # Initialize message_label to None
        self.message_label = None

        self.plot_frame = tk.Frame(self.quest_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas, self.line, self.side_a_label, self.side_b_label = Visualization.create_triangle_plot(self.plot_frame, self.a_value.get(), self.b_value.get(), max(self.a_max_value,self.b_max_value))

    def update_plot(self, event=None):
        Visualization.update_triangle_plot(self.canvas, self.line, self.side_a_label, self.side_b_label, self.a_value.get(), self.b_value.get())

    def check_answer(self):
        try:
            user_c = float(self.c_value.get())
        except ValueError:
            self.display_message(self.quest_frame, "Please enter a valid number.", error=True)
            return

        correct_c = sqrt(self.a_value.get() ** 2 + self.b_value.get() ** 2)
        if abs(user_c - correct_c) < 0.01:
            self.display_message(self.quest_frame, "Correct! Moving to the next quest.", success=True)
            self.ui.root.after(2000, self.end_quest)  # Delay ending the quest
        else:
            self.display_message(self.quest_frame, "Incorrect. Try again.", error=True)

    def end_quest(self):
        """
        Ends the quest, destroys the quest frame, and triggers the completion callback.
        """
        super().end_quest()
