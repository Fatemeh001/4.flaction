# Load the dataset
file_path = 'Processed.xlsx'
import pandas as pd

data = pd.read_excel(file_path, sheet_name='fcpi_m')

# Extract unique country names
unique_countries = data['Country'].unique()

# Display unique countries
print("List of countries in the dataset:")
print(unique_countries)
