import math
import os
import sys

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from plot_ml import *
from plot_distortion import *
from plot_ann import *
from plot_bs import *
from plotting.plot_ml import plot_ml_dataset_grouped_bar


def plot_ml(df):
    #compare implementation with and without space-decomposition
    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            data = df.query(f"dataset == '{d}' & metric == '{m}'")
            if data.empty:
                continue
            plot_comp(data, d, m, "M", "algorithm")

    df = df.query("algorithm != 'PQ-SPACEDECOMP'")

    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            for s in {True, False}:
                if m in perf_labels:
                    continue
                data = df.query(
                    f"dataset == '{d}' and metric == '{m}' and (separate == {s} or algorithm == "
                    f"'Baseline')")
                if data.empty:
                    continue
                if m == "time":
                    plot_ml_dataset_grouped_bar(data, d, m, s)
                    plot_ml_dataset_grouped_bar_time(data, d, m, s)
                else:
                    plot_ml_dataset_grouped_bar(data, d, m, s)
                if m in ["test-rsq", "train-rsq"]:
                    plot_rsquared_dataset_grouped_bar(data, d, m, s)
                    plot_rsquared_dataset_grouped_bar(data, d, m, s)
            data = df.query(f"dataset == '{d}' and metric == '{m}'")
            if data.empty:
                continue
            if m in perf_labels:
                continue
            plot_comp(data, d, m, "M", "separate")
            plot_comp(data, d, m, "centroids", "separate")

def plot_all(df, case):
    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            for s in {"True", "False"}:
                    if m in perf_labels:
                        continue
                    data = df.query(
                        f"dataset == '{d}' and metric == '{m}' and (separate == {s} or algorithm == 'Baseline' or algorithm == 'BASELINE_SAMPLING')")
                    if case == "distortion":
                        plot_dist_dataset_line(data, d, m, s)
                    elif case == "ann":
                        plot_ann_dataset_line(data, d, m, s)
                        plot_ann_comp(data, d, m, s)
                    if case == "bs":
                        plot_bs_dataset_grouped_bar(data, d, m, s)


def main():
    if len(sys.argv) < 2:
        print("Usage: {} <test_case>".format(sys.argv[0]))
        return 1
    case = sys.argv[1]

    #read and process input
    df = pd.read_csv(f"results/{case}.csv")

    df.loc[df["metric"] == "time", "value"] /= 1000
    pd.options.mode.copy_on_write = True
    df["centroids"] = df["subcentroids"] * df["M"]
    df = df.sort_values(by=["centroids", "M"])

    if case == "distortion":
        df = df.query("M != 8 or dataset != 'Adult'")

    #aggregate values of multiple runs
    df.drop('date', axis=1, inplace=True)
    agg_cols = ["value"] #, "date", "processor"]
    df = df.groupby([c for c in df.columns if c not in agg_cols]).mean().reset_index()
    if case != "ml":
        plot_all(df, case)
    else:
        plot_ml(df)

if __name__ == '__main__':
    main()
