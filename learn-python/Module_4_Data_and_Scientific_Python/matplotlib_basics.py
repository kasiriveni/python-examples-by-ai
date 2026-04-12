# Example: Matplotlib Basics
# Demonstrates basic plotting with Matplotlib

import matplotlib.pyplot as plt

# Data for plotting
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 35]

# Create a line plot
plt.plot(x, y, label="Line 1", color="blue", marker="o")

# Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Basic Line Plot")
plt.legend()

# Show the plot
plt.show()