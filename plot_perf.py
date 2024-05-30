import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from matplotlib.lines import Line2D


def parse_perf_output(output_dir):
    data = []
    for filename in os.listdir(output_dir):
        with open(os.path.join(output_dir, filename), 'r') as file:
            for line in file:
                parts = [e.strip() for e in line.split(';')]
                if len(parts) == 7:
                    value, unit, metric, _, _, _, _ = parts
                    try:
                        value = float(value)
                        testcase = os.path.splitext(filename)[0].split()
                        testcase.append(metric)
                        testcase.append(value)
                        data.append(testcase)
                    except ValueError:
                        continue

    df = pd.DataFrame(data, columns=["Algorithm", "Dataset", "M", "Centroids", "Sample Size", "Separate", 'Metric', 'Value'])
    df["M"] = df["M"].astype(int)
    df["Centroids"] = df["Centroids"].astype(int)
    df["Sample Size"] = df["Sample Size"].astype(int)
    df["Value"] = df["Value"].astype(float)
    return df


def plot_metrics(df):

    dfs = df.sort_values(by='M', ascending=False)
    for metric in dfs['Metric'].drop_duplicates():
        fig, ax = plt.subplots()
        tmp = dfs[dfs['Metric'] == metric]
        colors = {2: "tab:blue", 4: "tab:orange", 8: "tab:green", 64: "tab:purple", 128: "tab:olive"}
        tmp.plot(kind="scatter", x="Centroids", y="Value", c=tmp["M"].map(colors), label=metric, marker="x",
                ax=ax)
        # tmp = df[df["M"] == 4]
        # tmp = tmp.sort_values(by="Centroids", ascending=False)
        # plt.plot(tmp["Centroids"], tmp["Value"], "r-")
        # ax.set_ylim(0, 80000)
        # plt.scatter(df["Centroids"], df["Distortion"], c=df["M"].map(colors), label="Distortion")
        # plt.plot(df["Centroids"], df["Distortion"], c=df["M"].map(colors))

        handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=v, label=k, markersize=8) for k, v in
                   colors.items()]
        ax.legend(title='Subvector size', handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.title(metric)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join('plots', metric + '.svg'))
        #plt.show()


if __name__ == "__main__":
    perf_df = parse_perf_output("./perf_output")
    plot_metrics(perf_df)
