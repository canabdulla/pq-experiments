from plot_all import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_ml_dataset_line(df, M_list):
    pd.options.mode.copy_on_write = True
    metric = df["metric"].unique()[0]
    fig, ax = plt.subplots()
    df = df.sort_values(by=["centroids", "M"])

    for M in df["M"].unique():
        Mdf = df[df["M"] == M]
        if M != 0:
            Mdf.plot(kind="line", x="centroids", y="value", c=colors[M], ax=ax, marker=markers[M],
                     xlabel="Number of centroids", ylabel=all_labels[metric])
        else:
            baseline = Mdf["value"].values[0]
            plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    plot(M_list, ax, df, "line", "ml")


def plot_ml_dataset_grouped_bar(df, M_list):
    pd.options.mode.copy_on_write = True
    metric = df["metric"].unique()[0]
    fig, ax = plt.subplots()
    df = df.sort_values(by=["centroids", "M"])
    width = 0.2

    i = 0
    bars = []
    for M in M_list:
        Mdf = df[df["M"] == M]
        # q = Mdf["centroids"].unique()
        if M != 0:
            q = np.arange(len(Mdf["centroids"].unique()))
            bars.append(ax.bar(q + i * width, Mdf["value"], width, color=colors[M]))
            i += 1
        else:
            baseline = Mdf["value"].values[0]
            plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    q = np.arange(len(df["centroids"].unique())-1)
    plt.xticks(q + ((i-1)/2) * width, sorted(df["centroids"].unique())[1:], rotation=90)
    plt.xlabel("Number of centroids")
    plt.ylabel(all_labels[metric])
    plot(M_list, ax, df, "bar", "ml")

def plot(M_list, ax, df, sub_folder, folder):
    if 0 in M_list:
        M_list.remove(0)
    metric = df["metric"].unique()[0]
    if metric not in ["avg-precision", "avg-recall", "macro-f1", "accuracy"]:
        ax.set_ylim(ymin=0)
    else:
        ax.set_ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.2))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    handles = []
    t = markers[1]
    a = colors[1]
    handles.append(Line2D([0], [0], linestyle="--", color="r", label="baseline"))
    handles.extend([Line2D([0], [0], marker=markers[m] if not sub_folder == "bar" else 's', color='w',
                           markerfacecolor=colors[m], label=f"M={m}",
                           markersize=8) for m in
                    M_list])

    ax.legend(handles=handles, loc='center', bbox_to_anchor=(1.12, 0.9), facecolor='white')
    df = df[df["M"] == 2]
    sep = df['separate'].unique()[0]

    title = f"{all_labels[metric]} {sep}"

    sub_sub_f = ""
    if metric in perf_labels:
        sub_sub_f = "perf/"

    dataset = df['dataset'].unique()[0]

    props = dict(boxstyle='round', facecolor='white', alpha=0.5, edgecolor='grey')
    ax.text(1.02, 0.6, ds_desc[dataset], transform=ax.transAxes, bbox=props)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"plots/{folder}/{sub_folder}/{sub_sub_f}{dataset} {title}.png", dpi=300, bbox_inches='tight')
