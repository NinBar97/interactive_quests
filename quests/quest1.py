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
        self.c_value = tk.DoubleVar()
        self.a_max_value = 20.00
        self.b_max_value = 20.00
        self.a_min_value = 1.00
        self.b_min_value = 1.00

        self.style = ttk.Style()
        self.style.configure('Quest.TLabel', font=('Helvetica', 12))
        self.style.configure('Quest.TButton', font=('Helvetica', 14))
        self.style.configure('Quest.Title.TLabel', font=('Helvetica', 18))
        self.style.configure('Error.TLabel', foreground='red')

        # Initialize plot elements to None
        self.canvas = None
        self.line = None
        self.title = None

    def start(self):
        # Hide main menu
        self.ui.main_menu_frame.pack_forget()

        # Create quest frame
        self.quest_frame = tk.Frame(self.ui.root)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)

        # Display description
        ttk.Label(self.quest_frame, text=self.description, style='Quest.Title.TLabel').pack(pady=20)

        self.controls_frame = tk.Frame(self.quest_frame)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Sliders for sides a and b
        ttk.Label(self.controls_frame, text="Adjust side a:", style='Quest.TLabel').pack(pady=5)
        self.a_slider = tk.Scale(self.controls_frame, from_=self.a_min_value, to=self.a_max_value, orient=tk.HORIZONTAL, variable=self.a_value, command=self.update_plot, length=200, resolution=0.1)
        self.a_slider.pack(pady=5)

        ttk.Label(self.controls_frame, text="Adjust side b:", style='Quest.TLabel').pack(pady=5)
        self.b_slider = tk.Scale(self.controls_frame, from_=self.b_min_value, to=self.b_max_value, orient=tk.HORIZONTAL, variable=self.b_value, command=self.update_plot, length=200, resolution=0.1)
        self.b_slider.pack(pady=5)

        # Entry for the hypotenuse value
        ttk.Label(self.controls_frame, text="Enter the hypotenuse value:", style='Quest.TLabel').pack(pady=10)
        self.hypot_entry = tk.Entry(self.controls_frame, textvariable=self.c_value)
        self.hypot_entry.pack(pady=5)

        ttk.Button(self.controls_frame, text="Submit Answer", command=self.submit_answer, style='Quest.TButton').pack(pady=10)

        # Initialize message_label to None
        self.message_label = None

        # Plot area
        self.plot_frame = tk.Frame(self.quest_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initial plot
        self.create_plot()

    def submit_answer(self):
        if self.hypot_entry.get():
            #self.answer_frame.destroy()
            self.check_answer()
        else:
            ttk.Label(self.name_frame, text="Please enter a value.", style='Error.TLabel').pack()

    def check_answer(self):
        # Check if given answer is correct
        a = self.a_value.get()
        b = self.b_value.get()
        c = sqrt(a**2 + b**2)

        try:
            user_answer = float(self.hypot_entry.get())
        except ValueError:
            # User did not enter a valid number
            self.display_message("Please enter a valid number.", error=True)
            return

        # Use a tolerance for comparison
        if abs(user_answer - c) < 0.01:
            # Answer is correct!
            self.display_message("Correct answer!", success=True)
            # Inform the GameEngine that the quest is completed
            if self.completion_callback:
                self.completion_callback(self.quest_id, self.difficulty)
            # Hide quest frame and show main menu after a delay
            self.ui.root.after(2000, self.end_quest)
        else:
            # Wrong answer!
            self.display_message("Wrong answer. Try again.", error=True)

    def display_message(self, message, error=False, success=False):
        # Remove existing message label if any
        if self.message_label:
            self.message_label.destroy()
        color = 'red' if error else 'green' if success else 'black'
        self.message_label = ttk.Label(self.controls_frame, text=message, style='Quest.TLabel')
        self.message_label.configure(foreground=color)
        self.message_label.pack(pady=5)

    def create_plot(self):
        a = self.a_value.get()
        b = self.b_value.get()
        a_max = self.a_max_value
        b_max = self.b_max_value

        # Create the initial plot and store references
        self.canvas, self.line, self.title = Visualization.create_triangle_plot(self.plot_frame, a, b, a_max, b_max)

    def update_plot(self, event=None):
        a = self.a_value.get()
        b = self.b_value.get()
        c = sqrt(a ** 2 + b ** 2)
        a_max = self.a_max_value
        b_max = self.b_max_value

        # Update the line data
        x_data = [0, a, 0, 0]
        y_data = [0, 0, b, 0]
        self.line.set_data(x_data, y_data)

        # Update the title
        self.title.set_text(f"Right-Angled Triangle\nHypotenuse: {c:.2f}")

        # Redraw the canvas
        self.canvas.draw_idle()

    def end_quest(self):
        self.quest_frame.pack_forget()
        self.ui.create_main_menu()
