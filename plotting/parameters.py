# Colors for different number of subspaces
colors_M = {1: "orange", 2: "dodgerblue", 4: "red", 8: "forestgreen", 16: "gold"}
colors_c = {0: "red", 1: "orange", 2: "dodgerblue", 4: "red", 8: "forestgreen", 16: "gold", 32: "green", 64: "blue",
            128: "purple", 256: "brown", 512: "pink", 1024: "yellow", 2048: "orange", 4096: "teal"}
markers = {1: "X", 2: "^", 4: "s", 8: "h", 16: "D"}
# Colors for the comparison of different parameters of the implementation
colors_comp = ["blue", "green", "red", "teal", "brown", "pink", "teal"]
# Legend labels for the comparison of different parameters of the implementation
comp_labels = {"PQ": "Without Space-D.", "PQ-SPACEDECOMP": "With Space-D.", True: "Separately", False: "Together"}

# Dataset descriptions
ds_desc = {
    "Adult": "Dataset: Adult \nnrow(X)=32,561 \nncol(X)=13",
    "Covtype": "Dataset: Covtype \nnrow(X)=581,012 \nncol(X)=54",
    "KDD98": "Dataset: KDD 98 \nnrow(X)=95,412 \nncol(X)=469",
    "sift_base_100k": "Dataset: SIFT \nnrow(X)=100,000 \nncol(X)=128",
    "gist_base_100k": "Dataset: GIST \nnrow(X)=100,000 \nncol(X)=128",
    "siftsmall_base": "Dataset: SIFT \nnrow(X)=10,000 \nncol(X)=128",
}

# Plot titles for performance metrics
labels = {
    "recall": "Recall@100",
    "distortion": "Distortion",
    "train-mse": "Mean Squared Error (Train)",
    "train-rsq": "R² (Train)",
    "test-mse": "Mean Squared Error (Test)",
    "test-rsq": "R² (Test)",
    "test-accuracy": "Accuracy (Test)",
    "test-avg-precision": "Average Precision (Test)",
    "test-precision": "Precision (Test)",
    "test-avg-recall": "Average Recall (Test)",
    "test-recall": "Recall (Test)",
    "test-macro-f1": "Macro F1 Score (Test)",
    "test-f1": "F1 Score (Test)",
    "train-accuracy": "Accuracy (Train)",
    "train-avg-precision": "Average Precision (Train)",
    "train-precision": "Precision (Train)",
    "train-avg-recall": "Average Recall (Train)",
    "train-recall": "Recall (Train)",
    "train-macro-f1": "Macro F1 Score (Train)",
    "train-f1": "F1 Score (Train)",
    "ms": "Execution Time [s]",
    "time": "Execution Time [s]",
    "mse": "Mean Squared Error"}

# Plot titles for perf statistics
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
    "L1-dcache-prefetches": "L1 Data Cache Prefetches",
    "task-clock": "Task Clock"
}
all_labels = labels
all_labels.update(perf_labels)
