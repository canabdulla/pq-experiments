import colorsys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors

from parameters import *

def darken_color(color):
    sat_factor = 1.2
    light_factor = 0.7
    rgb = mcolors.to_rgb(color)
    h, l, s = colorsys.rgb_to_hls(*rgb)
    s = min(1, s * sat_factor)
    l = max(0, min(1, l * light_factor))
    distinct_rgb = colorsys.hls_to_rgb(h, l, s)
    return mcolors.to_hex(distinct_rgb)


# Control the axis range.
def control_axis(metric, ax):
    if metric in [f"{j}-{i}" for j in ["test", "train"] for i in
                      ["precision", "recall", "avg-precision", "avg-recall", "macro-f1", "accuracy"]]:
        ax.set_ylim(0, 1)
    elif metric in ["test-rsq", "train-rsq"]:
        ax.set_ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.2))
    elif metric in ["recall"]:
        ax.set_ylim(0, 1)
    else:
        ax.set_ylim(ymin=0)


# Add a legend displaying a different number of subspaces.
def add_legend_M(M_list, ax, type, baseline, dataset):
    if baseline:
        handles = [Line2D([0], [0], linestyle="--", color="r", label="Baseline")]
    else:
        handles = []
    handles.extend([Line2D([0], [0], marker=markers[m] if not type == "bar" else 's', color='w',
                           markerfacecolor=colors_M[m], label=f"M={m}",
                           markersize=8) for m in
                    M_list])
    ax.legend(title=ds_desc[dataset], handles=handles, loc='best')


# Add a legend for different parameters of the implementation (e.g. quantizing separately vs. quantizing together)
def add_legend_comp(M, ax, baseline, comp_column, comp_values, dataset, color_offset):
    if baseline:
        handles = [Line2D([0], [0], linestyle="--", color="r", label="Baseline")]
    else:
        handles = []
    handles.extend([Line2D([0], [0], marker='s', color='w',
                           markerfacecolor=colors_comp[comp_values.index(c) + color_offset], label=f"{c}" if c not in comp_labels else f"{comp_labels[c]}",
                           markersize=8) for c in comp_values])
    comp_legend = ax.legend(title=ds_desc[dataset], handles=handles, loc='best')
    plt.gca().add_artist(comp_legend)


# Add the legend for baseline sampling plot.
def add_legend_bs(M, ax, baseline, comp_column, comp_values, dataset, color_map):
    if baseline:
        handles = [Line2D([0], [0], linestyle="--", color="r", label="Baseline")]
    else:
        # handles = [Rectangle((0,0), 1, 1, fc="w", fill=False, edgecolor="none", linewidth=0.5, label=f"{comp_column}")]
        handles = []
    handles.extend([Line2D([0], [0], marker='s', color='w',
                           markerfacecolor=color_map[comp_values.index(c)] if c != "Baseline Sampling" else "red", label=f"{c} centroids" if c != "Baseline Sampling" else f"{c}",
                           markersize=6) for c in comp_values])
    comp_legend = ax.legend(title=ds_desc[dataset], handles=handles, loc='best', prop={'size': 6}, title_fontproperties={'size': 6})
    plt.gca().add_artist(comp_legend)

# Save the plots
def save_plot(folder, sub_folder, dataset, metric, subtitle):
    file_name = f"{all_labels[metric]} {subtitle}"
    title = f"{all_labels[metric]}"
    sub_sub_f = ""
    if metric in perf_labels:
        sub_sub_f = "perf/"
    plt.title(title)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"plots/{folder}/{sub_folder}/{sub_sub_f}{dataset} {file_name}.png", dpi=300, bbox_inches='tight')
    plt.close()