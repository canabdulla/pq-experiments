import math
import os
import sys

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable

ds_desc = {
    "Adult": "Dataset: Adult \nnrow(X)=32,561 \nncol(X)=13",
    "Covtype": "Dataset: Covtype \nnrow(X)=581,012 \nncol(X)=54",
    "KDD 98": "Dataset: KDD 98 \nnrow(X)=95,412 \nncol(X)=469",
}

# labels = {"macro-f1": "Macro F1 Score", "avg-recall": "Average Recall", "avg-precision": "Average Precision",
#           "accuracy": "Accuracy", "ms": "Execution Time [s]"}
labels = {
    "accuracy": "Accuracy",
    "avg-precision": "Average Precision",
    "avg-recall": "Average Recall",
    "macro-f1": "Macro F1 Score",
    "ms": "Execution Time [s]"
          # ,
}

perf_labels = {
    "context-switches": "Context Switches",
    "cpu-migrations": "CPU Migrations",
    "page-faults": "Page Faults",
    "cycles": "CPU Cycles",
    "stalled-cycles-frontend": "Stalled Cycles Frontend",
    "stalled-cycles-backend": "Stalled Cycles Backend",
    "instructions": "Instructions",
    "branches": "Branches",
    "branch-misses": "Branch Misses",
    "L1-dcache-loads": "L1 Data Cache Loads",
    "L1-dcache-load-misses": "L1 Data Cache Load Misses",
    "L1-icache-loads": "L1 Instruction Cache Loads",
    "L1-icache-load-misses": "L1 Instruction Cache Load Misses",
    "dTLB-loads": "Data TLB Loads",
    "dTLB-load-misses": "Data TLB Load Misses",
    "iTLB-loads": "Instruction TLB Loads",
    "iTLB-load-misses": "Instruction TLB Load Misses",
    "L1-dcache-prefetches": "L1 Data Cache Prefetches"
}

colors = {1: "black", 2: "dodgerblue", 4: "orangered", 8: "forestgreen"}
markers = {1: "*", 2: "^", 4: "s", 8: "h"}


def plot_ml_dataset_line(df, M_list):
    pd.options.mode.copy_on_write = True
    metric = df["metric"].unique()[0]
    fig, ax = plt.subplots()
    df = df.sort_values(by=["centroids", "M"])

    for M in df["M"].unique():
        Mdf = df[df["M"] == M]
        if M != 0:
            Mdf.plot(kind="line", x="centroids", y="value", c=colors[M], ax=ax, marker=markers[M],
                     xlabel="Number of centroids", ylabel=labels[metric])
        else:
            baseline = Mdf["value"].values[0]
            plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")

    plot(M_list[1:], ax, metric, df, "Line")


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
    plt.ylabel(labels[metric])
    plot(M_list[1:], ax, metric, df, "Bar")


def plot(M_list, ax, metric, df, plot_name):
    if metric not in ["avg-precision", "avg-recall", "macro-f1", "accuracy"]:
        ax.set_ylim(ymin=0)
    else:
        ax.set_ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.2))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    handles = []
    handles.append(Line2D([0], [0], linestyle="--", color="r", label="baseline"))
    handles.extend([Line2D([0], [0], marker='s', color='w', markerfacecolor=colors[m], label=f"M={m}", markersize=8) for m in
               M_list])

    ax.legend(handles=handles,  loc='center', bbox_to_anchor=(1.12, 0.9), facecolor='white')
    # ax.legend(["Datensatz yarro"])
    df = df[df["M"] == 2]
    sep = df['separate'].unique()[0]
    title = f"{labels[metric]} {sep}"
    dataset = df['dataset'].unique()[0]

    props = dict(boxstyle='round', facecolor='white', alpha=0.5, edgecolor='grey')
    ax.text(1.02, 0.6,  ds_desc[dataset], transform=ax.transAxes, bbox=props)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"plots/ml/{plot_name} {dataset} {title}.png", dpi=300, bbox_inches='tight')
    # plt.show(bbox_inches='tight')


def plot_ml(df):
    df["centroids"] = df["subcentroids"] * df["M"]
    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            if m in perf_labels:
                continue
            data = df.query(f"dataset == '{d}' and metric == '{m}'")
            if m == "ms":
                data["value"] = data["value"] / 1000
            plot_ml_dataset_line(data, sorted(data["M"].unique()))
            plot_ml_dataset_grouped_bar(data, sorted(data["M"].unique()))


def main():
    if len(sys.argv) < 2:
        print("Usage: {} <test_case>".format(sys.argv[0]))
        return 1
    if sys.argv[1] == "distortion":
        # df = pd.read_hdf('results/distortion/test.hdf5', 'data')
        df = pd.read_csv('results/distortion.csv')
    elif sys.argv[1] == "ml":
        df = pd.read_csv('results/ml.csv')
        df = df.query("algorithm == 'Baseline' | separate == False")
        plot_ml(df)


if __name__ == '__main__':
    main()


def plot_distortion(df):
    pd.options.mode.copy_on_write = True
    fig, ax = plt.subplots()
    colors = {1: "tab:olive", 2: "tab:blue", 4: "tab:orange", 8: "tab:green"}  # 16: "tab:purple", }
    df = df[df["metric"] == "avg-f1"]
    df = df[df["dataset"] == "Adult"]
    df["centroids"] = df["centroids"] * df["M"]
    sdf = df[df["separate"] == "TRUE"]
    fdf = df[df["separate"] == "FALSE"]
    # df["code length"] = (df["centroids"] / df["M"]).apply(np.log2) * df["M"]

    sdf.plot(kind="scatter", x="centroids", y="value", c=sdf["M"].map(colors), label="Distortion", marker="x", ax=ax)
    fdf.plot(kind="scatter", x="centroids", y="value", c=fdf["M"].map(colors), label="Distortion", marker=".", ax=ax)
    ax.set_ylim(0, 1)

    handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=v, label=k, markersize=8) for k, v in
               colors.items()]
    ax.legend(title='Subspaces', handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.title("Instructions (clustering separate)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    # plt.savefig(os.path.join("plots", "distortion-s.svg"))
    plt.show()
