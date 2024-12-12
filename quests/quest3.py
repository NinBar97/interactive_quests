#quests/quest3.py

import numpy as np
import random
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from quests.quest import Quest
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from visualization import Visualization

class Quest3(Quest):
    def __init__(self, ui):
        super().__init__(quest_id=3, description="Calculate the correct launch angle to hit the target.", difficulty=3, ui=ui)
        self.initial_speed = tk.DoubleVar(value=50.0)  # Initial speed in m/s
        self.launch_angle = tk.StringVar()  # Player's input for launch angle
        self.target_distance = tk.DoubleVar(value=random.uniform(100.0, 300.0))  # Distance to the target in meters
        self.gravity = 9.8  # Acceleration due to gravity in m/s^2

        # Variables for animation
        self.animation_running = False
        self.animation_index = 0
        self.x_coords = np.array([])
        self.y_coords = np.array([])

    def start(self):
        # Clear the content_frame
        for widget in self.ui.content_frame.winfo_children():
            widget.destroy()

        self.quest_frame = tk.Frame(self.ui.content_frame)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.quest_frame, text=self.description, style="Quest.Title.TLabel").pack(pady=20)

        self.control_frame = tk.Frame(self.quest_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Slider for initial speed
        ttk.Label(self.control_frame, text="Adjust initial speed (m/s):", style="Quest.TLabel").pack(pady=5)
        self.speed_slider = tk.Scale(self.control_frame, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.initial_speed, length=200, resolution=1)
        self.speed_slider.pack(pady=5)

        # Entry for launch angle
        ttk.Label(self.control_frame, text="Enter the launch angle (degrees):", style="Quest.TLabel").pack(pady=10)
        self.angle_entry = ttk.Entry(self.control_frame, textvariable=self.launch_angle)
        self.angle_entry.pack(pady=5)

        # Target distance display
        ttk.Label(self.control_frame, text=f"Target Distance: {self.target_distance.get():.1f} meters", style="Quest.TLabel").pack(pady=10)

        ttk.Button(self.control_frame, text="Fire Projectile", command=self.fire_projectile, style="Quest.TButton").pack(pady=10)

        # Add Skip button
        ttk.Button(self.control_frame, text="Skip Quest", command=self.skip_quest, style="Quest.TButton").pack(pady=10)

        # Initialize message_label to None
        self.message_label = None

        # Plot area
        self.plot_frame = tk.Frame(self.quest_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initial plot
        self.create_plot()

    def create_plot(self):
        self.canvas, self.ax, self.projectile_line, self.target_plot = Visualization.create_projectile_plot(
            self.plot_frame, self.target_distance.get(), self.initial_speed.get(), self.gravity)

    def fire_projectile(self):
        if self.animation_running:
            return  # Prevent firing multiple times at once

        try:
            angle_deg = float(self.launch_angle.get())
        except ValueError:
            self.display_message("Please enter a valid angle.", error=True)
            return

        angle_rad = np.radians(angle_deg)
        v = self.initial_speed.get()
        g = self.gravity

        # Time of flight
        t_flight = (2 * v * np.sin(angle_rad)) / g

        # Time intervals
        t = np.linspace(0, t_flight, num=200)

        # Projectile motion equations
        self.x_coords = v * np.cos(angle_rad) * t
        self.y_coords = v * np.sin(angle_rad) * t - 0.5 * g * t ** 2

        # Update the plot
        self.projectile_line, self.target_plot = Visualization.update_projectile_plot(
            self.ax, self.target_distance.get(), self.initial_speed.get(), self.gravity, self.x_coords, self.y_coords)

        self.canvas.draw()

        # Start the animation
        self.animation_index = 0
        self.animation_running = True
        self.animate_projectile()

    def animate_projectile(self):
        if self.animation_index < len(self.x_coords) and self.y_coords[self.animation_index] >= 0:
            x = self.x_coords[:self.animation_index + 1]
            y = self.y_coords[:self.animation_index + 1]

            # Update the projectile line data
            self.projectile_line.set_data(x, y)

            self.canvas.draw()

            self.animation_index += 1
            # Schedule the next frame
            self.ui.root.after(20, self.animate_projectile)
        else:
            self.animation_running = False
            # Animation is complete; call check_hit()
            self.check_hit()
    
    def check_hit(self):
        v = self.initial_speed.get()
        angle_deg = float(self.launch_angle.get())
        angle_rad = np.radians(angle_deg)
        g = self.gravity
        t_flight = (2 * v * np.sin(angle_rad)) / g
        max_distance = v * np.cos(angle_rad) * t_flight

        if abs(max_distance - self.target_distance.get()) < 5.0:
            self.display_message("Hit! You've successfully hit the target!", success=True)
            # Proceed to end the quest after a short delay
            self.ui.root.after(2000, self.end_quest)
        else:
            self.display_message("Missed! Try adjusting your angle or speed.", error=True)

    def display_message(self, message, error=False, success=False):
        # Remove existing message label if any
        if self.message_label:
            self.message_label.destroy()
        color = 'red' if error else 'green' if success else 'black'
        self.message_label = ttk.Label(self.control_frame, text=message, style='Quest.TLabel')
        self.message_label.configure(foreground=color)
        self.message_label.pack(pady=5)

    def skip_quest(self):
        self.ui.game_engine.skip_current_quest()

    def end_quest(self):
        # Do not destroy the quest_frame here
        super().end_quest()
