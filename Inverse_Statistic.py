# %% [markdown]
# # Introduction to the Problem: Analyzing Waiting Times for Gold Price Movements
# 
# ### Problem Statement:
# We aim to analyze gold price movements using a time-series dataset sampled at 1-minute intervals.
# Specifically, the goal is to determine the waiting time required for the price to either increase or decrease
# by a specified amount (e.g., $5, $10, $20) relative to the current price.
# 
# #### Steps Involved:
# 1. **Data Processing**:
#    - Load the gold price dataset from a text file.
#    - Extract the price information into a usable format for analysis.
# 
# 2. **Waiting Time Calculation**:
#    - For each price point in the dataset:
#      - Calculate the time it takes for the price to increase by a given increment.
#      - Similarly, calculate the time it takes for the price to decrease by the same increment.
#    - If the condition is not met within the dataset, mark the waiting time as infinity.
# 
# 3. **Visualization**:
#    - Visualize the waiting times for each increment and direction using bar plots.
#    - Analyze the distribution of waiting times using histograms.
#    - Analyze the scatter plots of the Emperical PDFs for the waiting times
# 
# 
# #### Example:
# Suppose the current price is $1800, and the increment is $10:
# - If the price reaches $1810 in 3 minutes, the waiting time for an increase is 3 minutes.
# - If the price drops to $1790 in 7 minutes, the waiting time for a decrease is 7 minutes.
# 
# #### Usage:
# - This analysis can help traders and investors understand how long they might need to wait for significant price changes.
# - It provides insights into market volatility and price dynamics over time.
# 
# #### Dataset Requirements:
# - The dataset should contain gold prices sampled at 1-minute intervals in plain text format,
#   where each line contains the price for a specific time.
# 
# **Output**:
# The analysis will produce:
# 1. Bar plots showing the waiting times for each price increment and direction.
# 2. Histograms depicting the distribution of waiting times for both increases and decreases.
# 
# 

# %% [markdown]
# ### Importing Libraries and Loading Gold Price Data
# 
# This cell performs the following steps:
# 
# 1. **Import Libraries**:
#    - `numpy` is imported as `np` for numerical operations.
#    - `matplotlib.pyplot` is imported as `plt` for data visualization (to be used later).
# 
# 2. **Define File Path**:
#    - The file path to the gold price data (`Gold_TimeWindow_1min.txt`) is specified. This file contains time-series data for gold prices sampled at 1-minute intervals.
# 
# 3. **Read and Process File**:
#    - The file is opened and read line by line using the `with open` statement for efficient file handling.
#    - Each line is processed to extract the gold price (assumed to be the first value in each line). These prices are converted to floating-point numbers and stored in a list.
# 
# 4. **Convert Prices to Numpy Array**:
#    - The list of prices is converted to a `numpy` array for optimized numerical computations.
# 
# **Output**: The `prices` variable contains an array of gold prices sampled at 1-minute intervals.

# %%
import numpy as np
import matplotlib.pyplot as plt

file_path = r"YOUR FILE PATH"

with open(file_path, 'r') as file:
    lines = file.readlines()

prices = [float(line.split()[0]) for line in lines]
prices = np.array(prices)

# %% [markdown]
# ### Generalized Function to Calculate Waiting Times for Price Increases and Decreases
# 
# This cell defines a generalized function to calculate the waiting times required for gold prices to reach a specified increment above or below the current price.
# 
# #### Function Definition: `calculate_waiting_times_both_directions`
# - **Purpose**:
#   This function calculates the waiting time for both price increases and decreases, given a set of price increments.
# 
# - **Parameters**:
#   1. `data`: A `numpy` array containing the gold price time-series data.
#   2. `increments`: A list of positive values (e.g., `[5, 10, 20]`) representing the price increments to check.
# 
# - **Returns**:
#   A dictionary with:
#   - Keys: Tuples in the form `(increment, direction)`, where `direction` is either `"increase"` or `"decrease"`.
#   - Values: `numpy` arrays containing the waiting times for each increment and direction.
# 
# #### Logic:
# 1. **Loop Over Increments**:
#    - For each increment in the provided list, calculate waiting times for both price increases and decreases.
# 
# 2. **Waiting Times for Price Increase**:
#    - For each price point in the dataset:
#      - Determine the target price as the current price plus the increment.
#      - Check subsequent prices (`data[i:]`) to see if the target price is reached.
#      - If reached, calculate the waiting time as the index difference. If not, set the waiting time to `infinity`.
# 
# 3. **Waiting Times for Price Decrease**:
#    - Repeat the same process as above, but calculate the target price as the current price minus the increment.
# 
# 4. **Store Results**:
#    - Save the computed waiting times for both increase and decrease in the results dictionary under the corresponding key.
# 
# #### Notes:
# - The function is optimized using `numpy` for element-wise comparisons and logical operations.
# - Waiting times are set to `infinity` if the target condition is not met within the dataset.
# - This function is flexible and can handle multiple increments simultaneously.
# 
# **Output**: A dictionary containing waiting times for both increases and decreases for all specified increments.

# %%
# Generalized function to calculate waiting times for both increase and decrease
def calculate_waiting_times_both_directions(data, increments):
    """
    Calculate waiting times for both increase and decrease for a list of increments.

    Parameters:
    - data: numpy array of prices.
    - increments: list of positive increments (e.g., [5, 10, 20]).

    Returns:
    - A dictionary with keys as tuples (increment, direction) where direction is "increase" or "decrease",
      and values are numpy arrays of waiting times.
    """
    results = {}
    n = len(data)

    for increment in increments:
        # Calculate waiting times for increase
        waiting_times_increase = []
        for i in range(n):
            target = data[i] + increment
            condition = data[i:] >= target
            if np.any(condition):
                waiting_time = np.argmax(condition)
            else:
                waiting_time = np.inf
            waiting_times_increase.append(waiting_time)
        results[(increment, "increase")] = np.array(waiting_times_increase)

        # Calculate waiting times for decrease
        waiting_times_decrease = []
        for i in range(n):
            target = data[i] - increment
            condition = data[i:] <= target
            if np.any(condition):
                waiting_time = np.argmax(condition)
            else:
                waiting_time = np.inf
            waiting_times_decrease.append(waiting_time)
        results[(increment, "decrease")] = np.array(waiting_times_decrease)

    return results

# %% [markdown]
# ### Applying the Function to Gold Price Data
# 
# This cell applies the previously defined `calculate_waiting_times_both_directions` function to a subset of the gold price data.
# 
# #### Steps:
# 1. **Subset the Data**:
#    - A subset of the gold price data (`prices[:125000]`) is selected for analysis.
#    - This ensures that the computation is performed on a manageable dataset size.
# 
# 2. **Define Increments**:
#    - A list of increments (`[5, 10, 20]`) is specified, representing the price changes to analyze:
#      - `5`: A small increment.
#      - `10`: A medium increment.
#      - `20`: A larger increment.
# 
# 3. **Calculate Waiting Times**:
#    - The `calculate_waiting_times_both_directions` function is called with:
#      - `data`: The subset of gold price data.
#      - `increments`: The list of increments.
#    - The function computes the waiting times for both price increases and decreases for each specified increment.
# 
# 4. **Store Results**:
#    - The output is stored in the variable `waiting_times_dict`, which is a dictionary containing the waiting times for each increment and direction.
# 
# #### Notes:
# - Ensure that the subset size (`125000`) is appropriate for the computational resources available.
# - The `waiting_times_dict` can be used for further analysis or visualization in subsequent cells.
# 
# **Output**: A dictionary (`waiting_times_dict`) containing waiting times for the specified increments and directions.
# 

# %%
data = prices[:125000]
increments = [5, 10, 20]  # Example increments
waiting_times_dict = calculate_waiting_times_both_directions(data, increments)

# %% [markdown]
# ### Visualizing the Waiting Times for Each Increment and Direction
# 
# This cell creates bar plots to visualize the minimum waiting times for price increases and decreases for each specified increment.
# 
# #### Steps:
# 1. **Iterate Through Results**:
#    - The `waiting_times_dict` dictionary is iterated over, with each key-value pair representing:
#      - `increment`: The price increment (e.g., 5, 10, 20).
#      - `direction`: The direction of price movement (`"increase"` or `"decrease"`).
#      - `waiting_times`: The array of computed waiting times for the respective increment and direction.
# 
# 2. **Clean the Data**:
#    - Replace `infinity` values (`np.inf`) in the `waiting_times` array with `NaN` using `np.where`. This ensures that these values are excluded from the visualization.
# 
# 3. **Create Bar Plots**:
#    - A bar plot is generated for each combination of increment and direction:
#      - The x-axis represents the time index (data points).
#      - The y-axis represents the waiting time in minutes.
#      - The title indicates the increment and direction being plotted (e.g., "Minimum Waiting Time for Increase by 10").
# 
# 4. **Customize the Plot**:
#    - The bar width is set to `1.0` for clarity.
#    - The bars are styled with a sky-blue color.
#    - Each plot includes labeled axes, a descriptive title, and appropriate scaling.
# 
# 5. **Display the Plots**:
#    - Each plot is displayed using `plt.show()`.
# 
# #### Notes:
# - Large datasets may produce densely packed plots. Consider reducing the dataset size or adjusting the bar width for better visualization.
# - The use of `NaN` ensures that bars for missing or infinite waiting times are omitted.
# 
# **Output**: Bar plots showing the minimum waiting times for price movements (increases and decreases) for each increment.
# 

# %%
# Plot results for each increment and direction
for (increment, direction), waiting_times in waiting_times_dict.items():
    plt.figure(figsize=(10, 6))
    cleaned_times = np.where(waiting_times == np.inf, np.nan, waiting_times)  # Replace inf with NaN for plotting
    plt.bar(range(len(cleaned_times)), cleaned_times, width=1.0, color='skyblue')
    plt.xlabel('Time Index')
    plt.ylabel('Minimum Waiting Time (minutes)')
    plt.title(f'Minimum Waiting Time for {direction.capitalize()} by {increment}')
    plt.show()

# %% [markdown]
# ### Plotting Histograms of Waiting Times for Each Increment and Direction
# 
# This cell generates histograms to visualize the distribution of waiting times for price increases and decreases for each specified increment.
# 
# #### Steps:
# 1. **Iterate Through Results**:
#    - The `waiting_times_dict` dictionary is iterated over, with each key-value pair representing:
#      - `increment`: The price increment (e.g., 5, 10, 20).
#      - `direction`: The direction of price movement (`"increase"` or `"decrease"`).
#      - `waiting_times`: The array of computed waiting times for the respective increment and direction.
# 
# 2. **Clean the Data**:
#    - Replace `infinity` values (`np.inf`) in the `waiting_times` array with `NaN` using `np.where`. This ensures that invalid values are excluded from the histogram.
# 
# 3. **Create Histograms**:
#    - A histogram is plotted for each combination of increment and direction:
#      - The x-axis represents the waiting times in minutes.
#      - The y-axis represents the frequency of waiting times.
#      - The data is binned into `1000` intervals for detailed visualization.
#      - A yellow color is applied to the bars for better distinction.
# 
# 4. **Customize the Plot**:
#    - Each histogram is given:
#      - A descriptive title indicating the increment and direction (e.g., "Minimum Waiting Time for Increase by 10").
#      - Labeled axes for clarity.
#      - An alpha value (`0.7`) for slight transparency to enhance visual appeal.
# 
# 5. **Display the Histograms**:
#    - Each histogram is displayed using `plt.show()`.
# 
# #### Notes:
# - The high number of bins (`1000`) ensures detailed visualization but may need adjustment for datasets with fewer data points.
# - The use of `NaN` excludes infinite waiting times from the histogram, ensuring accurate representation of the data.
# 
# **Output**: Histograms showing the frequency distribution of waiting times for price movements (increases and decreases) for each increment.
# 

# %%
# Plot histograms for each increment
for (increment, direction), waiting_times in waiting_times_dict.items():
    # Create a single figure with histograms for increase and decrease
    plt.figure(figsize=(10, 6))
    cleaned_times = np.where(waiting_times == np.inf, np.nan, waiting_times)  # Replace inf with NaN for plotting
    plt.hist(cleaned_times, bins=1000, alpha=0.7, color='yellow')
    plt.xlabel('Min Waiting Time (minutes)')
    plt.ylabel('Frequency')
    plt.title(f'Minimum Waiting Time for {direction.capitalize()} by {increment}')
    plt.show()

# %% [markdown]
# ### Plotting Emperical Probability Density Functions (PDFs) of Waiting Times for Each Increment and Direction
# 
# This cell generates and visualizes the probability density functions (PDFs) of waiting times for price increases and decreases, broken down by increment.
# 
# #### Steps:
# 1. **Iterate Through Increments**:
#    - The code iterates through unique `increments` present in the `waiting_times_dict`, extracting the corresponding waiting times for both `"increase"` and `"decrease"` directions for each increment.
#    - For each increment, the waiting times are fetched using the dictionary keys `(increment, "increase")` and `(increment, "decrease")`.
# 
# 2. **Clean the Data**:
#    - The waiting times arrays for both directions are cleaned by removing `NaN` and `infinity` values using `np.isfinite`. This ensures that only valid waiting times are used in the subsequent analysis.
# 
# 3. **Calculate Histograms and Normalize to PDFs**:
#    - For both directions, histograms are calculated using `np.histogram`, with the `density=True` parameter to normalize the histogram into a probability density function (PDF).
#    - The histograms are computed with 1000 bins for fine-grained results.
#    - The bin edges are then used to calculate the bin centers for plotting purposes.
# 
# 4. **Plot the PDFs**:
#    - The histograms for the `"increase"` and `"decrease"` directions are plotted as scatter plots.
#    - The `increase` direction is represented by blue circles (`'o'`), while the `decrease` direction is represented by red crosses (`'x'`).
#    - The areas under the curves are filled with semi-transparent colors (blue for increase, red for decrease) to improve visibility.
# 
# 5. **Customize the Plot**:
#    - Labels are added to the x-axis and y-axis: "Waiting Time (minutes)" and "Probability Density," respectively.
#    - A title is dynamically generated based on the current increment (e.g., "Empirical PDFs of Waiting Times for Increment = 5").
#    - A legend is added to distinguish between the `increase` and `decrease` directions.
#    - A grid is applied for better readability, and the layout is adjusted to ensure everything fits within the plot.
# 
# 6. **Display the Plot**:
#    - The plot is displayed using `plt.show()`, which renders the figure.
# 
# #### Notes:
# - **Probability Density**: The histograms are normalized to form a probability density function (PDF), making it easier to compare the relative frequency of waiting times for both directions.
# - **Transparency**: The use of alpha transparency in the fill areas helps make the overlapping regions more visible.
# - **Plot Customization**: Adjusting the plot's size and adding grid lines ensures that the visualization is clear and readable.
# 
# **Output**: A set of scatter plots showing the PDF of waiting times for both the `increase` and `decrease` directions, for each increment. The plots are color-coded for clarity and display the distribution of waiting times for better comparison.
# 

# %%
for increment in set(key[0] for key in waiting_times_dict.keys()):
        # Extract waiting times for "increase" and "decrease" directions for the current increment
    waiting_times_increase = waiting_times_dict.get((increment, "increase"), np.array([]))
    waiting_times_decrease = waiting_times_dict.get((increment, "decrease"), np.array([]))


    # Remove inf and NaN values explicitly
    cleaned_waiting_times_increase = waiting_times_increase[np.isfinite(waiting_times_increase)]
    cleaned_waiting_times_decrease = waiting_times_decrease[np.isfinite(waiting_times_decrease)]

    # Calculate histogram bins and normalize to obtain PDF
    # "density=True" ensures the histogram is normalized to form a probability density function
    hist_increase, bin_edges = np.histogram(cleaned_waiting_times_increase, bins=1000, density=True)
    hist_decrease, _ = np.histogram(cleaned_waiting_times_decrease, bins=1000, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Plot the PDFs using scatter plots for better visualization
    plt.figure(figsize=(10, 6))
    plt.scatter(bin_centers, hist_increase, color='blue', linewidth=2, marker='o', label='Increase', alpha=0.7)
    plt.scatter(bin_centers, hist_decrease, color='red', linewidth=2, marker='x', label='Decrease', alpha=0.7)
    plt.fill_between(bin_centers, hist_increase, color='blue', alpha=0.3)
    plt.fill_between(bin_centers, hist_decrease, color='red', alpha=0.3)

    # Add labels, title, and legend to the plot for clarity
    plt.xlabel('Waiting Time (minutes)', fontsize=14)
    plt.ylabel('Probability Density', fontsize=14)
    plt.title(f'Empirical PDFs of Waiting Times for Increment = {increment}', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


