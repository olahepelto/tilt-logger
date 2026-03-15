import pandas as pd
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
CSV_FILE = "tilt_log.csv"       # Path to your CSV file
DOWNSAMPLE_FREQ = '10s'    # Downsample interval: '10s' = every 10 seconds
# ----------------------------

def main():
    # Read CSV efficiently
    print("Loading data...")
    df = pd.read_csv(CSV_FILE, parse_dates=['Timestamp'])
    
    # Set Timestamp as index for easy resampling
    df.set_index('Timestamp', inplace=True)
    
    # Keep only numeric columns for downsampling
    numeric_cols = df.select_dtypes(include='number')
    
    # Downsample the data by taking the mean for numeric columns
    print(f"Downsampling data every {DOWNSAMPLE_FREQ}...")
    df_downsampled = numeric_cols.resample(DOWNSAMPLE_FREQ).mean()
    
    # Create figure and first axis for Gravity
    fig, ax1 = plt.subplots(figsize=(12,6))
    
    color_gravity = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Specific Gravity', color=color_gravity)
    ax1.plot(df_downsampled.index, df_downsampled['Gravity'], color=color_gravity, marker='o', linestyle='-', markersize=3)
    ax1.tick_params(axis='y', labelcolor=color_gravity)
    ax1.grid(True)
    
    # Create second axis for Temperature
    ax2 = ax1.twinx()
    color_temp = 'tab:red'
    ax2.set_ylabel('Temperature (°C)', color=color_temp)
    ax2.plot(df_downsampled.index, df_downsampled['Temp_C'], color=color_temp, marker='x', linestyle='-', markersize=3)
    ax2.tick_params(axis='y', labelcolor=color_temp)
    
    plt.title("Specific Gravity and Temperature Over Time")
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()