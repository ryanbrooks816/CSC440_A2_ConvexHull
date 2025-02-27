import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from benchmarks import run_benchmarks

def get_data_points():
    """Returns tuples of (n, t) data points."""
    return run_benchmarks()

# Define functions for different complexities
def linear(x, a, b): return a * x + b
def nlogn(x, a, b): 
    if 0 in x:
        x = np.array([i if i != 0 else 1 for i in x])
    return a * x * np.log2(x) + b
def quadratic(x, a, b): return a * x**2 + b
def cubic(x, a, b): return a * x**3 + b

def plot_complexities(complexities):
    """Plots the input size vs running time for given complexity functions."""
    n, t = get_data_points()
    n_fit = np.linspace(min(n), max(n), 100)

    for label, func in complexities.items():
        params, _ = curve_fit(func, n, t)
        a, b = params
        residuals = t - func(n, a, b)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((t - np.mean(t))**2)
        r_squared = 1 - (ss_res / ss_tot)

        plt.figure(figsize=(6, 4))
        plt.scatter(n, t, label="Observed Times", color='black')
        plt.plot(n_fit, func(n_fit, a, b), '--', label=f"{label} Fit (R²={r_squared:.4f})", color='blue')

        plt.xlabel("Input Size (n)")
        plt.ylabel("Running Time")
        plt.title(f"Naive Run Times vs. {label} Growth")
        plt.legend()

        # Set x-axis ticks to be integers
        plt.xticks(np.arange(min(n), max(n) + 1, step=max(1, (max(n) - min(n)) // 10)))

        plt.show()
        plt.close()
        
# Define the complexity functions to analyze
complexities = {
    "O(n)": linear,
    "O(n log n)": nlogn,
    "O(n²)": quadratic,
    # "O(n³)": cubic
}

# Plot the complexities
plot_complexities(complexities)
