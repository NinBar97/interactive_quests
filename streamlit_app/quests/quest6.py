# ./streamlit_app/quests/quest6.py

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Physical parameters
M_C = 1.0   # Mass of the cart (kg)
M_P = 0.1   # Mass of the pendulum (kg)
L = 0.5     # Length to pendulum center of mass (m)
G = 9.81    # Acceleration due to gravity (m/s^2)

# Success criteria
UPRIGHT_TOLERANCE = 0.05  # Radians (~2.86 degrees)
UPRIGHT_DURATION = 2.0    # Seconds the pendulum must remain upright
MAX_SIMULATION_TIME = 10.0  # Maximum simulation time (s)
DT = 0.02  # Time step (s)

def reset_simulation():
    """Reset all simulation parameters and session state."""
    st.session_state.time_elapsed = 0.0
    st.session_state.times = [0.0]
    st.session_state.x = [0.0]
    st.session_state.x_dot = [0.0]
    st.session_state.theta = [0.05]  # Small initial angle in radians
    st.session_state.theta_dot = [0.0]
    st.session_state.control_forces = [0.0]
    st.session_state.integral_error = 0.0
    st.session_state.previous_error = 0.0
    st.session_state.simulation_complete = False
    st.session_state.success = False
    st.session_state.message = ""

def initialize_session_state():
    """Initialize the session state variables if they do not exist."""
    if 'kp_theta' not in st.session_state:
        st.session_state.kp_theta = 100.0
    if 'ki_theta' not in st.session_state:
        st.session_state.ki_theta = 0.0
    if 'kd_theta' not in st.session_state:
        st.session_state.kd_theta = 20.0
    if 'time_elapsed' not in st.session_state:
        st.session_state.time_elapsed = 0.0
    if 'times' not in st.session_state:
        st.session_state.times = [0.0]
    if 'x' not in st.session_state:
        st.session_state.x = [0.0]
    if 'x_dot' not in st.session_state:
        st.session_state.x_dot = [0.0]
    if 'theta' not in st.session_state:
        st.session_state.theta = [0.05]
    if 'theta_dot' not in st.session_state:
        st.session_state.theta_dot = [0.0]
    if 'control_forces' not in st.session_state:
        st.session_state.control_forces = [0.0]
    if 'integral_error' not in st.session_state:
        st.session_state.integral_error = 0.0
    if 'previous_error' not in st.session_state:
        st.session_state.previous_error = 0.0
    if 'simulation_complete' not in st.session_state:
        st.session_state.simulation_complete = False
    if 'success' not in st.session_state:
        st.session_state.success = False
    if 'message' not in st.session_state:
        st.session_state.message = ""

def simulate_inverted_pendulum(kp, ki, kd):
    """
    Simulate the inverted pendulum system using a PID controller.

    Returns:
        dict: Simulation data containing times, positions, angles, etc.
    """
    times = [0.0]
    x = [0.0]
    x_dot = [0.0]
    theta = [0.05]  # Small initial angle
    theta_dot = [0.0]
    control_forces = [0.0]
    integral_error = 0.0
    previous_error = 0.0

    time_elapsed = 0.0

    while time_elapsed < MAX_SIMULATION_TIME:
        # Current state
        current_theta = theta[-1]
        current_theta_dot = theta_dot[-1]
        current_x = x[-1]
        current_x_dot = x_dot[-1]

        # Error for controller (theta should be zero)
        error = 0.0 - current_theta
        integral_error += error * DT
        derivative_error = (error - previous_error) / DT
        previous_error = error

        # Control force (PID controller)
        u = kp * error + ki * integral_error + kd * derivative_error

        # Limit control force
        u = max(-100.0, min(u, 100.0))

        # Equations of motion (linearized)
        m_c = M_C
        m_p = M_P
        l = L
        g = G

        # Compute accelerations
        denom = m_c + m_p
        theta_double_dot = (g * np.sin(current_theta) + np.cos(current_theta) * (-u - m_p * l * current_theta_dot**2 * np.sin(current_theta)) / denom) / (l * (4.0/3.0 - m_p * np.cos(current_theta)**2 / denom))
        x_double_dot = (u + m_p * l * (current_theta_dot**2 * np.sin(current_theta) - theta_double_dot * np.cos(current_theta))) / denom

        # Update velocities and positions using Euler's method
        current_theta_dot += theta_double_dot * DT
        current_theta += current_theta_dot * DT

        current_x_dot += x_double_dot * DT
        current_x += current_x_dot * DT

        # Update time
        time_elapsed += DT

        # Append new values
        times.append(time_elapsed)
        x.append(current_x)
        x_dot.append(current_x_dot)
        theta.append(current_theta)
        theta_dot.append(current_theta_dot)
        control_forces.append(u)

        # Check if the pendulum has fallen over
        if abs(current_theta) > np.pi / 2:
            break  # Pendulum has fallen over

    simulation_data = {
        'times': times,
        'x': x,
        'x_dot': x_dot,
        'theta': theta,
        'theta_dot': theta_dot,
        'control_forces': control_forces
    }

    return simulation_data

def create_animation(simulation_data):
    """
    Create an animation of the inverted pendulum system.
    """
    times = simulation_data['times']
    x = simulation_data['x']
    theta = simulation_data['theta']

    frames = []
    for i in range(len(times)):
        cart_x = x[i]
        pendulum_x = [cart_x, cart_x + L * np.sin(theta[i])]
        pendulum_y = [0.0, L * np.cos(theta[i])]

        frame = go.Frame(
            data=[
                # Cart
                go.Scatter(
                    x=[cart_x - 0.2, cart_x + 0.2],
                    y=[0.0, 0.0],
                    mode='lines',
                    line=dict(color='blue', width=10),
                    name='Cart'
                ),
                # Pendulum
                go.Scatter(
                    x=pendulum_x,
                    y=pendulum_y,
                    mode='lines+markers',
                    line=dict(color='red', width=4),
                    marker=dict(size=12, color='red'),
                    name='Pendulum'
                )
            ],
            name=str(i)
        )
        frames.append(frame)

    # Initial data
    cart_x = x[0]
    pendulum_x = [cart_x, cart_x + L * np.sin(theta[0])]
    pendulum_y = [0.0, L * np.cos(theta[0])]

    fig = go.Figure(
        data=[
            # Cart
            go.Scatter(
                x=[cart_x - 0.2, cart_x + 0.2],
                y=[0.0, 0.0],
                mode='lines',
                line=dict(color='blue', width=10),
                name='Cart'
            ),
            # Pendulum
            go.Scatter(
                x=pendulum_x,
                y=pendulum_y,
                mode='lines+markers',
                line=dict(color='red', width=4),
                marker=dict(size=12, color='red'),
                name='Pendulum'
            )
        ],
        layout=go.Layout(
            xaxis=dict(range=[-5, 5], autorange=False, zeroline=False),
            yaxis=dict(range=[-L - 0.5, L + 0.5], autorange=False, zeroline=False),
            title="Inverted Pendulum Animation",
            height=400,
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

def create_angle_plot(simulation_data):
    times = simulation_data['times']
    theta = simulation_data['theta']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=theta, mode='lines', name='Pendulum Angle'))
    fig.add_trace(go.Scatter(x=[times[0], times[-1]], y=[UPRIGHT_TOLERANCE, UPRIGHT_TOLERANCE],
                             mode='lines', name='Tolerance', line=dict(dash='dash', color='green')))
    fig.add_trace(go.Scatter(x=[times[0], times[-1]], y=[-UPRIGHT_TOLERANCE, -UPRIGHT_TOLERANCE],
                             mode='lines', name='Tolerance', line=dict(dash='dash', color='green'), showlegend=False))
    fig.update_layout(title="Pendulum Angle Over Time", xaxis_title="Time (s)", yaxis_title="Angle (rad)")
    return fig

def create_force_plot(simulation_data):
    times = simulation_data['times']
    control_forces = simulation_data['control_forces']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=control_forces, mode='lines', name='Control Force'))
    fig.update_layout(title="Control Force Over Time", xaxis_title="Time (s)", yaxis_title="Force (N)")
    return fig

def run():
    """Run the Quest 6 simulation."""
    initialize_session_state()

    st.title("Quest 6: Balance the Inverted Pendulum by Tuning the Controller")
    st.subheader("Adjust the PID controller gains to balance the inverted pendulum.")

    # Sidebar for controller gains
    st.sidebar.header("Controller Gains")
    st.session_state.kp_theta = st.sidebar.slider("Proportional Gain (Kp) for θ:", 0.0, 200.0, st.session_state.kp_theta, step=1.0)
    st.session_state.ki_theta = st.sidebar.slider("Integral Gain (Ki) for θ:", 0.0, 10.0, st.session_state.ki_theta, step=0.1)
    st.session_state.kd_theta = st.sidebar.slider("Derivative Gain (Kd) for θ:", 0.0, 50.0, st.session_state.kd_theta, step=1.0)

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
        simulation_data = simulate_inverted_pendulum(
            st.session_state.kp_theta,
            st.session_state.ki_theta,
            st.session_state.kd_theta
        )

        # Update session state with simulation data
        st.session_state.times = simulation_data['times']
        st.session_state.x = simulation_data['x']
        st.session_state.x_dot = simulation_data['x_dot']
        st.session_state.theta = simulation_data['theta']
        st.session_state.theta_dot = simulation_data['theta_dot']
        st.session_state.control_forces = simulation_data['control_forces']
        st.session_state.time_elapsed = simulation_data['times'][-1]
        st.session_state.simulation_complete = True

        # Check for success
        indices = [i for i, t in enumerate(st.session_state.times) if t >= st.session_state.time_elapsed - UPRIGHT_DURATION]
        if all(abs(st.session_state.theta[i]) < UPRIGHT_TOLERANCE for i in indices):
            st.session_state.success = True
            st.session_state.message = "Success! You've balanced the pendulum."
        else:
            st.session_state.success = False
            st.session_state.message = "The pendulum fell. Try adjusting the controller gains."

    # Display Simulation Results
    if st.session_state.simulation_complete:
        # Animation
        animation_fig = create_animation({
            'times': st.session_state.times,
            'x': st.session_state.x,
            'theta': st.session_state.theta
        })
        st.plotly_chart(animation_fig, use_container_width=True)

        # Angle over time
        angle_fig = create_angle_plot({
            'times': st.session_state.times,
            'theta': st.session_state.theta
        })
        st.plotly_chart(angle_fig, use_container_width=True)

        # Control force over time
        force_fig = create_force_plot({
            'times': st.session_state.times,
            'control_forces': st.session_state.control_forces
        })
        st.plotly_chart(force_fig, use_container_width=True)

        # Display message
        if st.session_state.success:
            st.success(st.session_state.message)
        else:
            st.error(st.session_state.message)
