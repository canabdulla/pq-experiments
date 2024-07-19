#!/bin/bash

mkdir -p data;
chmod 755 data;

mkdir -p ./data/ann
mkdir -p ./data/ml

mkdir -p ./output/distortion
mkdir -p ./output/ml
mkdir -p ./output/ann
mkdir -p ./output/bs

mkdir -p ./results

mkdir -p ./perf_output/ml
mkdir -p ./perf_output/distortion
mkdir -p ./perf_output/ann
mkdir -p ./perf_output/bs

mkdir -p ./plots/distortion/line/perf
mkdir -p ./plots/distortion/bar/perf
mkdir -p ./plots/ml/bar/perf
mkdir -p ./plots/ml/line/perf
mkdir -p ./plots/ann/line/perf
mkdir -p ./plots/ann/bar/perf
mkdir -p ./plots/bs/line/perf
mkdir -p ./plots/bs/bar/perf

sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`
sudo apt install unzip
pip install numpy
pip install matplotlib
pip install pandas
pip install tables
pip install seaborn
