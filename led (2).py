import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import Boltzmann as k
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# LED properties dictionary
led_properties = {
    'Red': {'V_f': 1.8, 'I_f': 20e-3},
    'Green': {'V_f': 2.2, 'I_f': 20e-3},
    'Blue': {'V_f': 3.0, 'I_f': 20e-3},
    'Yellow': {'V_f': 2.1, 'I_f': 20e-3},
    'White': {'V_f': 3.2, 'I_f': 20e-3}
}

# Custom dialog box for feedback
def custom_message_dialog(title, message):
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.configure(bg='#222')
    dialog.geometry("300x150")
    tk.Label(dialog, text=message, fg='white', bg='#222', font=('Arial', 12)).pack(pady=20)
    tk.Button(dialog, text='OK', command=dialog.destroy, bg='#444', fg='white').pack(pady=10)
    dialog.transient()
    dialog.grab_set()
    dialog.wait_window()

# Diode equation to calculate current
def diode_current(V, V_f, I_f, T=300):
    q = 1.6e-19
    V_T = k * T / q
    try:
        I = I_f * (np.exp(V / V_T) - 1)
        return I
    except OverflowError:
        return np.inf

# Inverse: Calculate voltage for given current
def diode_voltage(I_target, V_f, T=300):
    q = 1.6e-19
    V_T = k * T / q
    try:
        V = V_T * np.log((I_target / 20e-3) + 1)
        return V
    except:
        return None

# Modify characteristics based on conditions
def apply_modifications(V_f, I_f, temp, duration):
    delta_temp = (temp - 25) * 0.002
    delta_duration = (duration - 0) * 0.0005
    new_V_f = V_f - delta_temp - delta_duration
    new_I_f = I_f + delta_temp * 10 - delta_duration * 10
    return max(new_V_f, 0), max(new_I_f, 1e-6)

# Plotting VI curve
def plot_vi(color, mode, modified, temp, duration, show_comparison, graph_type, voltage_inputs):
    V_f = led_properties[color]['V_f']
    I_f = led_properties[color]['I_f']
    T = temp + 273.15 if modified else 298

    if modified:
        V_f, I_f = apply_modifications(V_f, I_f, temp, duration)

    # Set theme
    plt.style.use('dark_background' if mode == 'dark' else 'default')

    fig, ax = plt.subplots(figsize=(7, 5))
    for v_in in voltage_inputs:
        voltages = np.linspace(0, max(v_in + 1, 5), 100)
        currents = diode_current(voltages, V_f, I_f, T)

        label = f"{color} LED @ {v_in}V"
        if graph_type == 'line':
            ax.plot(voltages, currents * 1e3, label=label)
        elif graph_type == 'scatter':
            ax.scatter(voltages, currents * 1e3, label=label, s=10)
        elif graph_type == 'bar':
            ax.bar(voltages, currents * 1e3, width=0.05, label=label)

    if show_comparison:
        for other in led_properties:
            if other != color:
                ov, oi = led_properties[other]['V_f'], led_properties[other]['I_f']
                voltages = np.linspace(0, 5, 100)
                currents = diode_current(voltages, ov, oi, 298)
                ax.plot(voltages, currents * 1e3, '--', label=f'{other} LED')

    ax.set_title(f'VI Characteristics of {color} LED')
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (mA)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# GUI
def create_ui():
    def update_graph():
        try:
            selected_color = color_var.get()
            graph_mode = mode_var.get()
            use_modified = modified_var.get()
            temp = temp_var.get()
            duration = duration_var.get()
            comparison = comparison_var.get()
            graph_type = graph_type_var.get()
            input_mode = input_mode_var.get()
            voltage_input = voltage_input_var.get()

            if input_mode == 'Voltage to Current':
                voltages = voltage_input.split(',')
                voltages = [float(v.strip()) for v in voltages if v.strip()]
                if not voltages:
                    custom_message_dialog("Input Error", "Please enter valid voltage values.")
                    return
                plot_vi(selected_color, graph_mode, use_modified == 'Yes', temp, duration, comparison == 'Yes', graph_type, voltages)

            else:
                current_value = current_input_var.get()
                if current_value <= 0:
                    custom_message_dialog("Input Error", "Enter a valid current value.")
                    return
                voltage = diode_voltage(current_value, led_properties[selected_color]['V_f'], temp + 273.15)
                if voltage is None:
                    custom_message_dialog("Error", "Could not calculate voltage.")
                    return
                result_label.config(text=f"Required Voltage ≈ {voltage:.2f} V")
                plot_vi(selected_color, graph_mode, use_modified == 'Yes', temp, duration, comparison == 'Yes', graph_type, [voltage])

        except Exception as e:
            custom_message_dialog("Error", str(e))

    root = tk.Tk()
    root.title('VI Characteristics of LEDs')
    root.geometry('450x750')
    root.configure(bg='#f0f0f0')

    # Components
    def create_label(text):
        return tk.Label(root, text=text, bg='#f0f0f0', font=('Segoe UI', 10))

    color_var = tk.StringVar(value='Red')
    create_label('Select LED Color:').pack(pady=5)
    ttk.Combobox(root, textvariable=color_var, values=list(led_properties.keys())).pack()

    mode_var = tk.StringVar(value='light')
    create_label('Graph Theme:').pack(pady=5)
    ttk.Combobox(root, textvariable=mode_var, values=['light', 'dark']).pack()

    modified_var = tk.StringVar(value='No')
    create_label('Is LED Modified?').pack(pady=5)
    ttk.Combobox(root, textvariable=modified_var, values=['Yes', 'No']).pack()

    temp_var = tk.DoubleVar(value=25)
    create_label('Temperature (°C):').pack(pady=5)
    tk.Entry(root, textvariable=temp_var).pack()

    duration_var = tk.DoubleVar(value=0)
    create_label('Duration (s):').pack(pady=5)
    tk.Entry(root, textvariable=duration_var).pack()

    comparison_var = tk.StringVar(value='No')
    create_label('Show Comparison?').pack(pady=5)
    ttk.Combobox(root, textvariable=comparison_var, values=['Yes', 'No']).pack()

    graph_type_var = tk.StringVar(value='line')
    create_label('Graph Type:').pack(pady=5)
    ttk.Combobox(root, textvariable=graph_type_var, values=['line', 'scatter', 'bar']).pack()

    input_mode_var = tk.StringVar(value='Voltage to Current')
    create_label('Input Mode:').pack(pady=5)
    ttk.Combobox(root, textvariable=input_mode_var, values=['Voltage to Current', 'Current to Voltage']).pack()

    voltage_input_var = tk.StringVar()
    create_label('Input Voltage(s) (comma-separated):').pack(pady=5)
    tk.Entry(root, textvariable=voltage_input_var).pack()

    current_input_var = tk.DoubleVar(value=0)
    create_label('Input Current (A):').pack(pady=5)
    tk.Entry(root, textvariable=current_input_var).pack()

    result_label = create_label('Result will be shown here.')
    result_label.pack(pady=10)

    tk.Button(root, text='Generate Graph', command=update_graph, bg='#222', fg='white').pack(pady=20)

    root.mainloop()

# Run the full GUI
create_ui()
