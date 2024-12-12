# ./streamlit_app/quests/quest3_2.py

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Constants
HIT_TOLERANCE = 5.0  # meters
GRAVITY = 9.8         # m/s^2

# Initialize session state for target distance and animation state
if "target_distance" not in st.session_state:
    st.session_state.target_distance = np.random.uniform(100.0, 300.0)  # Randomize target once
if "animating" not in st.session_state:
    st.session_state.animating = False

def reset_target():
    """Reset the target distance."""
    st.session_state.target_distance = np.random.uniform(100.0, 300.0)

def run():
    st.title("Quest 3: Hit the Target!")
    st.subheader("Adjust the speed and angle to launch the projectile and hit the target.")

    # Simulation parameters
    target_distance = st.session_state.target_distance  # Static target distance

    # Reset button
    if st.button("Reset Target"):
        reset_target()
        st.experimental_rerun()

    # User input
    initial_speed = st.slider("Adjust initial speed (m/s):", 10, 100, 50)
    launch_angle = st.number_input("Enter the launch angle (degrees):", value=45.0, step=0.1)

    # Display target distance
    st.write(f"**Target Distance:** {target_distance:.2f} meters")

    # Initialize a placeholder for the plot
    plot_placeholder = st.empty()

    # Initial plot setup using Plotly
    fig = go.Figure()

    # Ground line
    fig.add_trace(go.Scatter(
        x=[0, target_distance * 1.2],
        y=[0, 0],
        mode='lines',
        line=dict(color='green', dash='dash'),
        name='Ground'
    ))

    # Target
    fig.add_trace(go.Scatter(
        x=[target_distance],
        y=[0],
        mode='markers',
        marker=dict(color='red', size=12, symbol='x'),
        name='Target'
    ))

    # Projectile path (initially empty)
    projectile_trace = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        line=dict(color='blue'),
        marker=dict(color='blue', size=6),
        name='Projectile Path'
    )
    fig.add_trace(projectile_trace)

    # Set plot layout
    fig.update_layout(
        title="Projectile Motion",
        xaxis_title="Distance (m)",
        yaxis_title="Height (m)",
        xaxis=dict(range=[0, target_distance * 1.2]),
        yaxis=dict(range=[-10, 50]),
        showlegend=True,
        width=800,
        height=400
    )

    # Display the initial plot
    plot_placeholder.plotly_chart(fig, use_container_width=True)

    # Fire button with animation control
    if st.button("Fire Projectile") and not st.session_state.animating:
        st.session_state.animating = True  # Set animation state to True

        # Calculate projectile motion
        angle_rad = np.radians(launch_angle)
        t_flight = (2 * initial_speed * np.sin(angle_rad)) / GRAVITY  # Time of flight
        t = np.linspace(0, t_flight, num=200)
        x_coords = initial_speed * np.cos(angle_rad) * t
        y_coords = initial_speed * np.sin(angle_rad) * t - 0.5 * GRAVITY * t**2

        # Animation loop
        for i in range(1, len(t)):
            # Update projectile path
            projectile_trace.x = x_coords[:i]
            projectile_trace.y = y_coords[:i]

            # Update the figure
            fig.data[2].x = x_coords[:i]
            fig.data[2].y = y_coords[:i]

            # Update the plot in the placeholder
            plot_placeholder.plotly_chart(fig, use_container_width=True)

            # Adjust sleep duration for faster animation
            time.sleep(0.01)  # 10ms pause for smoother and faster animation

        # Calculate the maximum horizontal distance
        max_distance = initial_speed * np.cos(angle_rad) * t_flight

        # Check hit/miss
        if abs(max_distance - target_distance) < HIT_TOLERANCE:
            st.success("Hit! You've successfully hit the target!")
        else:
            st.error(f"Missed! The projectile traveled {max_distance:.2f} meters.")

        st.session_state.animating = False  # Reset animation state after completion
