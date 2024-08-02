from plot_all import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from plot_helper import *


# Here we compare different parameters of the implementation to each other.
# It is used to compare quantizing separately/together and to compare the
# performance of space decomposition/no space decomposition.
def plot_comp(df, dataset, metric, parameter, comp_col):
    types = df["type"].unique()
    if len(types) > 1:
        plot_comp(df[df["type"] == types[1]], dataset, metric, parameter, comp_col)
    df = df.query(f"type == '{types[0]}'")
    M_list = sorted(df["M"].unique())
    fig, ax = plt.subplots()

    #vary parameter and fix {fixed}
    if parameter == "centroids":
        fixed = "M"
        val = 2
    elif parameter == "M":
        fixed = "centroids"
        val = 16
    else:
        raise ValueError(f"Parameter {parameter} not recognized")
    df = df[df[fixed] == val]

    width = 0.2
    i = 0
    bars = []
    color_offset = 0 if comp_col == "separate" else 2
    for s in df[comp_col].unique():
        if s == "Baseline":
            continue
        comp_df = df[df[comp_col] == s]
        if comp_col != "separate":
            comp_df = comp_df[comp_df["separate"] == False]
        q = np.arange(len(comp_df[parameter].unique()))
        bars.append(ax.bar(q + i * width, comp_df["value"], width, color=colors_comp[i + color_offset]))
        i += 1

    q = np.arange(len(df[parameter].unique()))
    plt.xticks(q + ((i - 1) / 2) * width, sorted(df[parameter].unique()), rotation=90)
    plt.xlabel(f"Number of {parameter}")
    plt.ylabel(all_labels[metric])

    control_axis(metric, ax)

    add_legend_comp(val, ax, False, comp_col, df[comp_col].unique().tolist(), dataset, color_offset)
    type = df["type"].unique()[0]

    save_plot("ml", "comp", dataset, metric, f"{fixed}={val} param={parameter} comp={comp_col} type={type}")

# Plot the R²-metric for the KDD98 dataset.
def plot_rsquared_dataset_grouped_bar(df, dataset, metric, sep):
    M_list = sorted(df["M"].unique())
    width = 0.2
    i = 0
    bars = []
    fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(12, 10), gridspec_kw={"width_ratios": [1, 5]})
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
    q = np.arange(len(df["centroids"].unique()))
    plt.xticks(q + ((i - 1) / 2) * width, sorted(df["centroids"].unique()), rotation=0)

    # add axis labels
    plt.xlabel("Number of centroids")
    plt.ylabel(all_labels[metric])
    add_legend_M([m for m in M_list if m != 0], ax1, "bar", True, dataset)

    # plt.show()
    save_plot("ml", "bar", dataset, metric, sep)


# Plot different metrics, including the accuracy and perf statistics as a bar chart for different number of subspaces
# M grouped by the number of centroids.
def plot_ml_dataset_grouped_bar(df, dataset, metric, sep):
    types = df["type"].unique()
    if len(types) > 1:
        plot_ml_dataset_grouped_bar(df[df["type"] == types[1]], dataset, metric, sep)
    df = df.query(f"type == '{types[0]}'")

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
    centroids = df["centroids"].unique()
    centroids = np.delete(centroids, np.where(centroids == 0))
    q = np.arange(len(centroids))
    plt.xticks(q + ((i - 1) / 2) * width, sorted(centroids), rotation=90)

    # add axis labels
    plt.xlabel("Number of centroids")
    plt.ylabel(all_labels[metric])

    control_axis(metric, ax)
    add_legend_M([m for m in M_list if m != 0], ax, "bar", True, dataset)

    save_plot("ml", "bar", dataset, metric, f"sep={sep} type={types[0]}")

# The execution time from the machine learning experiments is split into regression time and clustering time.
# This function plots the overall execution time.
def plot_ml_dataset_grouped_bar_time(df, dataset, metric, sep):
    # df.loc[df.type == "regression", "value"] = df["value"] * 200
    agg_cols = ["value", "type"]
    total_df = df.groupby([c for c in df.columns if c not in agg_cols]).agg({"value": "sum"}).reset_index()
    df = df.query(f"type == 'regression'")

    M_list = sorted(df["M"].unique())
    width = 0.2
    i = 0
    bars = []

    fig, ax = plt.subplots()

    # plot bars and baseline
    for M in M_list:
        Mdf = df[df["M"] == M]
        Mdft = total_df[total_df["M"] == M]
        if M != 0:
            q = np.arange(len(Mdf["centroids"].unique()))
            bars.append(ax.bar(q + i * width, Mdft["value"], width, color=darken_color(colors_M[M])))
            bars.append(ax.bar(q + i * width, Mdf["value"], width, color=colors_M[M]))
            i += 1
        else:
            baseline = Mdf["value"].values[0]
            plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    # add x-ticks
    centroids = df["centroids"].unique()
    centroids = np.delete(centroids, np.where(centroids == 0))
    q = np.arange(len(centroids))
    plt.xticks(q + ((i - 1) / 2) * width, sorted(centroids), rotation=90)

    # add axis labels
    plt.xlabel("Number of centroids")
    plt.ylabel(all_labels[metric])

    control_axis(metric, ax)
    add_legend_M([m for m in M_list if m != 0], ax, "bar", True, dataset)

    save_plot("ml", "bar", dataset, metric, f"sep={sep} type=BOTH")
