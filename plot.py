import math
import os
import sys

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


def plot_distortion(df):
    pd.options.mode.copy_on_write = True
    fig, ax = plt.subplots()
    colors = {1: "tab:olive", 2: "tab:blue", 4: "tab:orange", 8: "tab:green"} #16: "tab:purple", }
    df = df[df["metric"] == "avg-f1"]
    df = df[df["dataset"] == "Adult"]
    df["codebook_size"] = df["centroids"] * df["M"]
    sdf = df[df["separate"] == "TRUE"]
    fdf = df[df["separate"] == "FALSE"]
    #df["code length"] = (df["centroids"] / df["M"]).apply(np.log2) * df["M"]

    sdf.plot(kind="scatter", x="codebook_size", y="value", c=sdf["M"].map(colors), label="Distortion", marker="x", ax=ax)
    fdf.plot(kind="scatter", x="codebook_size", y="value", c=fdf["M"].map(colors), label="Distortion", marker=".", ax=ax)
    ax.set_ylim(0, 1)

    handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=v, label=k, markersize=8) for k, v in
               colors.items()]
    ax.legend(title='Subspaces', handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.title("Instructions (clustering separate)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    # plt.savefig(os.path.join("plots", "distortion-s.svg"))
    plt.show()

def plot_ml_dataset(df):
    fig, ax = plt.subplots()
    ax.set_ylim(0, 1)



def plot_ml(df):
    df["codebook_size"] = df["centroids"] * df["M"]
    for d in df["dataset"].unique():
        for m in df["metric"].unique():
            plot_ml_dataset(df.query(f"dataset == '{d}' and metric == '{m}'"))




def main():
    if len(sys.argv) < 2:
        print("Usage: {} <test_case>".format(sys.argv[0]))
        return 1
    if sys.argv[1] == "distortion":
        # df = pd.read_hdf('results/distortion/test.hdf5', 'data')
        df = pd.read_csv('results/distortion.csv')
    elif sys.argv[1] == "ml":
        # df = pd.read_hdf('results/ml/test.hdf5', 'data')
        df = pd.read_csv('results/ml.csv')
        plot_ml(df)
        # plot_distortion(df)


if __name__ == '__main__':
    main()
