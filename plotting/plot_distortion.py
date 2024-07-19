from plot_all import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from plot_helper import *
from scipy.interpolate import interp1d

#can be easily adjusted to compare different implementations
def plot_dist_sep_comp(df, dataset, metric, parameter):
    M_list = sorted(df["M"].unique())
    fig, ax = plt.subplots()

    baseline = df.query("algorithm == 'Baseline'")['value'].values[0]
    plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    #vary parameter and fix {fixed}
    if parameter == "centroids":
        fixed = "M"
        val = 2
    elif parameter == "M":
        fixed = "centroids"
        val = 32
    else:
        raise ValueError(f"Parameter {parameter} not recognized")
    df = df[df[fixed] == val]

    width = 0.2
    i = 0
    bars = []
    for s in {True, False}:
        sep_df = df[df["separate"] == s]
        q = np.arange(len(sep_df[parameter].unique()))
        bars.append(ax.bar(q + i * width, sep_df["value"], width, color=colors_sep[s]))
        i += 1

    q = np.arange(len(df[parameter].unique()))
    plt.xticks(q + ((i - 1) / 2) * width, sorted(df[parameter].unique()), rotation=90)
    plt.xlabel(f"Number of {parameter}")
    plt.ylabel(all_labels[metric])

    control_axis(metric, ax)

    # add_legend_M([M, M], ax, "bar")
    add_legend_sep(val, ax, False)
    add_legend_dataset(ax, dataset)
    save_plot("ml", "sep_comp", dataset, metric, f"{fixed}={val}")


def plot_dist_dataset_line(df, dataset, metric, sep):
    M_list = sorted(df["M"].unique())
    # metric = df["metric"].unique()[0]
    # sep = df.query("algorithm != 'Baseline'")['separate'].unique()[0]
    # dataset = df.query("algorithm != 'Baseline'")['dataset'].unique()[0]
    fig, ax = plt.subplots()
    df = df.query("algorithm != 'K-Means'")

    for M in M_list:
        Mdf = df[df["M"] == M]
        # x = Mdf["centroids"].values
        # y = Mdf["value"].values
        # x_new = np.linspace(x.min(), x.max(), 500)
        # f = interp1d(x, y, kind='slinear' if x.size < 4 else 'cubic')
        # y_smooth = f(x_new)
        #
        # plt.plot(x_new, y_smooth)
        # plt.scatter(x, y)

        Mdf.plot(kind="line", x="centroids", y="value", c=colors_M[M], ax=ax, marker=markers[M],
                 xlabel="Number of centroids", ylabel=all_labels[metric])


    control_axis(metric, ax)
    add_legend_M([m for m in M_list if m != 0], ax, "line", False)
    add_legend_dataset(ax, dataset)
    save_plot("distortion", "line", dataset, metric, sep)


def plot_dist_time(dist, time, dataset, sep):
    M_list = sorted(dist["M"].unique())
    # metric = df["metric"].unique()[0]
    # sep = df.query("algorithm != 'Baseline'")['separate'].unique()[0]
    # dataset = df.query("algorithm != 'Baseline'")['dataset'].unique()[0]
    fig, ax = plt.subplots()
    dist = dist.query("algorithm != 'K-Means'")
    time = time.query("algorithm != 'K-Means'")

    # ax2 = ax.twinx()
    for M in M_list:
        Mdist = dist[dist["M"] == M]
        Mtime = time[time["M"] == M]
        # x = Mdf["centroids"].values
        # y = Mdf["value"].values
        # x_new = np.linspace(x.min(), x.max(), 500)
        # f = interp1d(x, y, kind='slinear' if x.size < 4 else 'cubic')
        # y_smooth = f(x_new)
        #
        # plt.plot(x_new, y_smooth)
        # plt.scatter(x, y)

        Mdist.plot(kind="line", x="centroids", y="value", c=colors_M[M], ax=ax, marker=markers[M],
                 xlabel="Number of centroids", ylabel=all_labels["distortion"])
        # Mtime.plot(kind="line", x="centroids", y="value",  ax=ax2, color="black",
        #            xlabel="Number of centroids", ylabel=all_labels["ms"])

    control_axis("Distortion and Time", ax)
    add_legend_M([m for m in M_list if m != 0], ax, "line", False)
    add_legend_dataset(ax, dataset)
    save_plot("distortion", "line_2", dataset, "distortion", sep)

