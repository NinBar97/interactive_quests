# ./streamlit_app/quests/quest4.py

import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Constants
HIT_TOLERANCE = 0.05  # Tolerance for stabilizing water level
GRAVITY = 9.81         # Acceleration due to gravity (m/s^2)

def reset_simulation():
    """Reset all simulation parameters and session state."""
    st.session_state.water_level = 0.0
    st.session_state.time_elapsed = 0.0
    st.session_state.integral_error = 0.0
    st.session_state.previous_error = 0.0
    st.session_state.times = [0.0]
    st.session_state.water_levels = [0.0]
    st.session_state.kv_values = [0.0]
    st.session_state.error_values = [0.0]
    st.session_state.integral_error_values = [0.0]
    st.session_state.derivative_error_values = [0.0]
    st.session_state.simulation_complete = False
    st.session_state.message = ""

def initialize_session_state():
    """Initialize the session state variables if they do not exist."""
    if "water_level" not in st.session_state:
        st.session_state.water_level = 0.0  # Current water level
    if "time_elapsed" not in st.session_state:
        st.session_state.time_elapsed = 0.0
    if "integral_error" not in st.session_state:
        st.session_state.integral_error = 0.0
    if "previous_error" not in st.session_state:
        st.session_state.previous_error = 0.0
    if "times" not in st.session_state:
        st.session_state.times = [0.0]
    if "water_levels" not in st.session_state:
        st.session_state.water_levels = [0.0]
    if "kv_values" not in st.session_state:
        st.session_state.kv_values = [0.0]
    if "error_values" not in st.session_state:
        st.session_state.error_values = [0.0]
    if "integral_error_values" not in st.session_state:
        st.session_state.integral_error_values = [0.0]
    if "derivative_error_values" not in st.session_state:
        st.session_state.derivative_error_values = [0.0]
    if "simulation_complete" not in st.session_state:
        st.session_state.simulation_complete = False
    if "message" not in st.session_state:
        st.session_state.message = ""

def simulate_pid(Kp, Ki, Kd, desired_level=0.5, simulation_time=50, dt=0.1):
    """
    Simulate the PID controller for maintaining water level.
    
    Parameters:
        Kp (float): Proportional gain
        Ki (float): Integral gain
        Kd (float): Derivative gain
        desired_level (float): Desired water level (meters)
        simulation_time (float): Total simulation time (seconds)
        dt (float): Time step (seconds)
    
    Returns:
        dict: Dictionary containing simulation data
    """
    times = [0.0]
    water_levels = [0.0]
    kv_values = [0.0]
    error_values = [desired_level - 0.0]
    integral_error_values = [0.0]
    derivative_error_values = [0.0]
    
    water_level = 0.0
    integral_error = 0.0
    previous_error = desired_level - water_level
    
    for t in np.arange(dt, simulation_time + dt, dt):
        error = desired_level - water_level
        integral_error += error * dt
        derivative_error = (error - previous_error) / dt
        previous_error = error
        
        # PID Control Signal
        Kv = Kp * error + Ki * integral_error + Kd * derivative_error
        Kv = max(0.0, min(Kv, 1.0))  # Clamp Kv between 0 and 1
        
        # Update water level based on control signal
        Q_in = 0.1  # Constant inflow rate (m³/s)
        A = 1.0     # Cross-sectional area of the tank (m²)
        Q_out = Kv * np.sqrt(max(water_level, 0.0))  # Outflow proportional to sqrt(level)
        
        dh_dt = (Q_in - Q_out) / A
        water_level += dh_dt * dt
        water_level = max(0.0, min(water_level, 1.0))  # Clamp between 0 and 1
        
        # Append data
        times.append(t)
        water_levels.append(water_level)
        kv_values.append(Kv)
        error_values.append(error)
        integral_error_values.append(integral_error)
        derivative_error_values.append(derivative_error)
    
    simulation_data = {
        "times": times,
        "water_levels": water_levels,
        "kv_values": kv_values,
        "error_values": error_values,
        "integral_error_values": integral_error_values,
        "derivative_error_values": derivative_error_values
    }
    
    return simulation_data

def run():
    """Run the Quest 4 simulation."""
    initialize_session_state()

    st.title("Quest 4: Tune the Controller to Maintain the Water Level")
    st.subheader("Adjust the PID controller gains to stabilize the water level in the tank.")

    # Simulation parameters
    desired_level = 0.5  # Desired water level (meters)

    # User Inputs
    st.sidebar.header("PID Controller Parameters")
    Kp = st.sidebar.slider("Proportional Gain (Kp):", 0.0, 10.0, 1.0, step=0.1)
    Ki = st.sidebar.slider("Integral Gain (Ki):", 0.0, 5.0, 0.1, step=0.01)
    Kd = st.sidebar.slider("Derivative Gain (Kd):", 0.0, 5.0, 0.1, step=0.01)

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

    # Display target level
    st.write(f"**Desired Water Level:** {desired_level:.2f} meters")

    # Initialize Plotly Figures
    water_tank_placeholder = st.empty()
    controller_plot_placeholder = st.empty()

    if start_button and not st.session_state.simulation_complete:
        # Simulate PID controller
        simulation_data = simulate_pid(Kp, Ki, Kd, desired_level=desired_level)
        
        # Store simulation data in session_state for potential further use
        st.session_state.times = simulation_data["times"]
        st.session_state.water_levels = simulation_data["water_levels"]
        st.session_state.kv_values = simulation_data["kv_values"]
        st.session_state.error_values = simulation_data["error_values"]
        st.session_state.integral_error_values = simulation_data["integral_error_values"]
        st.session_state.derivative_error_values = simulation_data["derivative_error_values"]
        st.session_state.simulation_complete = True  # Mark simulation as complete

    if st.session_state.simulation_complete:
        # Create Water Tank Visualization
        fig_tank = go.Figure()
        fig_tank.add_trace(go.Bar(
            x=["Water Level"],
            y=[st.session_state.water_levels[-1]],
            width=[0.5],
            marker_color='blue',
            name='Current Level'
        ))
        # Add Desired Level Marker
        fig_tank.add_trace(go.Scatter(
            x=["Water Level"],
            y=[desired_level],
            mode='markers',
            marker=dict(color='red', size=12, symbol='diamond'),
            name='Desired Level'
        ))
        fig_tank.update_layout(
            title="Water Tank Level",
            yaxis=dict(range=[0, 1.0], title="Level (m)"),
            xaxis=dict(showticklabels=False),
            barmode='group'
        )

        # Create Controller Variables Plot with Animation
        fig_controller = go.Figure()

        # Add traces
        fig_controller.add_trace(go.Scatter(
            x=st.session_state.times,
            y=st.session_state.kv_values,
            mode='lines+markers',
            name='Kv (Control Signal)',
            line=dict(color='blue')
        ))
        fig_controller.add_trace(go.Scatter(
            x=st.session_state.times,
            y=st.session_state.error_values,
            mode='lines+markers',
            name='Error',
            line=dict(color='red')
        ))
        fig_controller.add_trace(go.Scatter(
            x=st.session_state.times,
            y=st.session_state.integral_error_values,
            mode='lines+markers',
            name='Integral Error',
            line=dict(color='green')
        ))
        fig_controller.add_trace(go.Scatter(
            x=st.session_state.times,
            y=st.session_state.derivative_error_values,
            mode='lines+markers',
            name='Derivative Error',
            line=dict(color='orange')
        ))

        # Add frames for animation
        frames = []
        for i in range(1, len(st.session_state.times)):
            frames.append(go.Frame(
                data=[
                    go.Bar(
                        x=["Water Level"],
                        y=[st.session_state.water_levels[i]],
                        width=[0.5],
                        marker_color='blue',
                        name='Current Level'
                    ),
                    go.Scatter(
                        x=["Water Level"],
                        y=[desired_level],
                        mode='markers',
                        marker=dict(color='red', size=12, symbol='diamond'),
                        name='Desired Level'
                    ),
                    go.Scatter(
                        x=st.session_state.times[:i+1],
                        y=st.session_state.kv_values[:i+1],
                        mode='lines+markers',
                        name='Kv (Control Signal)',
                        line=dict(color='blue')
                    ),
                    go.Scatter(
                        x=st.session_state.times[:i+1],
                        y=st.session_state.error_values[:i+1],
                        mode='lines+markers',
                        name='Error',
                        line=dict(color='red')
                    ),
                    go.Scatter(
                        x=st.session_state.times[:i+1],
                        y=st.session_state.integral_error_values[:i+1],
                        mode='lines+markers',
                        name='Integral Error',
                        line=dict(color='green')
                    ),
                    go.Scatter(
                        x=st.session_state.times[:i+1],
                        y=st.session_state.derivative_error_values[:i+1],
                        mode='lines+markers',
                        name='Derivative Error',
                        line=dict(color='orange')
                    )
                ],
                name=f'frame{i}'
            ))

        # Update layout for animation
        fig_controller.update_layout(
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
                    direction="left",
                    pad={"r": 10, "t": 87},
                    showactive=False,
                    x=0.1,
                    xanchor="right",
                    y=0,
                    yanchor="top"
                )
            ],
            sliders=[{
                "steps": [{
                    "args": [
                        [f'frame{k}'],
                        {"frame": {"duration": 50, "redraw": True},
                         "mode": "immediate",
                         "transition": {"duration": 0}}
                    ],
                    "label": str(k),
                    "method": "animate"
                } for k in range(1, len(st.session_state.times))]
            }],
            title="Controller Variables Over Time",
            xaxis_title="Time (s)",
            yaxis_title="Value",
            showlegend=True
        )

        # Add frames to the figure
        fig_controller.frames = frames

        # Display the plots
        water_tank_placeholder.plotly_chart(fig_tank, use_container_width=True, key='water_tank_plot')
        controller_plot_placeholder.plotly_chart(fig_controller, use_container_width=True, key='controller_variables_plot')

        # Check Success Criteria
        final_error = abs(desired_level - st.session_state.water_level)
        if final_error < HIT_TOLERANCE:
            st.success("Success! The water level is stable around the desired level.")
        else:
            st.error("Failure! The water level did not stabilize as desired. Try adjusting the PID gains.")
