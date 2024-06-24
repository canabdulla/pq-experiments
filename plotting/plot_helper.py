import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from parameters import *


def control_axis(metric, ax):
    if metric not in ["avg-precision", "avg-recall", "macro-f1", "accuracy"]:
        ax.set_ylim(ymin=0)
    else:
        ax.set_ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.2))


def add_legend_M(M_list, ax, type, baseline):
    if baseline:
        handles = [Line2D([0], [0], linestyle="--", color="r", label="baseline")]
    else:
        handles = []
    handles.extend([Line2D([0], [0], marker=markers[m] if not type == "bar" else 's', color='w',
                           markerfacecolor=colors_M[m], label=f"M={m}",
                           markersize=8) for m in
                    M_list])
    ax.legend(handles=handles, loc='center', bbox_to_anchor=(1.12, 0.9), facecolor='white')


def add_legend_dataset(ax, dataset):
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    props = dict(boxstyle='round', facecolor='white', alpha=0.5, edgecolor='grey')
    ax.text(1.02, 0.6, ds_desc[dataset], transform=ax.transAxes, bbox=props)


def add_legend_sep(M, ax, baseline):
    if baseline:
        handles = [Line2D([0], [0], linestyle="--", color="r", label="baseline")]
    else:
        handles = []
    handles.extend([Line2D([0], [0], marker='s', color='w',
                           markerfacecolor=colors_sep[s], label=f"Separate={s}",
                           markersize=8) for s in
                    {True, False}])
    ax.legend(handles=handles, loc='center', bbox_to_anchor=(1.17, 0.8), facecolor='white')


def save_plot(folder, sub_folder, dataset, metric, subtitle):
    title = f"{all_labels[metric]} {subtitle}"
    sub_sub_f = ""
    if metric in perf_labels:
        sub_sub_f = "perf/"
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"plots/{folder}/{sub_folder}/{sub_sub_f}{dataset} {title}.png", dpi=300, bbox_inches='tight')
    plt.close()
