import pandas as pd
import pvlib
import plotly.express as px
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
# 2. Calculate Solar Output
# -------------------------------
print("\n🔄 Calculating solar potential, please wait...\n")

# Generate hourly time range for the specified year
times = pd.date_range(f'{year}-01-01', f'{year}-12-31 23:00:00', freq='H', tz='Asia/Kolkata')

# Solar position and irradiance model
solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
clearsky = pvlib.clearsky.ineichen(times, latitude, longitude)

# Direct Normal Irradiance (DNI), Global Horizontal Irradiance (GHI), and Diffuse Horizontal Irradiance (DHI)
dni = clearsky['dni']
ghi = clearsky['ghi']
dhi = clearsky['dhi']

# Calculate the total irradiance on a tilted surface using solar position and irradiance
irradiance = pvlib.irradiance.get_total_irradiance(
    tilt, azimuth,
    solpos['zenith'], solpos['azimuth'],
    dni, ghi, dhi
)
poa_irradiance = irradiance['poa_global']  # Plane of array irradiance

# Energy produced (in Wh) for the given roof area, panel efficiency, and performance ratio
energy_wh = poa_irradiance * roof_area * panel_efficiency * performance_ratio

# Resample to monthly energy and calculate annual energy
monthly_energy = energy_wh.resample('M').sum() / 1000  # Convert Wh to kWh
annual_energy = energy_wh.sum() / 1000  # Annual energy in kWh

# -------------------------------
# 3. Display Results
# -------------------------------
monthly_df = pd.DataFrame({
    'Month': monthly_energy.index.strftime('%B'),
    'Estimated Energy (kWh)': monthly_energy.round(2).values
})

# Display monthly energy output in tabular format
print("\n📊 Monthly Energy Output:\n")
print(tabulate(monthly_df, headers='keys', tablefmt='pretty'))

# Display a summary of the results
print("\n📌 Summary")
print(f"🔆 Total Annual Energy      : {annual_energy:.2f} kWh")
print(f"📈 Average Monthly Output   : {monthly_energy.mean():.2f} kWh")
print(f"✅ Highest Monthly Output   : {monthly_energy.max():.2f} kWh ({monthly_energy.idxmax().strftime('%B')})")
print(f"⚠️  Lowest Monthly Output    : {monthly_energy.min():.2f} kWh ({monthly_energy.idxmin().strftime('%B')})")

# -------------------------------
# 4. Export to Excel
# -------------------------------
excel_file = "solar_output.xlsx"
monthly_df.to_excel(excel_file, index=False)
print(f"\n📁 Monthly data exported to: {excel_file}")

# -------------------------------
# 5. Interactive Graph
# -------------------------------
fig = px.bar(monthly_df, x='Month', y='Estimated Energy (kWh)',
             color='Estimated Energy (kWh)', color_continuous_scale='sunset',
             title='Monthly Solar Energy Output', text_auto='.2s')

# Update graph layout
fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Energy (kWh)',
    template='plotly_white',
    title_x=0.5
)

# Display graph
fig.show()
