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