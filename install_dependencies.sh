#!/bin/bash

mkdir -p data;
chmod 755 data;

mkdir -p ./data/ann
mkdir -p ./data/ml

mkdir -p ./output/distortion
mkdir -p ./output/ml

mkdir -p ./results/distortion
mkdir -p ./results/ml

mkdir -p ./perf_output/ml
mkdir -p ./perf_output/distortion

mkdir -p ./plots/distortion/line/perf
mkdir -p ./plots/distortion/bar/perf
mkdir -p ./plots/ml/bar/perf
mkdir -p ./plots/ml/line/perf

sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`
pip install numpy
pip install matplotlib
pip install pandas
pip install tables
pip install seaborn
