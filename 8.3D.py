import lightningchart as lc
import pandas as pd
import numpy as np
import trimesh
import asyncio

with open('D:/fatemeh_ajam/lightningChart/A/license-key', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Processed.xlsx'
def_a_data = pd.read_excel(file_path, sheet_name='def_a')

country = "Turkey"

years = [str(year) for year in range(2000, 2024)]
if country in def_a_data['Country'].values:
    inflation_data = (
        def_a_data[def_a_data['Country'] == country]
        .filter(regex='^' + '|^'.join(years))
        .values.flatten()
    )
else:
    print(f"Country '{country}' does not exist in the dataset.")
    exit()

min_inflation = min(inflation_data)
max_inflation = max(inflation_data)
normalized_heights = [
    ((value - min_inflation) / (max_inflation - min_inflation)) * 2 
    for value in inflation_data
]

chart = lc.Chart3D(title="GDP growth rate-Driven Balloon Movement", theme=lc.Themes.Light)

balloon_model = chart.add_mesh_model()

balloon_obj_path = 'Air_Balloon.obj'
balloon_scene = trimesh.load(balloon_obj_path)

if isinstance(balloon_scene, trimesh.Scene):
    balloon_mesh = balloon_scene.dump(concatenate=True)
else:
    balloon_mesh = balloon_scene

balloon_vertices = balloon_mesh.vertices.flatten().tolist()
balloon_indices = balloon_mesh.faces.flatten().tolist()
balloon_normals = balloon_mesh.vertex_normals.flatten().tolist()
balloon_model.set_model_geometry(vertices=balloon_vertices, indices=balloon_indices, normals=balloon_normals)

balloon_model.set_scale(0.015)
balloon_model.set_model_location(0, 0, 0)

balloon_model.set_color_shading_style(
    phong_shading=True,
    specular_reflection=0.8,
    specular_color=lc.Color(221, 227, 52)
)

chart.get_default_x_axis().set_title('X')
chart.get_default_y_axis().set_title('Height (GDP deflator growth rate )').set_interval(-1, 2)
chart.get_default_z_axis().set_title('Z')

chart.open(live=True)

async def move_balloon():
    for year, height in zip(years, normalized_heights):
        chart.set_title(f"GDP deflator growth rate -Driven Balloon Movement ({year})")

        print(f"Year: {year}, GDP deflator growth rate : {inflation_data[list(years).index(year)]}, Height: {height}")

        balloon_model.set_model_location(0, height, 0)

        await asyncio.sleep(1)  

asyncio.run(move_balloon())
