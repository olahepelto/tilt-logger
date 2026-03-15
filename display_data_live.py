import pandas as pd
import matplotlib.pyplot as plt
import time

# ---------- CONFIG ----------
CSV_FILE = "tilt_log.csv"       # Path to your CSV file
DOWNSAMPLE_FREQ = '10s'    # Downsample interval
UPDATE_INTERVAL = 5        # Seconds between updates
# ----------------------------

def plot_live():
    plt.ion()  # Turn on interactive mode
    fig, ax1 = plt.subplots(figsize=(12,6))
    ax2 = ax1.twinx()
    
    color_gravity = 'tab:blue'
    color_temp = 'tab:red'
    
    while True:
        try:
            # Read and process CSV
            df = pd.read_csv(CSV_FILE, parse_dates=['Timestamp'])
            df.set_index('Timestamp', inplace=True)
            numeric_cols = df.select_dtypes(include='number')
            df_downsampled = numeric_cols.resample(DOWNSAMPLE_FREQ).mean()
            
            # Clear previous lines
            ax1.cla()
            ax2.cla()
            
            # Plot Specific Gravity
            ax1.plot(df_downsampled.index, df_downsampled['Gravity'], color=color_gravity, marker='o', linestyle='-', markersize=3)
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Specific Gravity', color=color_gravity)
            ax1.tick_params(axis='y', labelcolor=color_gravity)
            ax1.grid(True)
            
            # Plot Temperature
            ax2.plot(df_downsampled.index, df_downsampled['Temp_C'], color=color_temp, marker='x', linestyle='-', markersize=3)
            ax2.set_ylabel('Temperature (°C)', color=color_temp)
            ax2.tick_params(axis='y', labelcolor=color_temp)
            
            plt.title("Live Specific Gravity and Temperature")
            fig.tight_layout()
            plt.pause(0.1)  # Needed to update the plot
            
            # Wait before next update
            time.sleep(UPDATE_INTERVAL)
            
        except KeyboardInterrupt:
            print("Stopped by user.")
            break

if __name__ == "__main__":
    plot_live()