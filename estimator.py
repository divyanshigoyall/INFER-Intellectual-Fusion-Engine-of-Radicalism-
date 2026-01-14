import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Function to calculate the solar energy output
def calculate_energy():
    try:
        # Get user inputs from the entry fields
        latitude = float(entry_latitude.get())
        longitude = float(entry_longitude.get())
        roof_area = float(entry_roof_area.get())
        panel_efficiency = float(entry_panel_efficiency.get()) / 100
        performance_ratio = float(entry_performance_ratio.get())
        year = int(entry_year.get())
        tilt = float(entry_tilt.get())
        azimuth = float(entry_azimuth.get())

        # Determine solar irradiance based on latitude
        if latitude > 30:
            avg_solar_irradiance = 5.0  # High solar irradiance for sunnier locations
        else:
            avg_solar_irradiance = 4.0  # Lower solar irradiance for less sunny locations

        # Calculate daily energy output
        daily_energy = avg_solar_irradiance * roof_area * panel_efficiency * performance_ratio

        # Estimate yearly energy (365 days)
        days_in_year = 365
        annual_energy = daily_energy * days_in_year

        # Generate monthly energy output (assume 30 days per month)
        monthly_energy = np.full(12, daily_energy * 30)
        monthly_energy_df = pd.DataFrame({
            'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            'Estimated Energy (kWh)': monthly_energy.round(2)
        })

        # Display the results in the table format
        result_text = ""
        result_text += "\n📊 Monthly Energy Output:\n"
        result_text += "\nMonth                      Estimated Energy (kWh)\n"
        result_text += "-" * 40 + "\n"
        for index, row in monthly_energy_df.iterrows():
            result_text += f"{row['Month']:<25} {row['Estimated Energy (kWh)']:>10}\n"

        # Add the summary results
        result_text += "\n📌 Summary\n"
        result_text += f"🔆 Total Annual Energy      : {annual_energy:.2f} kWh\n"
        result_text += f"📈 Average Daily Output     : {daily_energy:.2f} kWh\n"
        result_text += f"✅ Highest Monthly Output   : {monthly_energy.max():.2f} kWh ({monthly_energy_df.iloc[monthly_energy.argmax()]['Month']})\n"
        result_text += f"⚠️  Lowest Monthly Output    : {monthly_energy.min():.2f} kWh ({monthly_energy_df.iloc[monthly_energy.argmin()]['Month']})\n"

        # Export the result to Excel
        excel_file = "solar_output_estimate.xlsx"
        monthly_energy_df.to_excel(excel_file, index=False)

        result_text += f"\n📁 Monthly data exported to: {excel_file}\n"

        # Show results in the text box
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result_text)

        # Show the graph
        plt.figure(figsize=(10, 6))
        plt.bar(monthly_energy_df['Month'], monthly_energy_df['Estimated Energy (kWh)'], color='skyblue')
        plt.xlabel('Month')
        plt.ylabel('Energy (kWh)')
        plt.title('Monthly Solar Energy Output')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")

# Setup the main window
root = tk.Tk()
root.title("Solar Energy Estimator")
root.geometry("500x600")

# Add input labels and fields
label_latitude = tk.Label(root, text="Enter Latitude (e.g., 26.91):")
label_latitude.pack()
entry_latitude = tk.Entry(root)
entry_latitude.pack()

label_longitude = tk.Label(root, text="Enter Longitude (e.g., 75.78):")
label_longitude.pack()
entry_longitude = tk.Entry(root)
entry_longitude.pack()

label_roof_area = tk.Label(root, text="Enter Roof Area in m² (e.g., 100):")
label_roof_area.pack()
entry_roof_area = tk.Entry(root)
entry_roof_area.pack()

label_panel_efficiency = tk.Label(root, text="Enter Panel Efficiency % (e.g., 18):")
label_panel_efficiency.pack()
entry_panel_efficiency = tk.Entry(root)
entry_panel_efficiency.pack()

label_performance_ratio = tk.Label(root, text="Enter Performance Ratio (e.g., 0.75):")
label_performance_ratio.pack()
entry_performance_ratio = tk.Entry(root)
entry_performance_ratio.pack()

label_year = tk.Label(root, text="Enter Year (e.g., 2024):")
label_year.pack()
entry_year = tk.Entry(root)
entry_year.pack()

label_tilt = tk.Label(root, text="Enter Tilt Angle in degrees (e.g., 27):")
label_tilt.pack()
entry_tilt = tk.Entry(root)
entry_tilt.pack()

label_azimuth = tk.Label(root, text="Enter Azimuth Angle in degrees (180 for South):")
label_azimuth.pack()
entry_azimuth = tk.Entry(root)
entry_azimuth.pack()

# Button to calculate energy
calculate_button = tk.Button(root, text="Calculate Energy", command=calculate_energy)
calculate_button.pack(pady=20)

# Text box to show the output
output_text = tk.Text(root, height=15, width=50)
output_text.pack()

# Run the main loop
root.mainloop()
