# visualization.py
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt
import tkinter as tk

class Visualization:
    @staticmethod
    def create_triangle_plot(parent, a, b, a_max, b_max):

        c = sqrt(a**2 + b**2)
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot the triangle
        line, = ax.plot([0, a, 0, 0], [0, 0, b, 0], "b")
        title = ax.set_title(f"Right-Angled Triangle\nHypotenuse: {c:.2f}")
        ax.set_xlim(-1, max(a_max, b_max) + 1)
        ax.set_ylim(-1, max(a_max, b_max) + 1)
        ax.set_aspect('equal', 'box')
        ax.grid(True)

        # Create a canvas and add it to the parent frame
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        return canvas, line, title
