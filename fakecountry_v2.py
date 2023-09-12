# Executing the user's Python script to generate the shapefile
# Importing the necessary modules first
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

# Initialize parameters
num_areas = 100  # Number of areas in the fake country (will be used to generate points, but we'll only select 50 areas)
x_min, x_max = 0, 100  # X-coordinate limits for the bounding box
y_min, y_max = 0, 100  # Y-coordinate limits for the bounding box

# Generate random points within the bounding box
np.random.seed(12923)  # for reproducibility
points = np.random.rand(num_areas, 2) * [x_max - x_min, y_max - y_min] + [x_min, y_min]

# Create Voronoi polygons
vor = Voronoi(points)

# Create Geopandas GeoDataFrame from Voronoi polygons
poly_shapes = []
poly_ids = []
for i, region in enumerate(vor.regions):
    if not -1 in region and len(region) > 0:
        poly = Polygon([vor.vertices[i] for i in region])
        poly_shapes.append(poly)
        poly_ids.append(i)

gdf_v2 = gpd.GeoDataFrame({'geometry': poly_shapes, 'id': poly_ids})

# Create a larger irregular shape for clipping instead of a square
larger_irregular_shape = Polygon([(2, 2), (98, 10), (95, 98), (10, 95), (2, 2)])
gdf_clipped_larger_v2 = gdf_v2.copy()
gdf_clipped_larger_v2['geometry'] = gdf_v2.intersection(larger_irregular_shape)

# Merge small fragments into a single shape
merged_shape_larger_v2 = unary_union(gdf_clipped_larger_v2['geometry'])
final_gdf_larger_v2 = gdf_clipped_larger_v2[gdf_clipped_larger_v2.intersects(merged_shape_larger_v2)]

# Compute the area of each polygon and filter out small areas
final_gdf_larger_v2['area'] = final_gdf_larger_v2['geometry'].area
area_threshold = 20  # Area threshold for filtering small areas
filtered_gdf_v2 = final_gdf_larger_v2[final_gdf_larger_v2['area'] > area_threshold]

# Save to a shapefile
shapefile_path = 'data/fakecountry'
filtered_gdf_v2.to_file(shapefile_path)

# Plot the final shape of the fake country
filtered_gdf_v2.plot()
plt.show()

