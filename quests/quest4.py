#quests/quest4.py

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from quests.quest import Quest
from tkinter import ttk
from visualization import Visualization

class Quest4(Quest):
    def __init__(self, ui):
        super().__init__(quest_id=4, description="Tune the controller to maintain the water level.", difficulty=4, ui=ui)
        self.desired_level = 0.5  # Desired water level in tank
        self.kp = tk.DoubleVar(value=1.0)  # Proportional gain
        self.ki = tk.DoubleVar(value=0.1)
        self.kd = tk.DoubleVar(value=0.1)
        self.integral_error = 0.0
        self.h1 = [0.0]
        self.water_level = [0.0]  # Initial water level in the controlled tank
        self.time_elapsed = 0.0
        self.simulation_running = False
        self.animation = None
        self.message_label = None
        # Initialize data lists for plotting
        self.times = [0.0]
        self.kv_values = [0.0]
        self.error_values = [0.0]
        self.integral_error_values = [0.0]
        self.derivative_error_values = [0.0]

    def start(self):
        # Clear the content_frame
        for widget in self.ui.content_frame.winfo_children():
            widget.destroy()

        self.quest_frame = tk.Frame(self.ui.content_frame)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.quest_frame, text=self.description, style="Quest.Title.TLabel").pack(pady=20)

        self.control_frame = tk.Frame(self.quest_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Slider for proportional gain
        ttk.Label(self.control_frame, text="Adjust Proportional Gain (Kp):", style="Quest.TLabel").pack(pady=5)
        self.kp_slider = tk.Scale(self.control_frame, from_=0, to=10.0, orient=tk.HORIZONTAL, variable=self.kp, length=200, resolution=0.1)
        self.kp_slider.pack(pady=5)

        ttk.Label(self.control_frame, text="Adjust Integral Gain (Ki):", style="Quest.TLabel").pack(pady=5)
        self.ki_slider = tk.Scale(self.control_frame, from_=0, to=5.0, orient=tk.HORIZONTAL, variable=self.ki, length=200, resolution=0.01)
        self.ki_slider.pack(pady=5)

        ttk.Label(self.control_frame, text="Adjust Derivative Gain (Kd):", style="Quest.TLabel").pack(pady=5)
        self.kd_slider = tk.Scale(self.control_frame, from_=0, to=5.0, orient=tk.HORIZONTAL, variable=self.kd, length=200, resolution=0.01)
        self.kd_slider.pack(pady=5)

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
        desired_level = self.desired_level
        (self.canvas, self.fig, self.tank_ax, self.level_ax,
        self.water_patch, self.level_line, self.desired_level_line, self.control_ax, 
        self.kv_line, self.error_line, self.integral_error_line, self.derivative_error_line) = \
        Visualization.create_single_tank_control_plot(self.plot_frame, desired_level)

    def start_simulation(self):
        if self.simulation_running:
            return  # Prevent multiple simulations at once

        # Reset simulation parameters
        self.h1 = [0.0]  # Water level history for tank
        self.time_elapsed = 0.0
        self.previous_error = 0.0
        self.integral_error = 0.0
        self.previous_h1 = 0.0

        # Reset data lists
        self.times = [0.0]
        self.kv_values = [0.0]
        self.error_values = [0.0]
        self.integral_error_values = [0.0]
        self.derivative_error_values = [0.0]

        # Reset the level lines
        self.level_line.set_data([], [])
        self.kv_line.set_data([], [])
        self.error_line.set_data([], [])
        self.integral_error_line.set_data([], [])
        self.derivative_error_line.set_data([], [])

        # Reset the water level in the tank diagram
        self.water_patch.set_height(0)

        # Reset the axes limits
        self.level_ax.set_xlim(0, 50)
        self.level_ax.set_ylim(0, 1.0)
        self.control_ax.set_xlim(0, 50)
        self.control_ax.set_ylim(auto=True)  # Let matplotlib autoscale the y-axis
        self.simulation_running = True

        # Start the animation
        self.animate()

    def reset_simulation(self):
        # Stop the simulation if it's running
        self.simulation_running = False

        # Reset simulation parameters
        self.h1 = [0.0]  # Water level history for tank
        self.time_elapsed = 0.0
        self.previous_error = 0.0
        self.integral_error = 0.0
        self.previous_h1 = 0.0

        # Reset data lists
        self.times = [0.0]
        self.kv_values = [0.0]
        self.error_values = [0.0]
        self.integral_error_values = [0.0]
        self.derivative_error_values = [0.0]


        # Reset the level lines
        self.level_line.set_data([], [])
        self.kv_line.set_data([], [])
        self.error_line.set_data([], [])
        self.integral_error_line.set_data([], [])
        self.derivative_error_line.set_data([], [])

        # Reset the water level in the tank diagram
        self.water_patch.set_height(0)

        # Reset the axes limits
        self.level_ax.set_xlim(0, 50)
        self.level_ax.set_ylim(0, 1.0)
        self.control_ax.set_xlim(0, 50)
        self.control_ax.set_ylim(auto=True)  # Let matplotlib autoscale the y-axis

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
        dt = 0.1  # Time step
        max_time = 50  # Maximum simulation time
        A = 1.0  # Cross-sectional area of the tank
        Kv_max = 0.5  # Maximum control signal
        desired_level = self.desired_level

        # Get player's proportional, integral, and derivative gains
        Kp = self.kp.get()
        Ki = self.ki.get()
        Kd = self.kd.get()

        # Current water level in tank
        h1 = self.h1[-1]

        # Inflow to tank
        Q_in = 0.1  # Constant inflow

        # Calculate error term
        error = desired_level - h1

        # Calculate derivative term based on error
        if hasattr(self, "previous_error"):
            derivative_error = (error - self.previous_error) / dt
        else:
            derivative_error = 0.0
        self.previous_error = error

        # Update integral error with anti-windup
        if not (h1 >= 1.0 and error > 0):  # Assuming tank height is 1.0 m
            self.integral_error += error * dt
        self.integral_error = max(-10, min(self.integral_error, 10))  # Clamp integral error

        # Feedforward term
        Kv_ff = Q_in / np.sqrt(desired_level)

        # Controller adjusts Kv (PID Control Signal)
        Kv = Kv_ff + Kp * error + Ki * self.integral_error - Kd * derivative_error

        # Limit control signal
        Kv = max(0.0, min(Kv, Kv_max))

        # Outflow from tank
        Q_out = Kv * np.sqrt(max(h1, 0.0))  # Ensure h1 >= 0.0

        # Differential equation
        dh1_dt = (Q_in - Q_out) / A

        # Update water level
        h1_new = h1 + dh1_dt * dt

        # Ensure water level is within bounds
        h1_new = min(max(h1_new, 0.0), 1.0)  # Assuming tank height is 1.0 m

        # Append new water level
        self.h1.append(h1_new)

        # Update time
        self.time_elapsed += dt
        self.times.append(self.time_elapsed)

        # Append controller variables to lists
        self.kv_values.append(Kv)
        self.error_values.append(error)
        self.integral_error_values.append(self.integral_error)
        self.derivative_error_values.append(derivative_error)

        # Update visualization
        self.update_water_tank(h1_new)

        # Update water level plot
        self.level_line.set_data(self.times, self.h1)
        self.level_ax.set_xlim(0, max(10, self.time_elapsed))
        self.level_ax.set_ylim(0, 1.0)

        # Update controller variables plot
        self.kv_line.set_data(self.times, self.kv_values)
        self.error_line.set_data(self.times, self.error_values)
        self.integral_error_line.set_data(self.times, self.integral_error_values)
        self.derivative_error_line.set_data(self.times, self.derivative_error_values)
        self.control_ax.set_xlim(0, max(10, self.time_elapsed))
        # Autoscale y-axis
        self.control_ax.relim()
        self.control_ax.autoscale_view()

        # Redraw canvas
        self.canvas.draw()

        # Continue simulation or check success
        if self.time_elapsed < max_time:
            self.ui.root.after(int(dt * 1000), self.animate)
        else:
            self.simulation_running = False
            self.check_success()

    def update_water_tank(self, h1):
        # Update the water level in the tank diagram
        self.water_patch.set_height(min(h1, 1.0))  # Limit water height to tank height (1.0)
        self.water_patch.set_xy((0.5, 0.0))  # The water level starts from y=0.0

    def check_success(self):
        # Check if the water level stabilized around the desired level
        desired_level = self.desired_level
        levels = np.array(self.h1[-50:])  # Check the last 50 readings
        if np.all(np.abs(levels - desired_level) < 0.05):
            self.display_message("Success! The water level is stable.", success=True)
            self.ui.root.after(2000, self.end_quest)
        else:
            self.display_message("Try adjusting Kp to stabilize the level.", error=True)

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
