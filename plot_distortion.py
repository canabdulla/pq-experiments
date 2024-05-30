import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D


def parse_outputs(output_dir):
    data = []
    for filename in os.listdir(output_dir):
        with open(os.path.join(output_dir, filename), "r") as file:
            for line in file:
                try:
                    distortion = float(line.strip())
                    testcase = os.path.splitext(filename)[0].split()
                    testcase.append(distortion)
                    data.append(testcase)
                except ValueError:
                    continue

    df = pd.DataFrame(data, columns=["Algorithm", "Dataset", "M", "Centroids", "Sample Size", "Separate", "Distortion"])
    df["M"] = df["M"].astype(int)
    df["Centroids"] = df["Centroids"].astype(int)
    df["Sample Size"] = df["Sample Size"].astype(int)
    return df


def plot_metrics(df):
    fig, ax = plt.subplots()
    # dfs = df.sort_values(by="Test Case", ascending=False)
    # cmap = ListedColormap(["red", "green", "blue", "red", "green"])
    colors = {2: "tab:blue", 4: "tab:orange", 8: "tab:green", 64: "tab:purple", 128: "tab:olive"}
    df.plot(kind="scatter", x="Centroids", y="Distortion", c=df["M"].map(colors), label="Distortion", marker="x", ax=ax)
    tmp = df[df["M"] == 4]
    tmp = tmp.sort_values(by="Centroids", ascending=False)
    plt.plot(tmp["Centroids"], tmp["Distortion"], "r-", zorder=100)
    ax.set_ylim(0, 80000)
    # plt.scatter(df["Centroids"], df["Distortion"], c=df["M"].map(colors), label="Distortion")
    # plt.plot(df["Centroids"], df["Distortion"], c=df["M"].map(colors))

    handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=v, label=k, markersize=8) for k, v in colors.items()]
    ax.legend(title='Subvector size', handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.title("Distortion")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "distortion.svg"))
    plt.show()


if __name__ == '__main__':
    df = parse_outputs("output")
    plot_metrics(df)
