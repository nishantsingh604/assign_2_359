COMP 359 – Closest Pair of Points Visualization Project

Team Members and Responsibilities

Krishna
Implemented data_generation.py
Responsible for generating random points, sorting them by x-coordinate, splitting into halves, and providing basic statistics.

Dhananjay 
Implemented closest_pair_algorithms.py
Responsible for implementing the closest pair algorithm including:
- brute force search on left and right halves
- delta computation
- strip construction
- strip comparison (up to 7 neighboring points)
- determining overall closest pair

Japneet
Implemented visualization_elements.py
Responsible for creating all matplotlib visualization components including:
- plotting points
- visualizing left and right halves
- strip region
- division line and delta boundaries
- highlighting closest pairs

Nishant
Implemented main_visualization.py
Responsible for coordinating the full pipeline:
- preparing data
- running the algorithm
- generating visualization
- verifying results
- executing the complete workflow


Project Overview

This project visualizes the Closest Pair of Points problem using a structured modular approach. The dataset is generated and sorted, split into two halves, and analyzed using a brute force plus strip-based optimization method. The results are then visualized to clearly illustrate the algorithm’s behavior.


Algorithm Explanation (closest_pair_algorithms.py)

1. Points are sorted by x-coordinate.
2. The dataset is divided into left and right halves.
3. Brute force is applied independently to both halves.
4. Delta is computed as the minimum distance from the two halves.
5. A strip of width 2 * delta is constructed around the dividing line.
6. Points inside the strip are sorted by y-coordinate.
7. Each point in the strip is compared to at most the next 7 points.
8. The final closest pair is selected from left, right, and strip results.


Time Complexity Analysis

Brute force on n points has time complexity O(n²).

Since both halves are solved using brute force:
Left half: O((n/2)²)
Right half: O((n/2)²)

The strip comparison step is linear after sorting.

Therefore, the worst-case time complexity of this implementation remains O(n²).

This project demonstrates the strip optimization technique, though it is not the fully recursive O(n log n) divide-and-conquer implementation.


References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. Introduction to Algorithms. MIT Press.

Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357–362.

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90–95.
