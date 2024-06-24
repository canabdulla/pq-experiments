#!/bin/bash

./install_dependencies.sh
./download_data.sh
./prepare_inputs.sh
./run_distortion.sh
./run_logistic_regression.sh
python3 plotting/plot_all.py dist
python3 plotting/plot_all.py ml
