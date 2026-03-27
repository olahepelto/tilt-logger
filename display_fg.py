import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

CSV_FILE = "tilt_log.csv"
DOWNSAMPLE_FREQ = '300s'

def main():
    print("Loading data...")
    df = pd.read_csv(CSV_FILE, parse_dates=['Timestamp'])
    df.set_index('Timestamp', inplace=True)

    numeric_cols = df.select_dtypes(include='number')
    print(f"Downsampling data every {DOWNSAMPLE_FREQ}...")
    df_downsampled = numeric_cols.resample(DOWNSAMPLE_FREQ).mean()
    df_plot = df_downsampled.reset_index()

    # Numeric time for plotting & regression (seconds since start)
    df_plot['time_num'] = (df_plot['Timestamp'] - df_plot['Timestamp'].min()).dt.total_seconds()

    # Fit linear regression to gravity
    X = df_plot['time_num'].values.reshape(-1, 1)
    y = df_plot['Gravity'].values
    model = LinearRegression()
    model.fit(X, y)

    # Predict the time when gravity reaches 1.010
    target_gravity = 1.017
    # time_num = (target - intercept) / slope
    time_to_target_sec = (target_gravity - model.intercept_) / model.coef_[0]
    target_datetime = df_plot['Timestamp'].min() + pd.to_timedelta(time_to_target_sec, unit='s')
    print(f"Estimated time to reach {target_gravity} FG: {target_datetime}")

    fig, ax1 = plt.subplots(figsize=(12, 6))

    color_gravity = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Specific Gravity', color=color_gravity)

    # Plot gravity raw data on numeric axis
    ax1.plot(df_plot['time_num'], df_plot['Gravity'], color=color_gravity,
             marker='o', linestyle='-', markersize=3)

    # Plot trendline for gravity (numeric x)
    sns.regplot(x='time_num', y='Gravity', data=df_plot,
                scatter=False, ax=ax1, color=color_gravity,
                line_kws={'linewidth': 2})

    # Add horizontal line for target FG and vertical line for estimated time
    ax1.axhline(target_gravity, color='green', linestyle='--', label=f'Target FG {target_gravity}')
    ax1.axvline(time_to_target_sec, color='purple', linestyle='--', label=f'Estimated finish')

    ax1.tick_params(axis='y', labelcolor=color_gravity)
    ax1.grid(True)

    ax2 = ax1.twinx()
    color_temp = 'tab:red'
    ax2.set_ylabel('Temperature (°C)', color=color_temp)
    ax2.plot(df_plot['time_num'], df_plot['Temp_C'], color=color_temp,
             marker='x', linestyle='-', markersize=3)
    ax2.tick_params(axis='y', labelcolor=color_temp)

    # Format x-axis ticks to show datetime labels
    def time_num_to_datetime(x, pos):
        return (df_plot['Timestamp'].min() + pd.to_timedelta(x, unit='s')).strftime('%Y-%m-%d\n%H:%M')

    ax1.xaxis.set_major_formatter(plt.FuncFormatter(time_num_to_datetime))
    plt.setp(ax1.get_xticklabels(), rotation=30, ha='right')

    plt.title("Specific Gravity and Temperature Over Time (with Trendlines)")
    ax1.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
