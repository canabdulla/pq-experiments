import math

from plot_all import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from plot_helper import *
from scipy.interpolate import interp1d

# Here the impact of the number of subspaces M is plot.
def plot_ann_dataset_line(df, dataset, metric, sep):
    df = df.query("M != 16")
    if df["algorithm"].unique().size > 1:
        plot_ann_dataset_line(df.query("algorithm != 'PQ-SPACEDECOMP'"), dataset, metric, sep)
        df = df.query("algorithm != 'PQ'")
    if df.empty:
        return
    M_list = sorted(df["M"].unique())
    fig, ax = plt.subplots()
    df = df.query("algorithm != 'K-Means'")
    df["code-length"] = df["M"] * np.log2(df["subcentroids"])
    df["codebook"] = df["M"] * np.power(df["subcentroids"], 2)

    plt.xscale("log")

    for M in M_list:
        Mdf = df[df["M"] == M]
        Mdf.plot(kind="line", x="centroids", y="value", c=colors_M[M], ax=ax, marker=markers[M],
                 xlabel="Centroids", ylabel=all_labels[metric])
    control_axis(metric, ax)
    add_legend_M([m for m in M_list if m != 0], ax, "line", False, dataset)
    
    save_plot("ann", "line", dataset, metric, f"sep={sep} algo={df['algorithm'].unique()}")


# Here the comparison of ANN-Search with and without space decomposition is plot.
def plot_ann_comp(df, dataset, metric, sep):
    color_offset = 2
    if df["M"].unique().size > 1:
        plot_ann_comp(df.query("M == 4"), dataset, metric, sep)
        df = df.query("M == 2")
    M_list = sorted(df["M"].unique())
    alg_list = sorted(df["algorithm"].unique())
    fig, ax = plt.subplots()
    df = df.query("algorithm != 'K-Means'")
    df["code-length"] = df["M"] * np.log2(df["subcentroids"])
    plt.xscale("log")
    for alg in alg_list:
        for M in M_list:
            Mdf = df.query(f"M == {M} and algorithm == '{alg}'")
            Mdf.plot(kind="line", x="centroids", y="value", c=colors_comp[0 + color_offset] if alg == "PQ" else colors_comp[1 + color_offset], ax=ax, marker=markers[M],
                     xlabel="Centroids", ylabel=all_labels[metric])
    control_axis(metric, ax)
    add_legend_comp(2, ax, False, "algorithm", df["algorithm"].unique().tolist(), dataset, color_offset)

    save_plot("ann", "line", dataset, metric, f"sep={sep} algo={df['algorithm'].unique()} {df['M'].unique()}")

