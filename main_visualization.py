import numpy as np
import logging
from typing import Optional, Dict, Any, Tuple
from data_generation import PointDataGenerator
from closest_pair_algorithms import ClosestPairFinder
from visualization_elements import VisualizationElements

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClosestPairVisualizer:
    
    def __init__(self, n_points: int = 30, seed: int = 42):
        self.n_points = n_points
        self.seed = seed
        
        logger.info(f"Initializing ClosestPairVisualizer with {n_points} points, seed={seed}")
        
        try:
            self.data_generator = PointDataGenerator(n_points, seed)
            self.finder = ClosestPairFinder()
            self.viz_elements = VisualizationElements()
            logger.debug("All modules initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize modules: {e}")
            raise
        
        self.points: Optional[np.ndarray] = None
        self.points_sorted: Optional[np.ndarray] = None
        self.left_half: Optional[np.ndarray] = None
        self.right_half: Optional[np.ndarray] = None
        self.mid_idx: Optional[int] = None
        self.mid_x: Optional[float] = None
        self.results: Optional[Dict[str, Any]] = None
        
    def prepare_data(self) -> None:
        logger.info("Step 1: Preparing data")
        
        try:
            logger.debug("Generating random points...")
            self.points = self.data_generator.generate_random_points()
            
            logger.debug("Sorting points by x-coordinate...")
            self.points_sorted = self.data_generator.sort_points_by_x()
            
            logger.debug("Splitting into left and right halves...")
            self.left_half, self.right_half, self.mid_idx = self.data_generator.split_halves()
            
            self._calculate_midline()
            
            stats = self.data_generator.get_point_statistics()
            logger.info(f"Data Statistics:")
            logger.info(f"  - Total points: {stats['total_points']}")
            logger.info(f"  - X range: [{stats['x_range'][0]:.2f}, {stats['x_range'][1]:.2f}]")
            logger.info(f"  - Y range: [{stats['y_range'][0]:.2f}, {stats['y_range'][1]:.2f}]")
            logger.info(f"  - Left half: {len(self.left_half)} points")
            logger.info(f"  - Right half: {len(self.right_half)} points")
            logger.info(f"  - Midline at x = {self.mid_x:.4f}")
            
            logger.info("✓ Data preparation complete")
            
        except Exception as e:
            logger.error(f"Data preparation failed: {e}")
            raise
        
    def _calculate_midline(self) -> None:
        if self.mid_idx is not None and self.points_sorted is not None:
            self.mid_x = (self.points_sorted[self.mid_idx-1][0] + 
                         self.points_sorted[self.mid_idx][0]) / 2
            logger.debug(f"Calculated midline at x = {self.mid_x:.4f}")
    
    def run_algorithm(self) -> Dict[str, Any]:
        logger.info("Step 2: Running closest pair algorithm")
        
        try:
            logger.debug("Initializing algorithm with point data...")
            self.finder.set_points(self.points)
            
            logger.debug("Finding closest pairs in left and right halves...")
            logger.debug("Calculating delta and analyzing strip...")
            
            self.results = self.finder.run_full_analysis(
                self.points_sorted, 
                self.left_half, 
                self.right_half, 
                self.mid_x
            )
            
            logger.info(f"Algorithm Results:")
            logger.info(f"  - Left half closest distance: {self.results['left_dist']:.4f}")
            logger.info(f"  - Right half closest distance: {self.results['right_dist']:.4f}")
            logger.info(f"  - Delta (min of halves): {self.results['delta']:.4f}")
            logger.info(f"  - Points in strip: {len(self.results['strip_points'])}")
            logger.info(f"  - Strip minimum distance: {self.results['strip_dist']:.4f}")
            logger.info(f"  - Overall minimum distance: {self.results['overall_dist']:.4f}")
            logger.info(f"  - Cross-boundary case: {self.results['cross_case']}")
            
            logger.info("✓ Algorithm complete")
            return self.results
            
        except Exception as e:
            logger.error(f"Algorithm execution failed: {e}")
            raise
    
    def create_visualization(self, show_labels: bool = True, show_boxes: bool = True) -> None:
        logger.info("Step 3: Creating visualization")
        
        try:
            logger.debug("Setting up figure...")
            self.viz_elements.create_figure(figsize=(16, 11))
            
            logger.debug("Plotting background elements...")
            self._plot_background_elements()
            
            logger.debug("Drawing algorithm-specific elements...")
            self._draw_algorithm_elements()
            
            logger.debug("Adding annotations...")
            self._add_annotations(show_labels, show_boxes)
            
            logger.info("✓ Visualization created successfully")
            
        except Exception as e:
            logger.error(f"Visualization creation failed: {e}")
            raise
        
    def _plot_background_elements(self) -> None:
        self.viz_elements.plot_half_points(self.left_half, half_name='left')
        self.viz_elements.plot_half_points(self.right_half, half_name='right')
        
        self.viz_elements.plot_all_points(self.points_sorted)
        
        self.viz_elements.draw_division_line(self.mid_x)
        
        logger.debug("Background elements complete")
        
    def _draw_algorithm_elements(self) -> None:
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
        
        logger.debug("Algorithm elements complete")
        
    def _add_annotations(self, show_labels: bool, show_boxes: bool) -> None:
        if show_boxes and len(self.results['strip_points']) > 0:
            self.viz_elements.draw_comparison_boxes(
                self.results['strip_points'], 
                self.results['delta'],
                frequency=3
            )
            logger.debug("Comparison boxes added")
        
        if show_labels:
            self.viz_elements.add_point_labels(self.points_sorted)
            logger.debug("Point labels added")
        
        textstr = f'δ = min(δL, δR) = {self.results["delta"]:.3f}\n'
        textstr += f'Points in strip: {len(self.results["strip_points"])}\n'
        textstr += f'Strip min distance: {self.results["strip_dist"]:.3f}\n'
        textstr += f'Overall min distance: {self.results["overall_dist"]:.3f}\n'
        textstr += f'Cross-boundary pair: {self.results["cross_case"]}'
        
        self.viz_elements.add_text_box(textstr)
        logger.debug("Information text box added")
        
        title = 'Closest Pair of Points - Final Merge Step Visualization\n'
        title += '(Similar to Week 6 Fig 5.7, Slide 65)'
        self.viz_elements.customize_plot(title)
        logger.debug("Final plot customizations applied")
    
    def save_and_show(self, filename: str = 'closest_pair_final.png') -> None:
        logger.info(f"Saving visualization as '{filename}'...")
        
        try:
            self.viz_elements.save_plot(filename)
            self.viz_elements.show_plot()
            logger.info(f"✓ Visualization saved as '{filename}'")
        except Exception as e:
            logger.error(f"Failed to save visualization: {e}")
            raise
    
    def verify_result(self) -> bool:
        logger.info("Step 4: Verifying results")
        
        try:
            from closest_pair_algorithms import ClosestPairFinder
            
            temp_finder = ClosestPairFinder(self.points)
            full_pair, full_dist = temp_finder.brute_force_closest_pair(self.points)
            
            logger.info(f"Algorithm result distance: {self.results['overall_dist']:.6f}")
            logger.info(f"Full brute force distance: {full_dist:.6f}")
            
            if abs(full_dist - self.results['overall_dist']) < 1e-10:
                logger.info("✓ SUCCESS: Algorithm correctly identified the closest pair!")
                return True
            else:
                logger.warning("✗ ERROR: Algorithm result doesn't match brute force")
                return False
                
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False
    
    def print_summary(self) -> None:
        if not self.results:
            logger.warning("No results to summarize")
            return
            
        summary = f"""
{'='*60}
FINAL SUMMARY
{'='*60}
Configuration:
  - Total points: {self.n_points}
  - Random seed: {self.seed}

Results:
  - Left half closest distance: {self.results['left_dist']:.4f}
  - Right half closest distance: {self.results['right_dist']:.4f}
  - Delta (min of halves): {self.results['delta']:.4f}
  - Points in strip: {len(self.results['strip_points'])}
  - Strip minimum distance: {self.results['strip_dist']:.4f}
  - Overall minimum distance: {self.results['overall_dist']:.4f}
  - Cross-boundary closest pair: {self.results['cross_case']}

Output:
  - Visualization file: closest_pair_final.png

Status:
  - ✓ Pipeline completed successfully
{'='*60}
"""
        print(summary)
    
    def run_complete_pipeline(self, save_filename: str = 'closest_pair_final.png',
                             show_labels: bool = True, 
                             show_boxes: bool = True) -> Optional[Dict[str, Any]]:
        logger.info("=" * 60)
        logger.info("CLOSEST PAIR OF POINTS - FINAL MERGE VISUALIZATION")
        logger.info("=" * 60)
        
        try:
            self.prepare_data()
            self.run_algorithm()
            self.create_visualization(show_labels, show_boxes)
            self.save_and_show(save_filename)
            self.verify_result()
            self.print_summary()
            
            return self.results
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return None

def main():
    visualizer = ClosestPairVisualizer(n_points=30, seed=42)
    
    results = visualizer.run_complete_pipeline(
        save_filename='closest_pair_final.png',
        show_labels=True,
        show_boxes=True
    )
    
    if results is None:
        logger.error("Visualization pipeline failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)