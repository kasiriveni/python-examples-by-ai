# NumPy Basics
import numpy as np

# Create an array
arr = np.array([1, 2, 3, 4, 5])
print("Array:", arr)

# Perform basic operations
print("Mean:", np.mean(arr))
print("Sum:", np.sum(arr))

# Reshape array
reshaped = arr.reshape((1, 5))
print("Reshaped Array:", reshaped)
