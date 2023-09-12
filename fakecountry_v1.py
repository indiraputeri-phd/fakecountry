# Importing necessary libraries
import geopandas as gpd
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

# Initialize parameters
num_areas = 100  # Number of areas in the fake country
x_min, x_max = 0, 100  # X-coordinate limits for the bounding box
y_min, y_max = 0, 100  # Y-coordinate limits for the bounding box

# Generate random points within the bounding box
np.random.seed(12923)  # for reproducibility
points = np.random.rand(num_areas, 2) * [x_max - x_min, y_max - y_min] + [x_min, y_min]

# Create a Voronoi diagram based on the random points
vor = Voronoi(points)

# Plot the Voronoi diagram for a quick look
voronoi_plot_2d(vor)
plt.title('Voronoi Diagram')
plt.show()

# Create a bounding box (square) to represent the fake country's borders
bounding_box = Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)])

# Initialize an empty list to store the polygons that are inside the bounding box
clipped_polygons = []

# Clip Voronoi polygons to the bounding box
for region in vor.regions:
    # Skip empty regions and the region with points at infinity
    if len(region) == 0 or -1 in region:
        continue
    # Create a polygon from the Voronoi region
    polygon = Polygon([vor.vertices[i] for i in region])
    # Clip the polygon to the bounding box
    clipped_polygon = polygon.intersection(bounding_box)
    # Store the clipped polygon
    if isinstance(clipped_polygon, Polygon):  # Only keep Polygon objects (not MultiPolygon or other types)
        clipped_polygons.append(clipped_polygon)

# Create a GeoDataFrame to store the clipped polygons
gdf = gpd.GeoDataFrame({'geometry': clipped_polygons})

# Plot the polygons clipped to the bounding box (fake country)
gdf.boundary.plot()
plt.title('Fake Country with Neighboring Areas')
plt.show()

# Save the GeoDataFrame to a shapefile
shapefile_path = 'data/fakecountry'
gdf.to_file(shapefile_path)

shapefile_path
