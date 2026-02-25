import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import numpy as np

class VisualizationElements:
    
    def __init__(self):
        self.fig = None
        self.ax = None
        self.colors = {
            'left_half': 'lightblue',
            'right_half': 'lightcoral',
            'strip': 'yellow',
            'division_line': 'black',
            'delta_boundary': 'green',
            'left_pair': 'blue',
            'right_pair': 'red',
            'overall_pair': 'purple',
            'comparison_box': 'orange',
            'points': 'blue',
            'text_bg': 'wheat'
        }
        
    def create_figure(self, figsize=(14, 10)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        return self.fig, self.ax
    
    def plot_all_points(self, points, color='blue', size=50, alpha=0.6, label='All points'):
        self.ax.scatter(points[:, 0], points[:, 1], 
                       c=color, s=size, alpha=alpha, label=label, zorder=2)
    
    def plot_half_points(self, points, half_name='left', alpha=0.3, size=100):
        color = self.colors['left_half'] if half_name == 'left' else self.colors['right_half']
        label = 'Left half' if half_name == 'left' else 'Right half'
        
        self.ax.scatter(points[:, 0], points[:, 1], 
                       c=color, s=size, alpha=alpha, label=label, zorder=1)
    
    def draw_division_line(self, x_coord, linestyle='--', linewidth=2, label='Division line'):
        self.ax.axvline(x=x_coord, color=self.colors['division_line'], 
                       linestyle=linestyle, linewidth=linewidth, label=label, zorder=3)
    
    def draw_delta_boundaries(self, mid_x, delta, y_min, y_max):
        strip_left = mid_x - delta
        strip_right = mid_x + delta
        
        self.ax.axvline(x=strip_left, color=self.colors['delta_boundary'], 
                       linestyle=':', linewidth=1.5, alpha=0.7, 
                       label=f'δ = {delta:.3f} boundary', zorder=3)
        self.ax.axvline(x=strip_right, color=self.colors['delta_boundary'], 
                       linestyle=':', linewidth=1.5, alpha=0.7, zorder=3)
        
        return strip_left, strip_right
    
    def draw_strip_rectangle(self, strip_left, strip_right, y_min, y_max, delta):
        strip_rect = Rectangle(
            (strip_left, y_min - 1), 
            strip_right - strip_left, 
            (y_max - y_min) + 2,
            linewidth=0, 
            facecolor=self.colors['strip'], 
            alpha=0.2,
            label=f'Strip width 2δ = {2*delta:.3f}',
            zorder=0
        )
        self.ax.add_patch(strip_rect)
    
    def draw_pair_connection(self, pair, color, linewidth=2, alpha=0.7, 
                             linestyle='-', label=None, zorder=4):
        if pair:
            self.ax.plot([pair[0][0], pair[1][0]], 
                        [pair[0][1], pair[1][1]], 
                        color=color, linewidth=linewidth, 
                        linestyle=linestyle, alpha=alpha, label=label, zorder=zorder)
    
    def highlight_points(self, points, color, size=150, marker='*', 
                         edgecolors='black', linewidth=1, zorder=5):
        if points:
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            self.ax.scatter(x_coords, y_coords, 
                          c=color, s=size, marker=marker, 
                          edgecolors=edgecolors, linewidth=linewidth, zorder=zorder)
    
    def draw_comparison_boxes(self, strip_points, delta, frequency=3):
        if len(strip_points) > 0:
            strip_sorted = strip_points[np.argsort(strip_points[:, 1])]
            
            for i, point in enumerate(strip_sorted):
                if i % frequency == 0:  
                    y_range_bottom = point[1] - delta
                    y_range_top = point[1] + delta
                    
                    rect = Rectangle(
                        (point[0] - 0.1, y_range_bottom), 
                        0.2, 
                        y_range_top - y_range_bottom,
                        linewidth=1, 
                        edgecolor=self.colors['comparison_box'], 
                        facecolor='none',
                        alpha=0.5,
                        zorder=2
                    )
                    self.ax.add_patch(rect)
                    
                    circle = Circle(
                        (point[0], point[1]),
                        radius=0.05,
                        color=self.colors['comparison_box'],
                        alpha=0.5,
                        zorder=3
                    )
                    self.ax.add_patch(circle)
    
    def add_point_labels(self, points, offset=(5, 5), fontsize=8, alpha=0.7):
        for i, point in enumerate(points):
            self.ax.annotate(f'P{i}', (point[0], point[1]), 
                           xytext=offset, textcoords='offset points', 
                           fontsize=fontsize, alpha=alpha, zorder=6)
    
    def add_text_box(self, text, position=(0.02, 0.98), fontsize=10):
        props = dict(boxstyle='round', facecolor=self.colors['text_bg'], alpha=0.5)
        self.ax.text(position[0], position[1], text, transform=self.ax.transAxes, 
                    fontsize=fontsize, verticalalignment='top', bbox=props, zorder=7)
    
    def customize_plot(self, title, xlabel='X coordinate', ylabel='Y coordinate'):
        self.ax.set_xlabel(xlabel, fontsize=12)
        self.ax.set_ylabel(ylabel, fontsize=12)
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.legend(loc='upper right', fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_aspect('equal')
    
    def save_plot(self, filename='closest_pair_viz.png', dpi=150):
        plt.tight_layout()
        self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Plot saved to {filename}")
    
    def show_plot(self):
        plt.show()

if __name__ == "__main__":
    viz_elements = VisualizationElements()
    viz_elements.create_figure()
    
    dummy_points = np.random.rand(20, 2) * 10
    viz_elements.plot_all_points(dummy_points)
    viz_elements.add_point_labels(dummy_points[:5])
    viz_elements.customize_plot("Test Visualization")
    viz_elements.show_plot()