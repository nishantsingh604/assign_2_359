import numpy as np
import random


class PointDataGenerator:
    """Class to handle point generation and basic operations"""

    def __init__(self, n_points=30, seed=42):
        self.n_points = n_points
        self.seed = seed
        self.points = None
        self.points_sorted = None

    def generate_random_points(self):
        random.seed(self.seed)
        np.random.seed(self.seed)
        self.points = np.random.rand(self.n_points, 2) * 10
        return self.points

    def sort_points_by_x(self):
        if self.points is None:
            self.generate_random_points()
        self.points_sorted = self.points[np.argsort(self.points[:, 0])]
        return self.points_sorted

    def split_halves(self):
        if self.points_sorted is None:
            self.sort_points_by_x()
        mid = len(self.points_sorted) // 2
        left_half = self.points_sorted[:mid]
        right_half = self.points_sorted[mid:]
        return left_half, right_half, mid

    def get_point_statistics(self):
        if self.points is None:
            self.generate_random_points()

        stats = {
            "total_points": len(self.points),
            "x_range": (np.min(self.points[:, 0]), np.max(self.points[:, 0])),
            "y_range": (np.min(self.points[:, 1]), np.max(self.points[:, 1])),
            "centroid": np.mean(self.points, axis=0),
        }
        return stats

    def save_points_to_file(self, filename="points_data.npy"):
        if self.points is None:
            self.generate_random_points()
        np.save(filename, self.points)
        print(f"Points saved to {filename}")

    def load_points_from_file(self, filename="points_data.npy"):
        self.points = np.load(filename)
        self.points_sorted = None
        print(f"Points loaded from {filename}")
        return self.points