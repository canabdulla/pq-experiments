#!/bin/bash

./install_dependencies.sh
./download_data.sh
./prepare_inputs.sh
./run_distortion.sh
./run_logistic_regression.sh
./run_ann.sh
./run_baseline_sampling.sh
python3 plotting/plot_all.py dist
python3 plotting/plot_all.py ml
python3 plotting/plot_all.py ann
python3 plotting/plot_all.py bs
