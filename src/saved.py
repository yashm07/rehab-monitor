import numpy as np
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt

def avg_gait_cycle(df: pd.DataFrame):
    # mark all points where 1 -> 0,0
    f = list(df["f"])
    window = [1, 0]
    indices = []

    for i in range(len(f)):
        if f[i] == 0 and f[i-len(window):i] == window:
            indices.append(i)

    # go through all points to get data on each gait cycle
    gait_cycle_dfs = []
    for i in range(len(indices)-1):
        gait_cycle_dfs.append(df[indices[i]: indices[i+1]])

    # calculate avg len of gait cycle
    avg_cycle_len = int(np.mean([len(cycle) for cycle in gait_cycle_dfs]))

    # create empty vectors 
    x_final, k_final = np.zeros(avg_cycle_len), np.zeros(avg_cycle_len)

    # resample each dataframe to match avg len
    for cycle_df in gait_cycle_dfs:
        x_final += np.linspace(0, cycle_df.iloc[-1]["x"] - cycle_df.iloc[0]["x"], avg_cycle_len)
        k_final += signal.resample(cycle_df["k"], avg_cycle_len)

    # get average
    x_final /= len(gait_cycle_dfs)
    k_final /= len(gait_cycle_dfs)

    # plot
    return x_final, k_final

def plot_data(df: pd.DataFrame):
    x, k, f = df["x"], df["k"], df["f"]
    x_avg, k_avg = avg_gait_cycle(df)

    fig, [ax1, ax2, ax3] = plt.subplots(3)
    
    ax1.set_ylim(0, 100)
    ax2.set_ylim(0, 2)
    
    ax1.plot(x, k)    
    ax2.plot(x, f)
    ax3.plot(x_avg, k_avg)

    ax1.set_ylabel("Knee flexion angle")
    ax2.set_ylabel("Heel strike (0/1)")
    ax3.set_ylabel("Avg knee flexion angle")

    plt.show()