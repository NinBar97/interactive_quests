# ./streamlit_app/quests/quest5.py

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Constants
TARGET_POSITION = 10.0  # Target position where the mass should stop
VELOCITY_THRESHOLD = 0.05  # Threshold for considering the mass as stopped
POSITION_TOLERANCE = 0.1   # Acceptable distance from target position

def reset_simulation():
    """Reset all simulation parameters and session state."""
    st.session_state.time_elapsed = 0.0
    st.session_state.times = [0.0]
    st.session_state.positions = [st.session_state.initial_displacement]
    st.session_state.velocities = [0.0]
    st.session_state.simulation_complete = False
    st.session_state.success = False
    st.session_state.message = ""

def initialize_session_state():
    """Initialize the session state variables if they do not exist."""
    if 'mass' not in st.session_state:
        st.session_state.mass = 1.0
    if 'spring_const' not in st.session_state:
        st.session_state.spring_const = 1.0
    if 'damping_coeff' not in st.session_state:
        st.session_state.damping_coeff = 0.1
    if 'initial_displacement' not in st.session_state:
        st.session_state.initial_displacement = 0.0
    if 'time_elapsed' not in st.session_state:
        st.session_state.time_elapsed = 0.0
    if 'times' not in st.session_state:
        st.session_state.times = [0.0]
    if 'positions' not in st.session_state:
        st.session_state.positions = [st.session_state.initial_displacement]
    if 'velocities' not in st.session_state:
        st.session_state.velocities = [0.0]
    if 'simulation_complete' not in st.session_state:
        st.session_state.simulation_complete = False
    if 'success' not in st.session_state:
        st.session_state.success = False
    if 'message' not in st.session_state:
        st.session_state.message = ""

def simulate_mass_spring_damper(m, K_s, K_d, x0, simulation_time=10.0, dt=0.01):
    """
    Simulate the mass-spring-damper system.

    Returns:
        times (list): Time steps.
        positions (list): Position at each time step.
        velocities (list): Velocity at each time step.
    """
    times = [0.0]
    positions = [x0]
    velocities = [0.0]  # Initial velocity is zero

    # Initial conditions
    x = x0
    v = 0.0
    t = 0.0

    # Shift reference frame
    x_target = TARGET_POSITION - x0

    while t < simulation_time:
        # Calculate acceleration
        a = (-K_d * v - K_s * (x - x_target)) / m

        # Update velocity and position
        v += a * dt
        x += v * dt

        # Update time
        t += dt

        # Store data
        times.append(t)
        positions.append(x)
        velocities.append(v)

        # Check for stopping condition
        if abs(v) < VELOCITY_THRESHOLD and abs(x - TARGET_POSITION) < POSITION_TOLERANCE:
            break

    return times, positions, velocities

def create_animation(times, positions):
    """
    Create an animation of the mass-spring-damper system.
    """
    frames = []
    for i in range(len(times)):
        x = positions[i]
        # Spring representation
        spring_x = np.linspace(-10, x, 500)
        spring_y = 0.1 * np.sin(2 * np.pi * 20 * (spring_x - (-10)) / (x - (-10) + 0.1))
        # Mass representation
        mass_x = [x]
        mass_y = [0]

        frame = go.Frame(
            data=[
                go.Scatter(x=spring_x, y=spring_y, mode='lines', line=dict(color='black'), name='Spring'),
                go.Scatter(x=mass_x, y=mass_y, mode='markers', marker=dict(size=20, color='blue'), name='Mass'),
            ],
            name=str(i)
        )
        frames.append(frame)

    # Initial data
    x_init = positions[0]
    spring_x_init = np.linspace(-10, x_init, 500)
    spring_y_init = 0.1 * np.sin(2 * np.pi * 20 * (spring_x_init - (-10)) / (x_init - (-10) + 0.1))
    mass_x_init = [x_init]
    mass_y_init = [0]

    fig = go.Figure(
        data=[
            go.Scatter(x=spring_x_init, y=spring_y_init, mode='lines', line=dict(color='black'), name='Spring'),
            go.Scatter(x=mass_x_init, y=mass_y_init, mode='markers', marker=dict(size=20, color='blue'), name='Mass'),
        ],
        layout=go.Layout(
            xaxis=dict(range=[-15, 15], autorange=False),
            yaxis=dict(range=[-1, 1], autorange=False),
            title="Mass-Spring-Damper System Animation",
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(label="Play",
                             method="animate",
                             args=[None, {"frame": {"duration": 50, "redraw": True},
                                          "fromcurrent": True, "transition": {"duration": 0}}]),
                        dict(label="Pause",
                             method="animate",
                             args=[[None], {"frame": {"duration": 0, "redraw": False},
                                            "mode": "immediate",
                                            "transition": {"duration": 0}}])
                    ],
                    showactive=False,
                    x=0.1,
                    y=0,
                    xanchor="right",
                    yanchor="top"
                )
            ]
        ),
        frames=frames
    )

    return fig

def create_displacement_plot(times, positions):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=positions, mode='lines', name='Displacement'))
    fig.add_trace(go.Scatter(x=[times[0], times[-1]], y=[TARGET_POSITION, TARGET_POSITION],
                             mode='lines', name='Target Position', line=dict(dash='dash', color='red')))
    fig.update_layout(title="Displacement Over Time", xaxis_title="Time (s)", yaxis_title="Position")
    return fig

def create_phase_plot(positions, velocities):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=positions, y=velocities, mode='lines', name='Phase Plot'))
    fig.update_layout(title="Phase Plot (Position vs. Velocity)", xaxis_title="Position", yaxis_title="Velocity")
    return fig

def run():
    """Run the Quest 5 simulation."""
    initialize_session_state()

    st.title("Quest 5: Adjust Parameters to Stop the Mass at the Target Position")
    st.subheader("Adjust the mass-spring-damper parameters to make the mass stop at the target position.")

    # Sidebar for parameter adjustments
    st.sidebar.header("Simulation Parameters")
    st.session_state.mass = st.sidebar.slider("Mass (m):", 0.1, 10.0, st.session_state.mass, step=0.1)
    st.session_state.spring_const = st.sidebar.slider("Spring Constant (K_s):", 0.1, 10.0, st.session_state.spring_const, step=0.1)
    st.session_state.damping_coeff = st.sidebar.slider("Damping Coefficient (K_d):", 0.0, 5.0, st.session_state.damping_coeff, step=0.1)
    st.session_state.initial_displacement = st.sidebar.slider("Initial Displacement (x0):", -5.0, 15.0, st.session_state.initial_displacement, step=0.1)

    # Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        start_button = st.button("Start Simulation")
    with col2:
        reset_button = st.button("Reset Simulation")
    with col3:
        skip_button = st.button("Skip Quest")

    # Handle Buttons
    if reset_button:
        reset_simulation()
        st.rerun()

    if skip_button:
        st.warning("Quest skipped.")
        # Implement skip functionality as needed
        st.stop()

    # Start Simulation
    if start_button and not st.session_state.simulation_complete:
        times, positions, velocities = simulate_mass_spring_damper(
            st.session_state.mass,
            st.session_state.spring_const,
            st.session_state.damping_coeff,
            st.session_state.initial_displacement
        )

        # Update session state with simulation data
        st.session_state.times = times
        st.session_state.positions = positions
        st.session_state.velocities = velocities
        st.session_state.simulation_complete = True

        # Check for success
        final_velocity = velocities[-1]
        final_position = positions[-1]
        position_error = abs(final_position - TARGET_POSITION)

        if abs(final_velocity) < VELOCITY_THRESHOLD and position_error < POSITION_TOLERANCE:
            st.session_state.success = True
            st.session_state.message = "Success! The mass has stopped at the target position."
        else:
            st.session_state.success = False
            st.session_state.message = "Adjust parameters to stop the mass at the target position."

    # Display Simulation Results
    if st.session_state.simulation_complete:
        # Animation
        animation_fig = create_animation(st.session_state.times, st.session_state.positions)
        st.plotly_chart(animation_fig, use_container_width=True)

        # Displacement over time
        displacement_fig = create_displacement_plot(st.session_state.times, st.session_state.positions)
        st.plotly_chart(displacement_fig, use_container_width=True)

        # Phase plot
        phase_fig = create_phase_plot(st.session_state.positions, st.session_state.velocities)
        st.plotly_chart(phase_fig, use_container_width=True)

        # Display message
        if st.session_state.success:
            st.success(st.session_state.message)
        else:
            st.error(st.session_state.message)
