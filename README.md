# Product quantization - Experiments
# Project organization
The experiment pipeline for the different experiments consists of
multiple parts.

#### 1. The shell script `run_<testcase>.sh` located in the root folder
    This script runs multiple iterations with different parameters
    of the dml script described in `2.` 
#### 2. The dml script `experiments/<testcase>_test.dml`
    This script takes a number of different parameters 
    (e.g. the number of centroids) as an input and then executes 
    the experiment. The output of a single run is saved in the `output` and
    the `perf_output` folder in a single file. The name of the file is 
    a list of all of the parameters.
#### 3. The python script `parse_outputs.py`
    This script saves the output of the experiments stored in a large
    number of different files into a single file: `results/<testcase>.csv`
#### 4. Multiple python files for plotting located in `plotting/`
    The python file `plot_all.py` takes the created csv file as an input,
    plots all different metrics for the testcases
    and then saves the plots in
    `plots/`.
# Usage
Run `run_all.sh` to install all dependencies, execute all experiments,
save the outputs and plot the results.
```bash
./run_all.sh
```
## Manual Execution
### Installing Dependencies
```bash
./install_dependencies.sh
```
### Setup
```bash
./setup.sh
```
### Downloading the data
```bash
./download_data.sh
```
### Preparing the inputs
```bash
./prepare_inputs.sh
```
### Running the experiments
You can run the experiments independently by calling
`run_distortion.sh` `run_logistic_regression.sh` and 
`run_ann.sh` respectively. 
### Plotting
```bash
python3 plot_all.py <testcase>
```
To plot the results of the experiments you 
then have to call `python3 plotting/plot_all.py <testcase>` where
testcase is either ann, ml or dist.




