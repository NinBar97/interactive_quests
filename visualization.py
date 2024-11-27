# visualization.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt
import tkinter as tk

class Visualization:
    @staticmethod
    def plot_triangle(parent, a, b):

        # Clear the parent frame
        for widget in parent.winfo_children():
            widget.destroy()

        c = sqrt(a**2 + b**2)
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot the triangle
        ax.plot([0, a, 0, 0], [0, 0, b, 0], "b")
        ax.set_title(f"Right-Angled Triangle\nHypotenuse: {c:.2f}")
        ax.set_xlim(0, max(a, b) + 1)
        ax.set_ylim(0, max(a, b) + 1)
        ax.set_aspect('equal', 'box')
        ax.grid(True)

        # Create a canvas and add it to the parent frame
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        return canvas
