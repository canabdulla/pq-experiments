import math
import os
import sys

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from plot_ml import *

ds_desc = {
    "Adult": "Dataset: Adult \nnrow(X)=32,561 \nncol(X)=13",
    "Covtype": "Dataset: Covtype \nnrow(X)=581,012 \nncol(X)=54",
    "KDD98": "Dataset: KDD 98 \nnrow(X)=95,412 \nncol(X)=469",
    "sift_base_100k": "Dataset: SIFT \nnrow(X)=?",
    "gist_base_100k": "Dataset: GIST \nnrow(X)=?",
}

labels = {
    "distortion": "Distortion",
    "accuracy": "Accuracy",
    "avg-precision": "Average Precision",
    "avg-recall": "Average Recall",
    "macro-f1": "Macro F1 Score",
    "ms": "Execution Time [s]",
    "mse": "Mean Squared Error"}

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
all_labels = labels
all_labels.update(perf_labels)

colors = {1: "purple", 2: "dodgerblue", 4: "orangered", 8: "forestgreen"}
markers = {1: "X", 2: "^", 4: "s", 8: "h"}


def plot_dist_scatter(df, M_list):
    pd.options.mode.copy_on_write = True
    metric = df["metric"].unique()[0]
    fig, ax = plt.subplots()
    df = df.sort_values(by=["centroids", "M"])

    for M in df["M"].unique():
        Mdf = df[df["M"] == M]
        if M != 0:
            Mdf.plot(kind="scatter", x="centroids", y="value", c=colors[M], ax=ax, marker=markers[M],
                     # markersize=2, linewidth=0.8,
                     xlabel="Codebook size", ylabel=all_labels[metric],)
        else:
            baseline = Mdf["value"].values[0]
            plt.axhline(y=baseline, color="r", linestyle="--", label="baseline")
    plot(M_list[1:], ax, df, "line", "distortion")


def plot_ml(df):
    df["centroids"] = df["subcentroids"] * df["M"]
    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            for s in {True, False}:
                # if m in perf_labels:
                #     continue
                data = df.query(
                    f"dataset == '{d}' and metric == '{m}' and (separate == {s} or algorithm == 'Baseline')")
                if data.empty:
                    continue
                if m == "ms":
                    data["value"] = data["value"] / 1000
                plot_ml_dataset_line(data, sorted(data["M"].unique()))
                plot_ml_dataset_grouped_bar(data, sorted(data["M"].unique()))


def plot_dist(df):
    df["centroids"] = df["subcentroids"] * df["M"]
    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            for s in {"True", "False"}:
                # if m in perf_labels:
                #     continue
                data = df.query(
                    f"dataset == '{d}' and metric == '{m}' and (separate == {s} or algorithm == 'Baseline')")
                if m == "ms":
                    data["value"] = data["value"] / 1000
                plot_dist_scatter(data, sorted(data["M"].unique()))

def main():
    if len(sys.argv) < 2:
        print("Usage: {} <test_case>".format(sys.argv[0]))
        return 1
    if sys.argv[1] == "dist":
        df = pd.read_csv('results/distortion.csv')
        plot_dist(df)
    elif sys.argv[1] == "ml":
        df = pd.read_csv('results/ml.csv')
        # df = df.query("algorithm == 'Baseline' | separate == False")
        plot_ml(df)


if __name__ == '__main__':
    main()
