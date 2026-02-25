import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import numpy as np

class VisualizationElements:
    
    def __init__(self):
        self.fig = None
        self.ax = None
         self.colors = {
            'left_half': 'lightblue',
            'right_half': 'lightcoral',
            'division_line': 'black',
            'strip': 'yellow',
            'delta_boundary': 'green',
            'left_pair': 'blue',
            'right_pair': 'red',
            'overall_pair': 'purple',
            'comparison_box': 'orange',
            'text_bg': 'wheat'
        }
            def create_figure(self, figsize=(12, 8)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        return self.fig, self.ax

            def plot_all_points(self, points):
        self.ax.scatter(points[:, 0], points[:, 1],
                        c='blue', s=50, alpha=0.6, label="All Points")

    def plot_half_points(self, points, half_name='left'):
        color = self.colors['left_half'] if half_name == 'left' else self.colors['right_half']
        label = "Left Half" if half_name == 'left' else "Right Half"
        self.ax.scatter(points[:, 0], points[:, 1],
                       c=color, s=size, alpha=alpha, label=label, zorder=1)

                           def draw_division_line(self, x_coord, linestyle='--', linewidth=2, label='Division line'):
        self.ax.axvline(x=x_coord,
                        color=self.colors['division_line'],
                        linestyle=linestyle,
                        linewidth=linewidth,
                        label=label,
                        zorder=3)

    def draw_delta_boundaries(self, mid_x, delta):
        strip_left = mid_x - delta
        strip_right = mid_x + delta

        self.ax.axvline(x=strip_left,
                        color=self.colors['delta_boundary'],
                        linestyle=':',
                        linewidth=1.5,
                        alpha=0.7)

        self.ax.axvline(x=strip_right,
                        color=self.colors['delta_boundary'],
                        linestyle=':',
                        linewidth=1.5,
                        alpha=0.7)

        return strip_left, strip_right

