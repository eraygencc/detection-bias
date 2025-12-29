import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits
from astropy.table import Table

class WeightAssigner:
    def __init__(self, catalog_path):
        self.catalog_path = catalog_path
        self.catalog = None
        self.tree = None

    def load_catalog(self):
        """Loads FITS catalog and stores it as an Astropy Table."""
        with fits.open(self.catalog_path) as hdul:
            self.catalog = Table(hdul[1].data)
        print("Catalog loaded with", len(self.catalog), "objects.")

    def build_kdtree(self, x_col="x", y_col="y"):
        """Builds a KD-tree from X and Y positions of the catalog."""
        coords = np.vstack((self.catalog[x_col], self.catalog[y_col])).T
        self.tree = cKDTree(coords)
        print("KDTree built from catalog positions.")

    def calculate_nearest_neighbor_distance(self, index):
        """Returns distance to second nearest neighbor (excluding itself)."""
        point = [self.catalog['x'][index], self.catalog['y'][index]]
        dist, _ = self.tree.query(point, k=2)
        return dist[1]  # first is zero (itself), second is the true neighbor

    def assign_weights(self):
        """Assigns detection weights based on local density (e.g., inverse distance)."""
        weights = []
        for i in range(len(self.catalog)):
            d = self.calculate_nearest_neighbor_distance(i)
            weight = 1.0 / (d + 1e-6)  # avoid division by zero
            weights.append(weight)
        self.catalog["weight"] = weights
        print("Weights assigned.")

    def save_weighted_catalog(self, output_path):
        self.catalog.write(output_path, format="fits", overwrite=True)
        print(f"Weighted catalog saved to {output_path}")
