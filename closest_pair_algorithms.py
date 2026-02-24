import numpy as np

class ClosestPairFinder:
    def __init__(self, points=None):
        self.points = points
        self.left_pair = None
        self.right_pair = None
        self.strip_pair = None
        self.overall_pair = None

        self.left_dist = float("inf")
        self.right_dist = float("inf")
        self.strip_dist = float("inf")
        self.overall_dist = float("inf")

        self.delta = float("inf")
        self.mid_x = None
        self.strip_points = None

    def set_points(self, points):
        self.points = points

    def brute_force_closest_pair(self, points):
        if points is None or len(points) < 2:
            return None, float("inf")

        min_dist = float("inf")
        closest_pair = None

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = np.linalg.norm(points[i] - points[j])
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (points[i], points[j])

        return closest_pair, min_dist

    def find_halves_closest_pairs(self, left_half, right_half):
        self.left_pair, self.left_dist = self.brute_force_closest_pair(left_half)
        self.right_pair, self.right_dist = self.brute_force_closest_pair(right_half)
        return self.left_pair, self.right_pair

    def calculate_delta(self):
        self.delta = min(self.left_dist, self.right_dist)
        return self.delta

    def find_strip_points(self, points_sorted, mid_x):
        self.mid_x = mid_x
        left_bound = mid_x - self.delta
        right_bound = mid_x + self.delta

        mask = (points_sorted[:, 0] >= left_bound) & (points_sorted[:, 0] <= right_bound)
        self.strip_points = points_sorted[mask]
        return self.strip_points

    def find_closest_in_strip(self):
        if self.strip_points is None or len(self.strip_points) < 2:
            self.strip_dist = self.delta
            self.strip_pair = None
            return None, self.delta

        strip_sorted = self.strip_points[np.argsort(self.strip_points[:, 1])]
        self.strip_dist = self.delta
        self.strip_pair = None

        for i in range(len(strip_sorted)):
            for j in range(i + 1, min(i + 8, len(strip_sorted))):
                dist = np.linalg.norm(strip_sorted[i] - strip_sorted[j])
                if dist < self.strip_dist:
                    self.strip_dist = dist
                    self.strip_pair = (strip_sorted[i], strip_sorted[j])

        return self.strip_pair, self.strip_dist

    def determine_overall_closest(self):
        if self.strip_dist < self.delta:
            self.overall_pair = self.strip_pair
            self.overall_dist = self.strip_dist
            cross_case = True
        else:
            if self.left_dist <= self.right_dist:
                self.overall_pair = self.left_pair
                self.overall_dist = self.left_dist
            else:
                self.overall_pair = self.right_pair
                self.overall_dist = self.right_dist
            cross_case = False

        return self.overall_pair, self.overall_dist, cross_case

    def run_full_analysis(self, points):
        points = np.array(points, dtype=float)
        if len(points) < 2:
            self.overall_pair = None
            self.overall_dist = float("inf")
            return None, float("inf"), False

        points_sorted = points[np.argsort(points[:, 0])]
        mid = len(points_sorted) // 2
        left_half = points_sorted[:mid]
        right_half = points_sorted[mid:]
        mid_x = points_sorted[mid][0]

        self.find_halves_closest_pairs(left_half, right_half)
        self.calculate_delta()
        self.find_strip_points(points_sorted, mid_x)
        self.find_closest_in_strip()

        return self.determine_overall_closest()
