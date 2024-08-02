#!/bin/bash

CMD="java -Xmx22g -Xms22g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
#enable codegeneration
CONF=" -config dataprep/SystemDS-config.xml"

#sudo -v
#run the regression tests with perf. results are saved in output/ml and perf_output/ml
run_dml() {
  local alg=$1
  if [ "$alg" = "PQ" ]; then
      pq="TRUE"
      space_decomp="FALSE"
  elif [ "$alg" = "PQ-SPACEDECOMP" ]; then
      pq="TRUE"
      space_decomp="TRUE"
  else
      pq="FALSE"
      space_decomp="FALSE"
  fi
  if [ "$case" = "clustering" ]; then
     script="experiments/compute_codes.dml"
  else 
     script="experiments/logistic_regression.dml"
  fi
#  local script=$2
  file="ml/$alg $dataset $M $subcentroids $sep"
  start=$(date +%s%N)
  #execute dml script with perf
  sudo perf stat -x \; -o "./perf_output/$file $case" -d -d -d \
   $CMD -f $script -exec singlenode -stats \
   -nvargs dataset="$dataset" M=$M subcentroids=$subcentroids pq=$pq sep=$sep out_file="$file" space_decomp=$space_decomp
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  #append execution time to output
  sed -i "$ a\\$time;ms;time;;;;" "./perf_output/$file $case"
}

#run the regression tests for different parameters
execute_pq_runs() {
  local M_list=$1
  local c_list=$2
  local dataset=$3
  #execute product quantization
  for M in $M_list; do
    for centroids in $c_list; do
      subcentroids=$((centroids / M))
      for sep in FALSE TRUE; do
        run_dml PQ $case
        run_dml PQ-SPACEDECOMP $case
      done
    done
  done
}

execute_baseline_run() {
  #execute baseline
  M=0
  subcentroids=0
  sep=FALSE
  run_dml Baseline
}

#clean the output directory
rm -f output/ml/*
rm -f perf_output/ml/*

#execute pq iterations
for case in "clustering" "regression"; do
  execute_pq_runs "1 2 4" "4 8 16 32 64 128 256" "Adult"
  execute_pq_runs "1 2 4 8" "8 16 32 64 128 256" "Covtype"
  execute_pq_runs "1 2 4 8" "8 16 32 64 128 256" "KDD98"
done

#execute baseline
case=regression
for dataset in "Adult" "Covtype" "KDD98"; do
  execute_baseline_run
done



#remove metadata file to ensure correct parsing of outputs
rm -f output/ml/*.mtd
#parse all of the outputs to a single csv file. if it already the results are appended
python3 parse_outputs.py ml
