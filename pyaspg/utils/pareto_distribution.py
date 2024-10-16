import numpy as np

# Function to generate and normalize Pareto distribution for 5 classes
def distribute_pareto(alpha, num_classes):
    classes = np.arange(1, num_classes + 1)  # Class numbers 1 to 5
    # Pareto distribution formula
    distribution = (classes ** -alpha)
    normalized_distribution = distribution / np.sum(distribution)  # Normalize to sum to 1
    return normalized_distribution
