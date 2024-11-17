# import lightningchart as lc
# import pandas as pd
# import numpy as np
# import trimesh
# import asyncio
# import math

# with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# file_path = 'Processed.xlsx'
# def_a_data = pd.read_excel(file_path, sheet_name='def_a')

# countries = ["Turkey", "Iran, Islamic Rep.", "Egypt, Arab Rep."]  # Add countries of interest
# years = [str(year) for year in range(2000, 2024)]

# country_data = {}
# for country in countries:
#     if country in def_a_data['Country'].values:
#         inflation_data = (
#             def_a_data[def_a_data['Country'] == country]
#             .filter(regex='^' + '|^'.join(years))
#             .values.flatten()
#         )
#         country_data[country] = inflation_data
#     else:
#         print(f"Country '{country}' does not exist in the dataset.")
#         exit()

# min_inflation = min(min(values) for values in country_data.values())
# max_inflation = max(max(values) for values in country_data.values())
# normalized_heights = {
#     country: [
#         ((value - min_inflation) / (max_inflation - min_inflation)) * 2
#         for value in values
#     ]
#     for country, values in country_data.items()
# }

# balloon_colors = {
#     "Turkey": lc.Color(255, 0, 0),  # Red
#     "Iran, Islamic Rep.": lc.Color(0, 255, 0),  # Green
#     "Egypt, Arab Rep.": lc.Color(0, 0, 255)  # Blue
# }

# chart = lc.Chart3D(title="Balloon Race: Inflation by Country", theme=lc.Themes.Light)

# chart.get_default_x_axis().set_title('Countries').set_interval(-2, len(countries) * 2)
# chart.get_default_y_axis().set_title('Height (Inflation)').set_interval(-1, 2)
# chart.get_default_z_axis().set_title('Time (Years)').set_interval(0, len(years))

# balloons = {}
# balloon_obj_path = 'Air_Balloon.obj'
# balloon_scene = trimesh.load(balloon_obj_path)

# if isinstance(balloon_scene, trimesh.Scene):
#     balloon_mesh = balloon_scene.dump(concatenate=True)
# else:
#     balloon_mesh = balloon_scene

# balloon_vertices = balloon_mesh.vertices.flatten().tolist()
# balloon_indices = balloon_mesh.faces.flatten().tolist()
# balloon_normals = balloon_mesh.vertex_normals.flatten().tolist()

# for i, country in enumerate(country_data.keys()):
#     balloon = chart.add_mesh_model()
#     balloon.set_model_geometry(vertices=balloon_vertices, indices=balloon_indices, normals=balloon_normals)
#     balloon.set_scale(0.01)  
#     balloon.set_model_location(i * 2, 0, 0) 
#     balloon.set_color(balloon_colors[country]) 
#     balloon.set_color_shading_style(
#         phong_shading=True,
#         specular_reflection=0.8,
#         specular_color=lc.Color(255, 255, 255)
#     )
#     balloons[country] = balloon

# async def move_balloons():
#     for year_idx, year in enumerate(years):
#         print(f"Year: {year}")
#         for i, country in enumerate(countries):
#             height = normalized_heights[country][year_idx]
#             balloons[country].set_model_location(i * 2, height, year_idx)
#         chart.set_title(f"Balloon Race: Year {year}")
#         await asyncio.sleep(1)  
# # Run the animation
# chart.open(live=True)
# asyncio.run(move_balloons())



import lightningchart as lc
import pandas as pd
import numpy as np
import trimesh
import asyncio

# Load the license key
with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load datasets
file_path = 'Processed.xlsx'
def_a_data = pd.read_excel(file_path, sheet_name='def_a')
ecpi_data = pd.read_excel(file_path, sheet_name='ecpi_m')

# Select countries and years
countries = ["Turkey", "Iran, Islamic Rep.", "Egypt, Arab Rep."]
years = [str(year) for year in range(2000, 2024)]

# Prepare inflation data
country_data = {}
for country in countries:
    if country in def_a_data['Country'].values:
        inflation_data = (
            def_a_data[def_a_data['Country'] == country]
            .filter(regex='^' + '|^'.join(years))
            .iloc[0]
        )
        country_data[country] = inflation_data.tolist()
    else:
        print(f"Country '{country}' does not exist in the dataset.")
        exit()

# Normalize inflation data
min_inflation = min(min(values) for values in country_data.values())
max_inflation = max(max(values) for values in country_data.values())
normalized_heights = {
    country: [
        ((value - min_inflation) / (max_inflation - min_inflation)) * 2
        for value in values
    ]
    for country, values in country_data.items()
}

# Prepare energy price data (ECPI)
energy_data = {}
for country in countries:
    if country in ecpi_data['Country'].values:
        monthly_data = ecpi_data[ecpi_data['Country'] == country]
        monthly_data.columns = monthly_data.columns.map(str)
        monthly_data = monthly_data.apply(pd.to_numeric, errors='coerce')  # Ensure numeric
        annual_data = monthly_data.groupby(lambda x: x[:4], axis=1).mean().iloc[0].tolist()
        energy_data[country] = annual_data
    else:
        print(f"Country '{country}' does not exist in the energy dataset.")
        exit()

# Normalize energy data
min_energy = min(min(values) for values in energy_data.values())
max_energy = max(max(values) for values in energy_data.values())
normalized_energy = {
    country: [
        ((value - min_energy) / (max_energy - min_energy))
        for value in values
    ]
    for country, values in energy_data.items()
}

# Define initial balloon colors
balloon_colors = {
    "Turkey": (0, 0, 255),  # Blue
    "Iran, Islamic Rep.": (0, 255, 0),  # Green
    "Egypt, Arab Rep.": (255, 0, 0)  # Red
}

# Create the 3D Chart
chart = lc.Chart3D(title="Balloon Race: Inflation & Energy", theme=lc.Themes.Light)
chart.get_default_x_axis().set_title('Countries').set_interval(-2, len(countries) * 2)
chart.get_default_y_axis().set_title('Height (Inflation)').set_interval(0, 2)
chart.get_default_z_axis().set_title('Time (Years)').set_interval(0, len(years))

# Add balloons
balloons = {}
balloon_obj_path = 'Air_Balloon.obj'
balloon_scene = trimesh.load(balloon_obj_path)

if isinstance(balloon_scene, trimesh.Scene):
    balloon_mesh = balloon_scene.dump(concatenate=True)
else:
    balloon_mesh = balloon_scene

balloon_vertices = balloon_mesh.vertices.flatten().tolist()
balloon_indices = balloon_mesh.faces.flatten().tolist()
balloon_normals = balloon_mesh.vertex_normals.flatten().tolist()

for i, country in enumerate(countries):
    balloon = chart.add_mesh_model()
    balloon.set_model_geometry(vertices=balloon_vertices, indices=balloon_indices, normals=balloon_normals)
    balloon.set_scale(0.01)
    balloon.set_model_location(i * 2, 0, 0)
    balloon.set_color_shading_style(
        phong_shading=True,
        specular_reflection=0.8,
        specular_color=lc.Color(255, 255, 255)
    )
    balloons[country] = balloon

# Function to calculate brightness-adjusted color
def adjust_color(base_color, brightness):
    r, g, b = base_color
    inverse_brightness = 1 - brightness  # Invert brightness
    return lc.Color(int(r * inverse_brightness), int(g * inverse_brightness), int(b * inverse_brightness))

# Define a function for real-time balloon movement
async def move_balloons():
    for year_idx, year in enumerate(years):
        print(f"Year: {year}")
        for i, country in enumerate(countries):
            height = normalized_heights[country][year_idx]
            brightness = normalized_energy[country][year_idx]
            color = adjust_color(balloon_colors[country], brightness)
            balloons[country].set_model_location(i * 2, height, year_idx)
            balloons[country].set_color(color)
        chart.set_title(f"Balloon Race: Year {year}")
        await asyncio.sleep(1)

# Run the animation
chart.open(live=True)
asyncio.run(move_balloons())

