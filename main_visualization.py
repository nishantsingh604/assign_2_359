import numpy as np
from data_generation import PointDataGenerator
from closest_pair_algorithms import ClosestPairFinder
from visualization_elements import VisualizationElements

class ClosestPairVisualizer:
    def __init__(self, n_points=30, seed=42):
        self.n_points = n_points
        self.seed = seed
        
        # Initialize components from other modules
        self.data_generator = PointDataGenerator(n_points, seed)
        self.finder = ClosestPairFinder()
        self.viz_elements = VisualizationElements()
        
        self.points = None
        self.points_sorted = None
        self.left_half = None
        self.right_half = None
        self.mid_idx = None
        self.mid_x = None
        self.results = None
        
        print(f"ClosestPairVisualizer initialized with {n_points} points, seed={seed}")
        
    def prepare_data(self):
        print("\n" + "-" * 40)
        print("STEP 1: PREPARING DATA")
        print("-" * 40)
        
        print("Generating random points...")
        self.points = self.data_generator.generate_random_points()
        
        print("Sorting points by x-coordinate...")
        self.points_sorted = self.data_generator.sort_points_by_x()
        
        print("Splitting into left and right halves...")
        self.left_half, self.right_half, self.mid_idx = self.data_generator.split_halves()
        
        self._calculate_midline()
        
        stats = self.data_generator.get_point_statistics()
        print(f"\nData Statistics:")
        print(f"  - Total points: {stats['total_points']}")
        print(f"  - X range: [{stats['x_range'][0]:.2f}, {stats['x_range'][1]:.2f}]")
        print(f"  - Y range: [{stats['y_range'][0]:.2f}, {stats['y_range'][1]:.2f}]")
        print(f"  - Left half: {len(self.left_half)} points")
        print(f"  - Right half: {len(self.right_half)} points")
        print(f"  - Midline at x = {self.mid_x:.4f}")
        
        print("\n✓ Data preparation complete!")
        
    def _calculate_midline(self):
        if self.mid_idx is not None and self.points_sorted is not None:
            self.mid_x = (self.points_sorted[self.mid_idx-1][0] + 
                         self.points_sorted[self.mid_idx][0]) / 2
    
    def run_algorithm(self):
        print("\n" + "-" * 40)
        print("STEP 2: RUNNING CLOSEST PAIR ALGORITHM")
        print("-" * 40)
        
        print("Initializing algorithm with point data...")
        self.finder.set_points(self.points)
        
        print("Finding closest pairs in left and right halves...")
        print("Calculating delta and analyzing strip...")
        print("Determining overall closest pair...")
        
        self.results = self.finder.run_full_analysis(
            self.points_sorted, 
            self.left_half, 
            self.right_half, 
            self.mid_x
        )
        
        print(f"\nAlgorithm Results:")
        print(f"  - Left half closest distance: {self.results['left_dist']:.4f}")
        print(f"  - Right half closest distance: {self.results['right_dist']:.4f}")
        print(f"  - Delta (min of halves): {self.results['delta']:.4f}")
        print(f"  - Points in strip: {len(self.results['strip_points'])}")
        print(f"  - Strip minimum distance: {self.results['strip_dist']:.4f}")
        print(f"  - Overall minimum distance: {self.results['overall_dist']:.4f}")
        print(f"  - Cross-boundary case: {self.results['cross_case']}")
        
        print("\n✓ Algorithm complete!")
        return self.results
    
    def create_visualization(self, show_labels=True, show_boxes=True):
        print("\n" + "-" * 40)
        print("STEP 3: CREATING VISUALIZATION")
        print("-" * 40)
        
        # Will be implemented in next commit
        print("Visualization components will be added here...")
        pass
    
    def save_and_show(self, filename='closest_pair_final.png'):
        print(f"\nSaving visualization as '{filename}'...")
        # Will be implemented in next commit
        pass
    
    def verify_result(self):
        print("\n" + "-" * 40)
        print("STEP 4: VERIFYING RESULTS")
        print("-" * 40)
        
        # Will be implemented in next commit
        pass
    
    def run_complete_pipeline(self, save_filename='closest_pair_final.png'):
        print("=" * 60)
        print("CLOSEST PAIR OF POINTS - FINAL MERGE VISUALIZATION")
        print("=" * 60)
        
        self.prepare_data()
        self.run_algorithm()
        self.create_visualization()
        self.save_and_show(save_filename)
        self.verify_result()
        
        return self.results

def main():
    visualizer = ClosestPairVisualizer(n_points=30, seed=42)
    results = visualizer.run_complete_pipeline('closest_pair_final.png')

    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"✓ Visualization pipeline completed successfully!")
    print(f"  - Output file: closest_pair_final.png")
    print(f"  - Overall min distance: {results['overall_dist']:.4f}")

if __name__ == "__main__":
    main()