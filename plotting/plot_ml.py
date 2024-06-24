from plot_all import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from plot_helper import *

#can be easily adjusted to compare different implementations
def plot_sep_comp(df, dataset, metric, parameter):
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
        # if M != 0:
        #     q = np.arange(len(Mdf["centroids"].unique()))
        #     bars.append(ax.bar(q + i * width, Mdf["value"], width, color=colors[M]))
        #     i += 1
        # else:
        # baseline = Mdf["value"].values[0]
        # plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    q = np.arange(len(df[parameter].unique()))
    plt.xticks(q + ((i - 1) / 2) * width, sorted(df[parameter].unique()), rotation=90)
    plt.xlabel(f"Number of {parameter}")
    plt.ylabel(all_labels[metric])

    control_axis(metric, ax)

    # add_legend_M([M, M], ax, "bar")
    add_legend_sep(val, ax, False)
    add_legend_dataset(ax, dataset)
    save_plot("ml", "sep_comp", dataset, metric, f"{fixed}={val}")


def plot_ml_dataset_line(df, dataset, metric, sep):
    M_list = sorted(df["M"].unique())
    # metric = df["metric"].unique()[0]
    # sep = df.query("algorithm != 'Baseline'")['separate'].unique()[0]
    # dataset = df.query("algorithm != 'Baseline'")['dataset'].unique()[0]
    fig, ax = plt.subplots()

    for M in M_list:
        Mdf = df[df["M"] == M]
        if M != 0:
            Mdf.plot(kind="line", x="centroids", y="value", c=colors_M[M], ax=ax, marker=markers[M],
                     xlabel="Number of centroids", ylabel=all_labels[metric])
        else:
            baseline = Mdf["value"].values[0]
            plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    control_axis(metric, ax)
    add_legend_M([m for m in M_list if m != 0], ax, "line", True)
    add_legend_dataset(ax, dataset)
    save_plot("ml", "line", dataset, metric, sep)


def plot_ml_dataset_grouped_bar(df, dataset, metric, sep):
    M_list = sorted(df["M"].unique())
    width = 0.2
    i = 0
    bars = []

    fig, ax = plt.subplots()

    # plot bars and baseline
    for M in M_list:
        Mdf = df[df["M"] == M]
        if M != 0:
            q = np.arange(len(Mdf["centroids"].unique()))
            bars.append(ax.bar(q + i * width, Mdf["value"], width, color=colors_M[M]))
            i += 1
        else:
            baseline = Mdf["value"].values[0]
            plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    # add x-ticks
    q = np.arange(len(df["centroids"].unique()) - 1)
    plt.xticks(q + ((i - 1) / 2) * width, sorted(df["centroids"].unique())[1:], rotation=90)

    # add axis labels
    plt.xlabel("Number of centroids")
    plt.ylabel(all_labels[metric])

    control_axis(metric, ax)
    add_legend_M([m for m in M_list if m != 0], ax, "bar", True)
    add_legend_dataset(ax, dataset)
    save_plot("ml", "bar", dataset, metric, sep)
