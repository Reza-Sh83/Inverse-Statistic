# Gold Price Waiting Time Analysis

## Project Overview
This project analyzes time-series gold price data (sampled at 1-minute intervals) to determine how long it takes for the price to increase or decrease by specified amounts (e.g., $5, $10, $20). This can offer valuable insights into market volatility and help traders estimate reaction times for price movements.

---

## Problem Statement
Given a time series of gold prices:
- Compute the **waiting time** for the price to increase or decrease by a specified amount from the current point.
- Prices are in **USD** and sampled every **1 minute**.
- If no such change occurs before the end of the data, the waiting time is marked as **infinity**, indicating that the target price was never reached within the dataset timeframe.

---

## Dataset Requirements
- A plain text file where each line contains a single gold price value.
- Prices must be sampled at **1-minute** intervals.

---

## Methodology
### 1. **Data Processing**
- Load data from text file.
- Convert to a NumPy array for efficient numerical operations.

### 2. **Waiting Time Calculation**
- For a set of price increments (e.g., 5, 10, 20):
  - Compute time to reach `price + increment` (increase).
  - Compute time to reach `price - increment` (decrease).
- Store these as separate arrays for each increment and direction.

**Example:**
If the current price is $1800 and the increment is $10:
- If price reaches $1810 in 3 minutes → waiting time (increase) = 3 min.
- If price drops to $1790 in 7 minutes → waiting time (decrease) = 7 min.

### 3. **Visualization**
- **Bar Plots**: Show waiting times over time.
- **Histograms**: Frequency distribution of waiting times.
- **Empirical PDFs**: Scatter plots showing estimated PDFs of waiting times.

---

## Output
### Minimum Waiting Time for Increase by 10 (Sample Output)
<img src="Minimum Waiting Time for Increase by 10.png" width="450">

### Minimum Waiting Time for Increase by 10 (Frequency) (Sample Output)
<img src="Minimum Waiting Time for Increase by 10 (Frequency).png" width="450">

### Empirical PDFs of Waiting Times for Increment 10 (Sample Output)
<img src="Empirical PDFs of Waiting Times for Increment 10.png" width="450">

---

## Assumptions & Limitations
- Assumes constant 1-minute sampling without missing data.
- Does not account for market closures or external shocks.
- Waiting times marked as infinity when price target is never reached.

---

## Applications
- Helps understand **market reaction times** to price changes.
- Can be used to model **short-term risk and return profiles**.
- Useful for **trading strategies** that depend on price momentum or reversals.

---

## Dependencies
- Python 3+
- NumPy
- Matplotlib

---

## License

MIT License. Feel free to modify and use for academic or personal purposes. Attribution appreciated!

