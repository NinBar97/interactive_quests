# visualization.py

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Visualization:
    @staticmethod
    def create_triangle_plot(parent, a, b, max_side):
        """
        Creates a right-angled triangle plot with labeled sides a and b.
        """
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Plot triangle lines
        line, = ax.plot([0, a, 0, 0], [0, 0, b, 0], "b")

        # Label the triangle's sides
        side_a_label = ax.text(a / 2, -0.5, f"a = {a:.1f}", ha='center', va='top', fontsize=10, color='blue')
        side_b_label = ax.text(-0.5, b / 2, f"b = {b:.1f}", ha='right', va='center', fontsize=10, color='blue')

        # Set plot properties
        ax.set_title("Right-Angled Triangle")
        ax.set_xlim(-5, max_side + 1)
        ax.set_ylim(-5, max_side + 1)
        ax.set_aspect('equal', 'box')
        ax.grid(True)

        # Embed the plot in the tkinter parent frame
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        return canvas, line, side_a_label, side_b_label

    @staticmethod
    def update_triangle_plot(canvas, line, side_a_label, side_b_label, a, b):
        """
        Updates an existing triangle plot with new side lengths.
        """
        # Update line data
        line.set_data([0, a, 0, 0], [0, 0, b, 0])

        # Update side labels
        side_a_label.set_position((a / 2, -0.5))
        side_a_label.set_text(f"a = {a:.1f}")

        side_b_label.set_position((-0.5, b / 2))
        side_b_label.set_text(f"b = {b:.1f}")

        # Redraw the canvas
        canvas.draw_idle()

    @staticmethod
    def create_projectile_plot(parent, target_distance, initial_speed, gravity):
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot target
        target_plot, = ax.plot(target_distance, 0, 'ro', markersize=15, label='Target')
        
        # Set plot limits
        max_height = (initial_speed ** 2) / (2 * gravity)
        ax.set_xlim(0, target_distance * 1.8)
        ax.set_ylim(-5, max_height * 1.2)
        
        # Ground line
        ax.axhline(0, color='green', linestyle='--')
        
        # Labels and grid
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Height (m)')
        ax.set_title('Projectile Motion')
        ax.grid(True)
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        
        # Initialize the projectile line
        projectile_line, = ax.plot([], [], 'b-', label='Projectile Path')
        
        return canvas, ax, projectile_line, target_plot
    
    @staticmethod
    def update_projectile_plot(ax, target_distance, initial_speed, gravity, x_coords, y_coords):
        # Clear the axes
        ax.clear()
        
        # Plot target
        target_plot, = ax.plot(target_distance, 0, 'ro', markersize=15, label='Target')
        
        # Ground line
        ax.axhline(0, color='green', linestyle='--')
        
        # Set plot limits
        max_height = max(y_coords) * 1.2
        ax.set_xlim(0, target_distance * 1.8)
        ax.set_ylim(-5, max_height)
        
        # Labels and grid
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Height (m)')
        ax.set_title('Projectile Motion')
        ax.grid(True)
        ax.legend()
        
        # Initialize the projectile line
        projectile_line, = ax.plot([], [], 'b-', label='Projectile Path')
        
        return projectile_line, target_plot
    
    @staticmethod
    def animate_projectile(canvas, projectile_line, x_coords, y_coords, index):
        if index < len(x_coords):
            x = x_coords[:index]
            y = y_coords[:index]
            
            # Update the projectile line data
            projectile_line.set_data(x, y)
            
            canvas.draw()
            index += 1
            # Return the updated index
            return index
        else:
            # Animation is complete
            return None

    @staticmethod
    def create_single_tank_control_plot(parent, desired_level):
        fig, axs = plt.subplots(1, 3, figsize=(15, 4), dpi=100)
        fig.subplots_adjust(wspace=0.3)

        # Left plot: Water tank diagram
        tank_ax = axs[0]
        tank_ax.set_title('Water Tank')
        tank_ax.set_xlim(0, 2)
        tank_ax.set_ylim(0, 1.5)
        tank_ax.axis('off')  # Hide axes

        # Draw the tank
        rect = plt.Rectangle((0.5, 0.0), 1, 1, fill=False)
        tank_ax.add_patch(rect)
        # Initialize water level
        water_patch = plt.Rectangle((0.5, 0.0), 1, 0, facecolor='blue', edgecolor='blue')
        tank_ax.add_patch(water_patch)

        # Add desired level line in Tank
        desired_line_tank = tank_ax.hlines(y=desired_level, xmin=0.5, xmax=1.5, colors='red', linestyles='dashed', label='Desired Level')

        # Middle plot: Water level over time
        level_ax = axs[1]
        level_ax.set_title('Water Level Over Time')
        level_ax.set_xlabel('Time (s)')
        level_ax.set_ylabel('Water Level (m)')
        level_ax.set_xlim(0, 50)
        level_ax.set_ylim(0, 1.0)
        # Line for the tank
        level_line, = level_ax.plot([], [], label='Tank')
        desired_level_line = level_ax.axhline(y=desired_level, color='red', linestyle='--', label='Desired Level')
        level_ax.legend()

        # Right plot: Controller variables over time
        control_ax = axs[2]
        control_ax.set_title('Controller Variables Over Time')
        control_ax.set_xlabel('Time (s)')
        control_ax.set_ylabel('Value')
        control_ax.set_xlim(0, 50)
        # Lines for Kv and errors
        kv_line, = control_ax.plot([], [], label='Kv (Control Signal)')
        error_line, = control_ax.plot([], [], label='Error (e)')
        integral_error_line, = control_ax.plot([], [], label='Integral Error (∫e dt)')
        derivative_error_line, = control_ax.plot([], [], label='Derivative Error (de/dt)')
        control_ax.legend()
    
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
    
        # Return the new lines as part of the output
        return (canvas, fig, tank_ax, level_ax,
                water_patch, level_line, desired_level_line, control_ax, 
                kv_line, error_line, integral_error_line, derivative_error_line)
        
    @staticmethod
    def draw_tanks(ax):
        water_patches = []
        # Draw three tanks
        for i in range(3):
            rect = plt.Rectangle((0.5, i * 1.5), 1, 1, fill=False)
            ax.add_patch(rect)
            # Initialize water levels
            water = plt.Rectangle((0.5, i * 1.5), 1, 0, facecolor='blue', edgecolor='blue')
            ax.add_patch(water)
            water_patches.append(water)
        return water_patches

    @staticmethod
    def create_mass_spring_damper_plots(parent):
        # Create a figure with multiple subplots
        fig = plt.Figure(figsize=(12, 6), dpi=100)
        
        # Grid specification for subplots
        gs = fig.add_gridspec(2, 2)

        # Subplot for trolley animation
        ax_animation = fig.add_subplot(gs[0, 0])
        ax_animation.set_xlim(-10, 20)
        ax_animation.set_ylim(-5, 5)
        ax_animation.axis('off')  # Hide axes for animation
        # Draw the fixed spring origin
        ax_animation.plot([-10, -5], [0, 0], color='black', linewidth=2)
        # Initialize trolley and spring lines
        trolley, = ax_animation.plot([], [], 's', markersize=20, color='blue')
        spring_line, = ax_animation.plot([], [], color='black', linewidth=2)
        # Target position indicator
        target_marker = ax_animation.axvline(x=10, color='red', linestyle='--', label='Target Position')

        # Subplot for displacement over time
        ax_position = fig.add_subplot(gs[0, 1])
        ax_position.set_title('Displacement Over Time')
        ax_position.set_xlabel('Time (s)')
        ax_position.set_ylabel('Displacement (m)')
        ax_position.set_xlim(0, 10)
        ax_position.set_ylim(-15, 15)
        line_position, = ax_position.plot([], [], label='Position (x)')
        ax_position.legend()

        # Subplot for velocity vs displacement (phase plot)
        ax_phase = fig.add_subplot(gs[1, :])
        ax_phase.set_title('Velocity vs. Displacement (Phase Plot)')
        ax_phase.set_xlabel('Displacement (m)')
        ax_phase.set_ylabel('Velocity (m/s)')
        ax_phase.set_xlim(-15, 15)
        ax_phase.set_ylim(-15, 15)
        line_phase, = ax_phase.plot([], [], label='Phase Trajectory')
        ax_phase.legend()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        return (canvas, fig, ax_animation, trolley, spring_line, ax_position, line_position,
                ax_phase, line_phase)

    @staticmethod
    def create_inverted_pendulum_plot(parent):
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        gs = fig.add_gridspec(2, 2)

        # Animation subplot
        ax_animation = fig.add_subplot(gs[:, 0])
        ax_animation.set_xlim(-2, 2)
        ax_animation.set_ylim(-0.5, 1.5)
        ax_animation.set_aspect('equal')
        ax_animation.axis('off')

        # Draw ground
        ax_animation.plot([-2, 2], [0, 0], 'k')

        # Initialize cart
        cart_width = 0.4
        cart_height = 0.2
        cart_patch = plt.Rectangle((-cart_width/2, 0), cart_width, cart_height, fill=True, color='blue')
        ax_animation.add_patch(cart_patch)

        # Initialize pendulum
        pendulum_line, = ax_animation.plot([], [], lw=2, color='red')

        # Subplot for pendulum angle over time
        ax_angle = fig.add_subplot(gs[0, 1])
        ax_angle.set_title('Pendulum Angle Over Time')
        ax_angle.set_xlabel('Time (s)')
        ax_angle.set_ylabel('Angle (rad)')
        line_angle, = ax_angle.plot([], [], label='θ(t)')
        ax_angle.legend()

        # Subplot for control force over time
        ax_force = fig.add_subplot(gs[1, 1])
        ax_force.set_title('Control Force Over Time')
        ax_force.set_xlabel('Time (s)')
        ax_force.set_ylabel('Force (N)')
        line_force, = ax_force.plot([], [], label='u(t)')
        ax_force.legend()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        return (canvas, fig, ax_animation, cart_patch, pendulum_line, ax_angle, line_angle, ax_force, line_force)
    

    @staticmethod
    def create_loss_accuracy_plots(parent):
        fig, axs = plt.subplots(2, 2, figsize=(12, 8), dpi=100)
        fig.subplots_adjust(wspace=0.3, hspace=0.3)

        # Training Loss
        ax_train_loss = axs[0, 0]
        ax_train_loss.set_title('Training Loss')
        ax_train_loss.set_xlabel('Epoch')
        ax_train_loss.set_ylabel('Loss')
        line_train_loss, = ax_train_loss.plot([], [], label='Training Loss', color='blue')
        ax_train_loss.legend()

        # Validation Loss
        ax_val_loss = axs[0, 1]
        ax_val_loss.set_title('Validation Loss')
        ax_val_loss.set_xlabel('Epoch')
        ax_val_loss.set_ylabel('Loss')
        line_val_loss, = ax_val_loss.plot([], [], label='Validation Loss', color='orange')
        ax_val_loss.legend()

        # Training Accuracy
        ax_train_acc = axs[1, 0]
        ax_train_acc.set_title('Training Accuracy')
        ax_train_acc.set_xlabel('Epoch')
        ax_train_acc.set_ylabel('Accuracy (%)')
        line_train_acc, = ax_train_acc.plot([], [], label='Training Accuracy', color='green')
        ax_train_acc.legend()

        # Validation Accuracy
        ax_val_acc = axs[1, 1]
        ax_val_acc.set_title('Validation Accuracy')
        ax_val_acc.set_xlabel('Epoch')
        ax_val_acc.set_ylabel('Accuracy (%)')
        line_val_acc, = ax_val_acc.plot([], [], label='Validation Accuracy', color='red')
        ax_val_acc.legend()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        return (canvas, fig, ax_train_loss, line_train_loss,
                ax_val_loss, line_val_loss,
                ax_train_acc, line_train_acc,
                ax_val_acc, line_val_acc)
