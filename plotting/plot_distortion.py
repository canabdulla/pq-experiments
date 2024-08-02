from plot_all import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from plot_helper import *
from scipy.interpolate import interp1d

# Plot the distortion for different datasets in a line plot.
def plot_dist_dataset_line(df, dataset, metric, sep):
    M_list = sorted(df["M"].unique())
    fig, ax = plt.subplots()
    df = df.query("algorithm != 'K-Means'")

    for M in M_list:
        Mdf = df[df["M"] == M]
        Mdf.plot(kind="line", x="centroids", y="value", c=colors_M[M], ax=ax, marker=markers[M],
                 xlabel="Number of centroids", ylabel=all_labels[metric])

    control_axis(metric, ax)
    add_legend_M([m for m in M_list if m != 0], ax, "line", False, dataset)
    
    save_plot("distortion", "line", dataset, metric, sep)