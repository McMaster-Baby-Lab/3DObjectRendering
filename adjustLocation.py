import pandas as pd
import numpy as np
import ast

# Load the spreadsheet
file_path = '/Users/naiqixiao/Downloads/object_names_Pumpkin.csv'
data = pd.read_csv(file_path)

# Display the first few rows to understand its structure
data.head()

# Reset the dataframe to original state for Location and deltaLocation adjustments
data['Location'] = data['Location'].apply(ast.literal_eval)
data['newLocation'] = [[] for _ in range(len(data))]
data['deltaLocation'] = [[] for _ in range(len(data))]

# First, we process base objects to set their Location to [0,0,0] and calculate deltaLocation
for index, row in data.iterrows():
    if row['ObjectType'] == 'base':
        original_location = np.array(row['Location'])
        delta_location = -original_location
        data.at[index, 'newLocation'] = [0, 0, 0]
        data.at[index, 'deltaLocation'] = delta_location.tolist()

# Create a mapping from AssociatedBaseIndex to deltaLocation for base objects
base_delta_mapping = {}
for index, row in data[data['ObjectType'] == 'base'].iterrows():
    base_delta_mapping[row['AssociatedBaseIndex']] = row['deltaLocation']

# Update Locations for part objects using the base_delta_mapping
for index, row in data.iterrows():
    if row['ObjectType'] == 'part':
        associated_base_delta = np.array(base_delta_mapping.get(row['AssociatedBaseIndex'], [0, 0, 0]))
        part_location = np.array(row['Location'])
        updated_location = part_location + associated_base_delta
        data.at[index, 'newLocation'] = updated_location.tolist()
        data.at[index, 'deltaLocation'] = associated_base_delta.tolist()

# Display a few rows to verify the updates
data.head()

# Save the updated dataframe to a new CSV file
updated_file_path = '/Users/naiqixiao/Downloads/updated_object_names_Pumpkin.csv'
data.to_csv(updated_file_path, index=False)