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
