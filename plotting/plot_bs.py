from plot_all import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from plot_helper import *


# Here the model performance of a logistic regression workload
# employing baseline sampling is compared to the performance of product quantization.
def plot_bs_dataset_grouped_bar(df, dataset, metric, sep):
    if df["algorithm"].unique().size > 2:
        plot_bs_dataset_grouped_bar(df.query("algorithm != 'PQ-SPACEDECOMP'"), dataset, metric, sep)
        df = df.query("algorithm != 'PQ'")
    if df.empty:
        return
    c_list = sorted(df["centroids"].unique())
    width = 0.1
    i = 0
    bars = []

    fig, ax = plt.subplots()
    color_map = plt.cm.Blues(np.linspace(0, 1, len(c_list)))

    q = np.arange(len(df["M"].unique()))
    # plot bars and baseline
    for c in c_list:
        cdf = df[df["centroids"] == c]
        q = np.arange(len(cdf["M"].unique()))
        # Loop through each row in the filtered dataframe to plot bars with increasingly darker colors
        for j, (index, row) in enumerate(cdf.iterrows()):
            bars.append(ax.bar(q[j] + i * width, row['value'], width,
                               color=color_map[c_list.index(c)] if row.algorithm == "PQ" or row.algorithm == "PQ-SPACEDECOMP" else "red"))
        i += 1

    # add x-ticks
    q = np.arange(len(df["M"].unique()))
    df["sf"] = np.round(df["M"] / 14, decimals=2)
    plt.xticks(q + ((i - 1) / 2) * width, sorted(df["sf"].unique()), rotation=360)

    # add axis labels
    plt.xlabel("Sampling Factor")
    plt.ylabel(all_labels[metric])

    control_axis(metric, ax)
    add_legend_bs(0, ax, False, "centroids", ["Baseline Sampling", 8, 16, 32, 64, 128], dataset, color_map)
    
    save_plot("bs", "bar", dataset, metric, f"sep={sep} algo={df['algorithm'].unique()}")
