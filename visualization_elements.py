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
                        c=color, s=100, alpha=0.3, label=label)