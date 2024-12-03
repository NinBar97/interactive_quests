# quests/quest6.py

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from quests.quest import Quest
from tkinter import ttk
from visualization import Visualization

class Quest6(Quest):
    def __init__(self, ui):
        super().__init__(quest_id=6, description="Balance the inverted pendulum by tuning the controller.", difficulty=6, ui=ui)
        # Physical parameters
        self.m_c = 1.0  # Mass of the cart
        self.m_p = 0.1  # Mass of the pendulum
        self.l = 0.5    # Length to pendulum center of mass
        self.g = 9.81   # Acceleration due to gravity

        # Controller gains
        self.kp_theta = tk.DoubleVar(value=100.0)
        self.ki_theta = tk.DoubleVar(value=0.0)
        self.kd_theta = tk.DoubleVar(value=20.0)

        # State variables
        self.x = [0.0]          # Cart position
        self.x_dot = [0.0]      # Cart velocity
        self.theta = [0.05]     # Pendulum angle (radians), small initial angle
        self.theta_dot = [0.0]  # Pendulum angular velocity

        self.time_elapsed = 0.0
        self.simulation_running = False
        self.animation = None
        self.message_label = None

        # Data for plotting
        self.times = [0.0]
        self.control_forces = [0.0]
    
    def start(self):
        # Clear the content_frame
        for widget in self.ui.content_frame.winfo_children():
            widget.destroy()

        self.quest_frame = tk.Frame(self.ui.content_frame)
        self.quest_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.quest_frame, text=self.description, style="Quest.Title.TLabel").pack(pady=20)

        self.control_frame = tk.Frame(self.quest_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # Sliders for controller gains
        ttk.Label(self.control_frame, text="Adjust Kp for θ:", style="Quest.TLabel").pack(pady=5)
        self.kp_theta_slider = tk.Scale(self.control_frame, from_=0.0, to=200.0, orient=tk.HORIZONTAL, variable=self.kp_theta, length=200, resolution=1.0)
        self.kp_theta_slider.pack(pady=5)

        ttk.Label(self.control_frame, text="Adjust Ki for θ:", style="Quest.TLabel").pack(pady=5)
        self.ki_theta_slider = tk.Scale(self.control_frame, from_=0.0, to=10.0, orient=tk.HORIZONTAL, variable=self.ki_theta, length=200, resolution=0.1)
        self.ki_theta_slider.pack(pady=5)

        ttk.Label(self.control_frame, text="Adjust Kd for θ:", style="Quest.TLabel").pack(pady=5)
        self.kd_theta_slider = tk.Scale(self.control_frame, from_=0.0, to=50.0, orient=tk.HORIZONTAL, variable=self.kd_theta, length=200, resolution=1.0)
        self.kd_theta_slider.pack(pady=5)

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
        (self.canvas, self.fig, self.ax_animation, self.cart_patch, self.pendulum_line,
         self.ax_angle, self.line_angle, self.ax_force, self.line_force) = Visualization.create_inverted_pendulum_plot(self.plot_frame)
    
    def start_simulation(self):
        if self.simulation_running:
            return  # Prevent multiple simulations at once

        # Reset simulation parameters
        self.time_elapsed = 0.0
        self.times = [0.0]
        self.x = [0.0]
        self.x_dot = [0.0]
        self.theta = [0.05]  # Small initial angle in radians
        self.theta_dot = [0.0]
        self.control_forces = [0.0]
        self.integral_error = 0.0
        self.previous_error = 0.0

        # Reset plots
        self.line_angle.set_data([], [])
        self.ax_angle.set_xlim(0, 10)
        self.ax_angle.set_ylim(-0.5, 0.5)
        self.line_force.set_data([], [])
        self.ax_force.set_xlim(0, 10)
        self.ax_force.set_ylim(-50, 50)

        self.simulation_running = True

        # Start the animation
        self.animate()

    def reset_simulation(self):
        if self.simulation_running:
            return  # Prevent multiple simulations at once

        # Reset simulation parameters
        self.time_elapsed = 0.0
        self.times = [0.0]
        self.x = [0.0]
        self.x_dot = [0.0]
        self.theta = [0.05]  # Small initial angle in radians
        self.theta_dot = [0.0]
        self.control_forces = [0.0]
        self.integral_error = 0.0
        self.previous_error = 0.0

        # Reset plots
        self.line_angle.set_data([], [])
        self.ax_angle.set_xlim(0, 10)
        self.ax_angle.set_ylim(-0.5, 0.5)
        self.line_force.set_data([], [])
        self.ax_force.set_xlim(0, 10)
        self.ax_force.set_ylim(-50, 50)

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
        dt = 0.02  # Time step
        max_time = 10.0  # Maximum simulation time

        # Retrieve controller gains
        Kp_theta = self.kp_theta.get()
        Ki_theta = self.ki_theta.get()
        Kd_theta = self.kd_theta.get()

        # Current state
        x = self.x[-1]
        x_dot = self.x_dot[-1]
        theta = self.theta[-1]
        theta_dot = self.theta_dot[-1]

        # Error for controller (theta should be zero)
        error = 0.0 - theta
        self.integral_error += error * dt
        derivative_error = (error - self.previous_error) / dt
        self.previous_error = error

        # Control force (PID controller)
        u = Kp_theta * error + Ki_theta * self.integral_error + Kd_theta * derivative_error

        # Limit control force
        u = max(-100.0, min(u, 100.0))

        # Equations of motion (linearized)
        m_c = self.m_c
        m_p = self.m_p
        l = self.l
        g = self.g

        # Compute accelerations
        theta_double_dot = (g * theta + u / (m_c + m_p)) / l
        x_double_dot = u / (m_c + m_p)

        # Update velocities and positions using Euler's method
        theta_dot_new = theta_dot + theta_double_dot * dt
        theta_new = theta + theta_dot_new * dt

        x_dot_new = x_dot + x_double_dot * dt
        x_new = x + x_dot_new * dt

        # Update time
        self.time_elapsed += dt

        # Append new values
        self.times.append(self.time_elapsed)
        self.x.append(x_new)
        self.x_dot.append(x_dot_new)
        self.theta.append(theta_new)
        self.theta_dot.append(theta_dot_new)
        self.control_forces.append(u)

        # Update animation
        self.update_animation(x_new, theta_new)

        # Update plots
        self.line_angle.set_data(self.times, self.theta)
        self.ax_angle.set_xlim(0, max(10, self.time_elapsed))
        self.ax_angle.set_ylim(-0.5, 0.5)

        self.line_force.set_data(self.times, self.control_forces)
        self.ax_force.set_xlim(0, max(10, self.time_elapsed))
        self.ax_force.set_ylim(min(self.control_forces) - 10, max(self.control_forces) + 10)

        # Redraw canvas
        self.canvas.draw()

        # Continue simulation or check success
        if self.time_elapsed < max_time:
            self.ui.root.after(int(dt * 1000), self.animate)
        else:
            self.simulation_running = False
            self.check_success()

    def update_animation(self, x, theta):
        # Update cart position
        cart_width = 0.4
        cart_height = 0.2
        self.cart_patch.set_xy((x - cart_width/2, 0))

        # Update pendulum position
        pendulum_x = [x, x + self.l * np.sin(theta)]
        pendulum_y = [0.1, 0.1 + self.l * np.cos(theta)]
        self.pendulum_line.set_data(pendulum_x, pendulum_y)


    def check_success(self):
        # Check if the pendulum remained upright within a tolerance
        upright_tolerance = 0.05  # Radians (~2.86 degrees)
        duration = 2.0  # Seconds the pendulum must remain upright

        # Check if the pendulum angle stayed within tolerance for the last 'duration' seconds
        indices = [i for i, t in enumerate(self.times) if t >= self.time_elapsed - duration]
        if all(abs(self.theta[i]) < upright_tolerance for i in indices):
            self.display_message("Success! You've balanced the pendulum.", success=True)
            self.ui.root.after(2000, self.end_quest)
        else:
            self.display_message("The pendulum fell. Try adjusting the controller gains.", error=True)

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

