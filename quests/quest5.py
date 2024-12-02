# quests/quest5.py

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from quests.quest import Quest
from tkinter import ttk
from visualization import Visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Quest5(Quest):
    def __init__(self, ui):
        super().__init__(quest_id=5, description="Explore the mass-spring-damper system.", difficulty=5, ui=ui)
        self.mass = tk.DoubleVar(value=1.0)      # Mass (m)
        self.spring_const = tk.DoubleVar(value=1.0)  # Spring constant (K_s)
        self.damping_coeff = tk.DoubleVar(value=0.1)  # Damping coefficient (K_d)
        self.initial_displacement = tk.DoubleVar(value=1.0)  # Initial displacement
        self.time_elapsed = 0.0
        self.simulation_running = False
        self.animation = None
        self.message_label = None

        # Initialize data lists for plotting
        self.times = [0.0]
        self.positions = [self.initial_displacement.get()]
        self.velocities = [0.0]  # Initial velocity is zero

    def start(self):
        # Clear the content_frame
        for widget in self.ui.content_frame.winfo_children():
            widget.destroy()

        self.quest_frame = tk.Frame(self.ui.content_frame)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.quest_frame, text=self.description, style="Quest.Title.TLabel").pack(pady=20)

        self.control_frame = tk.Frame(self.quest_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Sliders for mass, spring constant, damping coefficient, and initial displacement
        ttk.Label(self.control_frame, text="Adjust Mass (m):", style="Quest.TLabel").pack(pady=5)
        self.mass_slider = tk.Scale(self.control_frame, from_=0.1, to=10.0, orient=tk.HORIZONTAL, variable=self.mass, length=200, resolution=0.1)
        self.mass_slider.pack(pady=5)

        ttk.Label(self.control_frame, text="Adjust Spring Constant (K_s):", style="Quest.TLabel").pack(pady=5)
        self.spring_slider = tk.Scale(self.control_frame, from_=0.1, to=10.0, orient=tk.HORIZONTAL, variable=self.spring_const, length=200, resolution=0.1)
        self.spring_slider.pack(pady=5)

        ttk.Label(self.control_frame, text="Adjust Damping Coefficient (K_d):", style="Quest.TLabel").pack(pady=5)
        self.damping_slider = tk.Scale(self.control_frame, from_=0.0, to=5.0, orient=tk.HORIZONTAL, variable=self.damping_coeff, length=200, resolution=0.1)
        self.damping_slider.pack(pady=5)

        ttk.Label(self.control_frame, text="Initial Displacement (x0):", style="Quest.TLabel").pack(pady=5)
        self.displacement_slider = tk.Scale(self.control_frame, from_=-5.0, to=5.0, orient=tk.HORIZONTAL, variable=self.initial_displacement, length=200, resolution=0.1)
        self.displacement_slider.pack(pady=5)

        ttk.Button(self.control_frame, text="Start Simulation", command=self.start_simulation, style="Quest.TButton").pack(pady=10)
        ttk.Button(self.control_frame, text="Reset Simulation", command=self.reset_simulation, style="Quest.TButton").pack(pady=10)
        ttk.Button(self.control_frame, text="Skip Quest", command=self.skip_quest, style="Quest.TButton").pack(pady=10)

        # Message Label
        self.message_label = None

        # Plot area
        self.plot_frame = tk.Frame(self.quest_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize the plot
        self.create_plot()

    def create_plot(self):
        self.canvas, self.fig, self.ax_position, self.line_position = Visualization.create_mass_spring_damper_plot(self.plot_frame)

    def start_simulation(self):
        if self.simulation_running:
            return  # Prevent multiple simulations at once

        # Reset simulation parameters
        self.time_elapsed = 0.0
        self.times = [0.0]
        self.positions = [self.initial_displacement.get()]
        self.velocities = [0.0]  # Initial velocity is zero

        # Reset the plot
        self.line_position.set_data([], [])
        self.ax_position.set_xlim(0, 10)
        self.ax_position.set_ylim(-10, 10)
        self.simulation_running = True

        # Start the animation
        self.animate()

    def reset_simulation(self):
        # Stop the simulation if it's running
        self.simulation_running = False

        # Reset simulation parameters
        self.time_elapsed = 0.0
        self.times = [0.0]
        self.positions = [self.initial_displacement.get()]
        self.velocities = [0.0]

        # Reset the plot
        self.line_position.set_data([], [])
        self.ax_position.set_xlim(0, 10)
        self.ax_position.set_ylim(-10, 10)

        # Remove any existing message
        if self.message_label:
            self.message_label.destroy()
            self.message_label = None

        # Redraw the canvas to reflect the reset state
        self.canvas.draw()

    def animate(self):
        if not self.simulation_running:
            return

        # Simulation parameters
        dt = 0.01  # Time step
        max_time = 10.0  # Maximum simulation time

        # Retrieve parameters from sliders
        m = self.mass.get()
        K_s = self.spring_const.get()
        K_d = self.damping_coeff.get()

        # Current state
        t = self.times[-1]
        x = self.positions[-1]
        v = self.velocities[-1]

        # Differential equations
        # Using the equation: m * a + K_d * v + K_s * x = 0
        # Acceleration: a = (-K_d * v - K_s * x) / m
        a = (-K_d * v - K_s * x) / m

        # Update velocity and position using Euler's method
        v_new = v + a * dt
        x_new = x + v_new * dt

        # Update time
        t_new = t + dt

        # Append new values
        self.times.append(t_new)
        self.positions.append(x_new)
        self.velocities.append(v_new)

        # Update plot
        self.line_position.set_data(self.times, self.positions)
        self.ax_position.set_xlim(0, max(10, t_new))
        self.ax_position.set_ylim(min(self.positions) - 1, max(self.positions) + 1)

        # Redraw canvas
        self.canvas.draw()

        # Continue simulation or stop
        if t_new < max_time:
            self.ui.root.after(int(dt * 1000), self.animate)
        else:
            self.simulation_running = False
            self.check_success()

    def check_success(self):
        # Determine if the system is critically damped
        m = self.mass.get()
        K_s = self.spring_const.get()
        K_d = self.damping_coeff.get()
        critical_damping = 2 * np.sqrt(m * K_s)
        if abs(K_d - critical_damping) < 0.1:
            self.display_message("Success! You've achieved critical damping.", success=True)
            self.ui.root.after(2000, self.end_quest)
        else:
            self.display_message("Try adjusting K_d to achieve critical damping.", error=True)

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
