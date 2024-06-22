import os
import sys

import numpy as np
import pandas as pd
import datetime
import platform
import cpuinfo

def save_csv(data, dest):
    df = pd.DataFrame(data,
                      columns=["algorithm", "dataset", "M", "subcentroids", "separate", 'metric', 'value'])
    df["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    processor = cpuinfo.get_cpu_info()["brand_raw"]
    df["processor"] = processor
    if not os.path.isfile(dest):
        df.to_csv(dest, header=True, index=False)
    else:
        df.to_csv(dest, mode='a', header=False, index=False)

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
    return data


def parse_dist_output(output_dir):
    data = []
    for filename in os.listdir(output_dir):
        val = np.loadtxt(open(os.path.join(output_dir, filename), "rb"), delimiter=",")
        metrics = ["distortion", "ms"]
        for i in range(len(val)):
            testcase = os.path.splitext(filename)[0].split()
            testcase.append(metrics[i])
            testcase.append(val[i])
            data.append(testcase)
    return data


def parse_ml_output(output_dir):
    data = []
    for filename in os.listdir(output_dir):
        dataset = filename.split(' ')[1]
        if dataset == 'KDD98':
            metrics = ["mse", "ms"]
        else:
            metrics = ["accuracy", "avg-precision", "avg-recall", "macro-f1", "ms"]
        val = np.loadtxt(open(os.path.join(output_dir, filename), "rb"), delimiter=",")
        for i in range(len(val)):
            testcase = os.path.splitext(filename)[0].split()
            testcase.append(metrics[i])
            testcase.append(val[i])
            data.append(testcase)
    return data


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_outputs.py <test_case>")
        return
    if sys.argv[1] == "dist":
        data = parse_dist_output("output/distortion")
        perf_data = parse_perf_output("perf_output/distortion")
        data.extend(perf_data)
        save_csv(data, "results/distortion.csv")
    elif sys.argv[1] == "ml":
        # perf_data = parse_perf_output("perf_output/ml")
        data = parse_ml_output("output/ml")
        perf_data = parse_perf_output("perf_output/ml")
        data.extend(perf_data)
        save_csv(data, "./results/ml.csv")


if __name__ == '__main__':
    main()
