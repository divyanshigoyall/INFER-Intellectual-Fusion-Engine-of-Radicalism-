import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

# -------------------------------
# 1. Get User Input
# -------------------------------
print("\n🔧 Solar Energy Estimator Configuration\n")

latitude = float(input("Enter Latitude (e.g., 26.91): "))
longitude = float(input("Enter Longitude (e.g., 75.78): "))
roof_area = float(input("Enter Roof Area in m² (e.g., 100): "))
panel_efficiency = float(input("Enter Panel Efficiency % (e.g., 18): ")) / 100
performance_ratio = float(input("Enter Performance Ratio (e.g., 0.75): "))
year = int(input("Enter Year (e.g., 2024): "))
tilt = float(input("Enter Tilt Angle in degrees (e.g., 27): "))
azimuth = float(input("Enter Azimuth Angle in degrees (180 for South): "))

# -------------------------------
# 2. Calculate Solar Output (Using Assumptions)
# -------------------------------

# Assume average daily solar irradiance (in kWh/m²/day) based on latitude
# Here we're using rough estimates based on different latitudes.
if latitude > 30:
    avg_solar_irradiance = 5.0  # High solar irradiance for sunnier locations
else:
    avg_solar_irradiance = 4.0  # Lower solar irradiance for less sunny locations

# Solar Energy calculation: Energy (kWh) = Irradiance (kWh/m²/day) * Area (m²) * Efficiency * Performance Ratio
# Assuming daily energy output for each day in the year
daily_energy = avg_solar_irradiance * roof_area * panel_efficiency * performance_ratio

# Generate a simple yearly estimate (365 days)
days_in_year = 365
annual_energy = daily_energy * days_in_year

# -------------------------------
# 3. Display Results
# -------------------------------
# Create a DataFrame for the monthly energy output (assuming equal daily energy across months)
monthly_energy = np.full(12, daily_energy * 30)  # Assume 30 days per month
monthly_energy_df = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'Estimated Energy (kWh)': monthly_energy.round(2)
})

# Display monthly energy output in tabular format
print("\n📊 Monthly Energy Output:\n")
print(tabulate(monthly_energy_df, headers='keys', tablefmt='pretty'))

# Display a summary of the results
print("\n📌 Summary")
print(f"🔆 Total Annual Energy      : {annual_energy:.2f} kWh")
print(f"📈 Average Daily Output     : {daily_energy:.2f} kWh")
print(f"✅ Highest Monthly Output   : {monthly_energy.max():.2f} kWh ({monthly_energy_df.iloc[monthly_energy.argmax()]['Month']})")
print(f"⚠️  Lowest Monthly Output    : {monthly_energy.min():.2f} kWh ({monthly_energy_df.iloc[monthly_energy.argmin()]['Month']})")

# -------------------------------
# 4. Export to Excel
# -------------------------------
excel_file = "solar_output_simple.xlsx"
monthly_energy_df.to_excel(excel_file, index=False)
print(f"\n📁 Monthly data exported to: {excel_file}")

# -------------------------------
# 5. Simple Graph
# -------------------------------
plt.figure(figsize=(10, 6))
plt.bar(monthly_energy_df['Month'], monthly_energy_df['Estimated Energy (kWh)'], color='skyblue')
plt.xlabel('Month')
plt.ylabel('Energy (kWh)')
plt.title('Monthly Solar Energy Output')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
