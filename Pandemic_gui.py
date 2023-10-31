import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('your_file.csv')

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 7.2))

# Define a scaling factor for the coordinates
scaling_factor_x = 1280 / data['X'].max()
scaling_factor_y = 720 / data['Y'].max()

# Iterate through each row in the DataFrame
for index, row in data.iterrows():
    # Extract the data for each city
    city_name = row['City Name']
    color = row['Disease Color']
    x = row['X'] * scaling_factor_x
    y = row['Y'] * scaling_factor_y

    # Plot the circle with the specified color and coordinates
    circle = plt.Circle((x, y), 20, color=color, alpha=0.7)
    ax.add_patch(circle)

    # Add the label for the city
    ax.text(x, y, city_name, color='black', ha='center', va='center')

# Set the x and y limits of the plot
plt.xlim(0, 1280)
plt.ylim(0, 720)

# Set the title of the plot
plt.title('Pandemic Map')

# Show the plot
plt.show()
