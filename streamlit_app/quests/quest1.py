# ./streamlit_app/quest1.py

import streamlit as st
import math
import matplotlib.pyplot as plt

def run():
    # Title and description for the quest
    st.title("Quest 1: Solve the Triangle Problem")
    st.subheader("Adjust the sides of a right-angled triangle and see the hypotenuse update in real time!")

    # Sliders for input sides
    side_a = st.slider("Adjust side a (base):", 1.0, 20.0, 3.0, step=0.1)
    side_b = st.slider("Adjust side b (height):", 1.0, 20.0, 4.0, step=0.1)

    # Calculate the hypotenuse
    hypotenuse = math.sqrt(side_a**2 + side_b**2)

    # Create the triangle plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot([0, side_a, 0, 0], [0, 0, side_b, 0], "b", label="_nolegend_")

    ax.text(side_a/2, -0.4, f"a", ha='center', va='top', fontsize=10, color='blue')
    ax.text(-0.4, side_b/2, f"b", ha='right', va='center', fontsize=10, color='blue')
    ax.text(0.25+side_a/2, 0.25+side_b/2, f"c", ha='center', va='center', fontsize=10, color='red')
    
    # Add points to mark the vertices of the triangle
    ax.scatter([0, side_a, 0], [0, 0, side_b], color='black')  # Vertices: (0,0), (side_a,0), (0,side_b)

    # Add labels and grid
    ax.set_xlim(-2, max(side_a, side_b) + 2)
    ax.set_ylim(-2, max(side_a, side_b) + 2)
    ax.set_xlabel("Base (a)", fontsize=12)
    ax.set_ylabel("Height (b)", fontsize=12)
    ax.set_aspect('equal', 'box')
    ax.set_title("Right-Angled Triangle", fontsize=14)
    ax.grid(True)

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Input field for user's answer
    user_answer = st.number_input("Enter your calculated hypotenuse value:", value=0.0, step=0.01)

    # Check button for validation
    if st.button("Check Answer"):
        if math.isclose(user_answer, hypotenuse, rel_tol=1e-2):
            st.success("Correct! Well done.")
        else:
            st.error(f"Incorrect. The correct answer is **{hypotenuse:.2f}**.")
