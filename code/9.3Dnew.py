import lightningchart as lc
import pandas as pd
import trimesh
import asyncio

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'dataset/Processed.xlsx'
def_a_data = pd.read_excel(file_path, sheet_name='def_a')
ecpi_data = pd.read_excel(file_path, sheet_name='ecpi_m')

countries = ["Turkey", "Iran, Islamic Rep.", "Egypt, Arab Rep."]
years = [str(year) for year in range(2000, 2024)]


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

min_inflation = min(min(values) for values in country_data.values())
max_inflation = max(max(values) for values in country_data.values())
normalized_heights = {
    country: [
        ((value - min_inflation) / (max_inflation - min_inflation)) * 2
        for value in values
    ]
    for country, values in country_data.items()
}


energy_data = {}
for country in countries:
    if country in ecpi_data['Country'].values:
        monthly_data = ecpi_data[ecpi_data['Country'] == country]
        monthly_data.columns = monthly_data.columns.map(str)
        monthly_data = monthly_data.apply(pd.to_numeric, errors='coerce')
        annual_data = monthly_data.groupby(lambda x: x[:4], axis=1).mean().iloc[0].tolist()
        energy_data[country] = annual_data
    else:
        print(f"Country '{country}' does not exist in the energy dataset.")
        exit()

min_energy = min(min(values) for values in energy_data.values())
max_energy = max(max(values) for values in energy_data.values())
normalized_energy = {
    country: [
        ((value - min_energy) / (max_energy - min_energy))
        for value in values
    ]
    for country, values in energy_data.items()
}


balloon_colors = {
    "Turkey": (0, 0, 255),
    "Iran, Islamic Rep.": (0, 255, 0),
    "Egypt, Arab Rep.": (255, 0, 0)
}


chart = lc.Chart3D(title="Balloon Race: Normalized GDP Deflator Growth Rate & Energy", theme=lc.Themes.Light)

x_axis = chart.get_default_x_axis().set_tick_strategy('Empty')
x_axis.set_title('Countries')
x_axis.set_interval(-0.5, 4.5, stop_axis_after=True).add_custom_tick


custom_ticks = [0, 2, 4] 
country_labels = ['Turkey', 'Iran', 'Egypt']


for tick_value, label in zip(custom_ticks, country_labels):
    custom_tick = x_axis.add_custom_tick()
    custom_tick.set_value(tick_value)  
    custom_tick.set_text(label) 




chart.get_default_y_axis().set_title('Height (Inflation)').set_interval(0, 2,stop_axis_after=True)

z_axis = chart.get_default_z_axis()
z_axis.set_title('Time (Years)')
z_axis.set_tick_strategy('Empty')  

for i, year in enumerate(years):
    if i % 2 == 0: 
        custom_tick = z_axis.add_custom_tick()  
        custom_tick.set_value(i) 
        custom_tick.set_text(str(year))

legend = chart.add_legend().set_title("Countries")
for country, color in balloon_colors.items():
    dummy_series = chart.add_point_series()
    dummy_series.set_name(country)
    dummy_series.set_point_color(lc.Color(color[0], color[1], color[2]))
    legend.add(dummy_series)

balloons = {}
balloon_obj_path = 'dataset/Air_Balloon.obj'
balloon_scene = trimesh.load(balloon_obj_path)

if isinstance(balloon_scene, trimesh.Scene):
    balloon_mesh = balloon_scene.dump(concatenate=True)
else:
    balloon_mesh = balloon_scene

balloon_vertices = balloon_mesh.vertices.flatten().tolist()
balloon_indices = balloon_mesh.faces.flatten().tolist()
balloon_normals = balloon_mesh.vertex_normals.flatten().tolist()

for i, country in enumerate(countries):
    x_position = 0.75 + i * 1.5
    balloon = chart.add_mesh_model()
    balloon.set_model_geometry(vertices=balloon_vertices, indices=balloon_indices, normals=balloon_normals)
    balloon.set_scale(0.005)
    balloon.set_model_location(x_position, 0, 0)
    balloon.set_color_shading_style(
        phong_shading=True,
        specular_reflection=0.8,
        specular_color=lc.Color(255, 255, 255)
    )
    balloons[country] = balloon

line_series = {}
for country in countries:
    line_series[country] = chart.add_line_series()
    line_series[country].set_name(f"{country} Path")
    line_series[country].set_line_color(lc.Color(*balloon_colors[country]))

def adjust_color(base_color, brightness, sensitivity=2):
    r, g, b = base_color
    inverted_brightness = max(1 - min(brightness * sensitivity, 1.0), 0.2)
    adjusted_color = lc.Color(
        int(r * inverted_brightness),
        int(g * inverted_brightness),
        int(b * inverted_brightness)
    )
    return adjusted_color

async def move_balloons():
    for year_idx in range(len(years) - 1):
        for step in range(50):  
            for i, country in enumerate(countries):
                x_position = 0.75 + i * 1.5
                height_start = normalized_heights[country][year_idx]
                height_end = normalized_heights[country][year_idx + 1]
                brightness_start = normalized_energy[country][year_idx]
                brightness_end = normalized_energy[country][year_idx + 1]
                
                # Interpolation
                height = height_start + (height_end - height_start) * (step / 50)
                brightness = brightness_start + (brightness_end - brightness_start) * (step / 50)
                color = adjust_color(balloon_colors[country], brightness, sensitivity=2)
                
                balloons[country].set_model_location(x_position, height, year_idx + (step / 50))
                balloons[country].set_color(color)
                
                # Update line series
                line_series[country].add([x_position], [height], [year_idx + (step / 50)])
            
            await asyncio.sleep(0.02) 

chart.open(live=True)
asyncio.run(move_balloons())
