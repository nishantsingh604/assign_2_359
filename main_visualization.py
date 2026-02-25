import numpy as np
from data_generation import PointDataGenerator
from closest_pair_algorithms import ClosestPairFinder
from visualization_elements import VisualizationElements

class ClosestPairVisualizer:
   
    def __init__(self, n_points=30, seed=42):
        self.n_points = n_points
        self.seed = seed
        
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
        
        print("Setting up figure...")
        self.viz_elements.create_figure(figsize=(16, 11))
        
        print("Plotting background elements...")
        self._plot_background_elements()
        
        print("Drawing algorithm-specific elements...")
        self._draw_algorithm_elements()
        
        print("Adding annotations...")
        self._add_annotations(show_labels, show_boxes)
        
        print("\n✓ Visualization created successfully!")
        
    def _plot_background_elements(self):
        self.viz_elements.plot_half_points(self.left_half, half_name='left')
        self.viz_elements.plot_half_points(self.right_half, half_name='right')
        
        self.viz_elements.plot_all_points(self.points_sorted)
        
        self.viz_elements.draw_division_line(self.mid_x)
        
        print("  - Background elements complete")
        
    def _draw_algorithm_elements(self):
        y_min, y_max = np.min(self.points[:, 1]), np.max(self.points[:, 1])
        
        strip_left, strip_right = self.viz_elements.draw_delta_boundaries(
            self.mid_x, self.results['delta'], y_min, y_max
        )
        
        self.viz_elements.draw_strip_rectangle(
            strip_left, strip_right, y_min, y_max, self.results['delta']
        )
        
        if self.results['left_pair']:
            self.viz_elements.draw_pair_connection(
                self.results['left_pair'], 
                self.viz_elements.colors['left_pair'],
                linewidth=2, alpha=0.7,
                label=f"Left half closest (δL={self.results['left_dist']:.3f})"
            )
            self.viz_elements.highlight_points(
                self.results['left_pair'], 
                self.viz_elements.colors['left_pair'],
                marker='*', size=150
            )
        
        if self.results['right_pair']:
            self.viz_elements.draw_pair_connection(
                self.results['right_pair'], 
                self.viz_elements.colors['right_pair'],
                linewidth=2, alpha=0.7,
                label=f"Right half closest (δR={self.results['right_dist']:.3f})"
            )
            self.viz_elements.highlight_points(
                self.results['right_pair'], 
                self.viz_elements.colors['right_pair'],
                marker='*', size=150
            )
        
        if self.results['overall_pair']:
            color = (self.viz_elements.colors['overall_pair'] if self.results['cross_case'] 
                    else (self.viz_elements.colors['left_pair'] 
                          if self.results['overall_pair'] == self.results['left_pair'] 
                          else self.viz_elements.colors['right_pair']))
            
            line_style = '-' if self.results['cross_case'] else '--'
            label_text = f"Overall closest pair (δ={self.results['overall_dist']:.3f})"
            if self.results['cross_case']:
                label_text += " - CROSS CASE!"
            
            self.viz_elements.draw_pair_connection(
                self.results['overall_pair'],
                color, linewidth=3, linestyle=line_style, alpha=0.9,
                label=label_text
            )
            self.viz_elements.highlight_points(
                self.results['overall_pair'],
                color, marker='D', size=200, edgecolors='black', linewidth=2
            )
        
        print("  - Algorithm elements complete")
        
    def _add_annotations(self, show_labels, show_boxes):
        if show_boxes and len(self.results['strip_points']) > 0:
            self.viz_elements.draw_comparison_boxes(
                self.results['strip_points'], 
                self.results['delta'],
                frequency=3
            )
            print("  - Comparison boxes added")
        
        if show_labels:
            self.viz_elements.add_point_labels(self.points_sorted)
            print("  - Point labels added")
        
        textstr = f'δ = min(δL, δR) = {self.results["delta"]:.3f}\n'
        textstr += f'Points in strip: {len(self.results["strip_points"])}\n'
        textstr += f'Strip min distance: {self.results["strip_dist"]:.3f}\n'
        textstr += f'Overall min distance: {self.results["overall_dist"]:.3f}\n'
        textstr += f'Cross-boundary pair: {self.results["cross_case"]}'
        
        self.viz_elements.add_text_box(textstr)
        print("  - Information text box added")
        
        title = 'Closest Pair of Points - Final Merge Step Visualization\n'
        title += '(Similar to Week 6 Fig 5.7, Slide 65)'
        self.viz_elements.customize_plot(title)
        print("  - Final plot customizations applied")
    
    def save_and_show(self, filename='closest_pair_final.png'):
        print(f"\nSaving visualization as '{filename}'...")
        self.viz_elements.save_plot(filename)
        self.viz_elements.show_plot()
        print(f"✓ Visualization saved as '{filename}'")
    
    def verify_result(self):
        print("\n" + "-" * 40)
        print("STEP 4: VERIFYING RESULTS")
        print("-" * 40)
        
        from closest_pair_algorithms import ClosestPairFinder
        
        temp_finder = ClosestPairFinder(self.points)
        full_pair, full_dist = temp_finder.brute_force_closest_pair(self.points)
        
        print(f"Algorithm result distance: {self.results['overall_dist']:.6f}")
        print(f"Full brute force distance: {full_dist:.6f}")
        
        if abs(full_dist - self.results['overall_dist']) < 1e-10:
            print("✓ SUCCESS: Algorithm correctly identified the closest pair!")
            return True
        else:
            print("✗ ERROR: Algorithm result doesn't match brute force")
            return False
    
    def run_complete_pipeline(self, save_filename='closest_pair_final.png'):
        print("=" * 60)
        print("CLOSEST PAIR OF POINTS - FINAL MERGE VISUALIZATION")
        print("=" * 60)
        
        self.prepare_data()
        self.run_algorithm()
        self.create_visualization(show_labels=True, show_boxes=True)
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
    print(f"  - Cross-boundary case: {results['cross_case']}")

if __name__ == "__main__":
    main()