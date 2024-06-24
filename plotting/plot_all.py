import math
import os
import sys

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from plot_ml import *
from plot_dist import *


def plot_ml(df):
    pd.options.mode.copy_on_write = True
    df["centroids"] = df["subcentroids"] * df["M"]
    df = df.sort_values(by=["centroids", "M"])

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
                # plot_ml_dataset_line(data, d, m, s)
                plot_ml_dataset_grouped_bar(data, d, m, s)
            data = df.query(f"dataset == '{d}' and metric == '{m}'")
            if data.empty:
                continue
            plot_sep_comp(data, d, m, "M")
            plot_sep_comp(data, d, m, "centroids")


def plot_dist_all(df):
    pd.options.mode.copy_on_write = True
    df["centroids"] = df["subcentroids"] * df["M"]
    df = df.sort_values(by=["centroids", "M"])
    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            for s in {"True", "False"}:
                # if m in perf_labels:
                #     continue
                data = df.query(
                    f"dataset == '{d}' and metric == '{m}' and (separate == {s} or algorithm == 'Baseline')")
                if m == "ms":
                    data["value"] = data["value"] / 1000
                plot_dist_dataset_line(data, d, m, s)
                # plot_dist_dataset_grouped_bar(data, d, m, s)



def plot_dist(df):
    pd.options.mode.copy_on_write = True
    df["centroids"] = df["subcentroids"] * df["M"]
    df = df.sort_values(by=["centroids", "M"])
    for d in df["dataset"].unique():
        for s in {"True", "False"}:
            distortion = df.query(f"dataset == '{d}' and metric == 'distortion' and (separate == {s} or algorithm == 'Baseline')")
            time = df.query(f"dataset == '{d}' and metric == 'ms' and (separate == {s} or algorithm == 'Baseline')")
            time["value"] = time["value"] / 1000
            plot_dist_time(distortion, time, d, s)

def main():
    if len(sys.argv) < 2:
        print("Usage: {} <test_case>".format(sys.argv[0]))
        return 1
    agg_cols = ["value"] #, "date", "processor"]
    if sys.argv[1] == "dist":
        df = pd.read_csv('server-files/distortion.csv')
        df.drop('date', axis=1, inplace=True)
        df = df.query("M != 8 or dataset != 'Adult'")
        df = df.groupby([c for c in df.columns if c not in agg_cols]).mean().reset_index()
        plot_dist_all(df)
        plot_dist(df)
    elif sys.argv[1] == "ml":
        df = pd.read_csv('server-files/ml.csv')
        df.drop('date', axis=1, inplace=True)
        df = df.groupby([c for c in df.columns if c not in agg_cols]).mean().reset_index()
        plot_ml(df)


if __name__ == '__main__':
    main()
