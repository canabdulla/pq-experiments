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


def plot_rsquared_dataset_grouped_bar(df, dataset, metric, sep):
    M_list = sorted(df["M"].unique())
    width = 0.2
    i = 0
    bars = []
    fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(12, 10), gridspec_kw={'width_ratios': [1, 5]})
    ldf = df[np.abs(df["value"]) > 0.1]
    df = df[np.abs(df["value"]) <= 0.1]

    # plot bars and baseline
    for M in M_list:
        Mdf = df[df["M"] == M]
        if M != 0:
            q = np.arange(len(Mdf["centroids"].unique()))
            bars.append(ax1.bar(q + i * width, Mdf["value"], width, color=colors_M[M]))
            i += 1

    plt.axhline(y=0, color="black", linewidth=0.8)
    ax2.axhline(y=0, color="black", linewidth=0.8)

    rvalue = ldf["value"].unique()[0]
    ldf.plot(kind="bar", x="algorithm", y="value", ax=ax2, color="darkgreen" if rvalue > 0 else "darkred",
             ylabel=all_labels[metric], xlabel="")
    if rvalue > 0:
        ax2.set_ylim([0, 1])
    else:
        ax2.set_ylim([-1, 0])
    if all(i > 0 for i in df["value"]):
        ax1.set_ylim([0, 0.01])
        ax2.set_ylim([0, 1])
    else:
        ax1.set_ylim([-0.01, 0.01])
        ax2.set_ylim([-1, 1])

    ax2.tick_params(axis='x', labelrotation=360)
    ax2.get_legend().set_visible(False)


    # add x-ticks
    q = np.arange(len(df["centroids"].unique()) - 1)
    plt.xticks(q + ((i - 1) / 2) * width, sorted(df["centroids"].unique())[1:], rotation=90)

    # add axis labels
    plt.xlabel("Number of centroids")
    plt.ylabel(all_labels[metric])
    # ax1.set_ylim([-0.01, 0.01])
    fig.tight_layout()

    # control_axis(metric, ax1)
    add_legend_M([m for m in M_list if m != 0], ax1, "bar", True)
    add_legend_dataset(ax1, dataset)
    # add_legend_dataset(ax2, dataset)
    plt.show()
    # save_plot("ml", "bar", dataset, metric, sep)


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
    # ax.set_ylim(-1, 1)
    # plt.yscale("log")
    add_legend_M([m for m in M_list if m != 0], ax, "bar", True)
    add_legend_dataset(ax, dataset)
    save_plot("ml", "bar", dataset, metric, sep)
