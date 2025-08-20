import pandas as pd
import numpy as np

# Define parameters
rows = 21906
cols = 53

# Define column-specific percentages (converted to fractions)
percentages_ones = np.array([
    17.759985, 15.1857058, 13.5891357, 13.8454582, 10.8756993, 12.0291833,
    11.5494828, 15.4347125, 13.3401303, 9.99319537, 12.2525589, 15.1820357,
    14.5485418, 13.9113761, 18.0346287, 12.6224024, 15.4164037, 9.01181645,
    12.4283246, 8.57972035, 7.19920079, 11.8094757, 11.4322998, 10.8866879,
    6.15191168, 14.7902289, 18.8329092, 21.5353558, 13.9003949, 13.7795551,
    11.1137264, 11.4359633, 12.0145077, 13.592801, 17.5366175, 16.3282055,
    15.3065506, 9.06307156, 19.2320495, 14.4936193, 15.3504852, 14.7462885,
    15.9656727, 20.1987838, 24.8273657, 21.403531, 16.4636903, 16.7383307,
    18.4850362, 22.8829206, 22.2713895, 20.0632992, 14.5229113
]) / 100  # Convert to fractions

# Generate the matrix
matrix = np.zeros((rows, cols), dtype=int)

# Populate each column with the desired percentage of ones
for j in range(cols):
    ones_count = int(rows * percentages_ones[j])  # Column-specific number of ones
    ones_indices = np.random.choice(rows, ones_count, replace=False)
    matrix[ones_indices, j] = 1

# Convert to DataFrame
df = pd.DataFrame(matrix)

# Save to Excel file
df.to_excel("random_binary_matrix_broad_distribution.xlsx", index=False, header=False)

print("File saved as 'random_binary_matrix_broad_distribution.xlsx'")

