#!/bin/bash

CMD="java -Xmx10g -Xms10g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
#enable codegeneration
CONF=" -config dataprep/SystemDS-config.xml"

#sudo -v
#run the regression tests with perf. results are saved in output/ml and perf_output/ml
run_reg() {
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

  file="ml/$alg $dataset $M $subcentroids $sep"
  start=$(date +%s%N)
  #execute dml script with perf
  sudo perf stat -x \; -o "./perf_output/$file" -d -d -d \
   $CMD $CONF -f experiments/logistic_regression.dml -exec singlenode -stats \
   -nvargs dataset="$dataset" M=$M subcentroids=$subcentroids pq=$pq sep=$sep out_file="$file" space_decomp=$space_decomp
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  #append execution time to output
  if [ -f "./output/$file" ]; then
      echo "$alg $dataset M=$M subcentroids=$subcentroids sep=$sep" >> successful_ml_runs.txt
      sed -i s/$/,"$time"/ "./output/$file"
  else
      echo "$alg $dataset M=$M subcentroids=$subcentroids sep=$sep" >> failed_ml_runs.txt
  fi
}

#run the regression tests for different parameters
execute_runs() {
  local M_list=$1
  local c_list=$2
  local dataset=$3
  #execute baseline
  M=0
  subcentroids=0
  sep=FALSE
  run_reg Baseline
  #execute product quantization
  for M in $M_list; do
    for centroids in $c_list; do
      subcentroids=$((centroids / M))
      for sep in FALSE TRUE; do
        run_reg PQ
        run_reg PQ-SPACEDECOMP
      done
    done
  done
}

#clean the output directory
rm -f output/ml/*
rm -f perf_output/ml/*

#clustering with 64 or more centroids causes kmeans to fail because the wcss is 0
execute_runs "1 2 4" "4 8 16 32 64 128 256" "Adult"
#execute_runs "1 2 4" "32" "Adult"
execute_runs "1 2 4 8" "8 16 32 64 128 256" "Covtype"
execute_runs "1 2 4 8" "8 16 32 64 128 256" "KDD98"


#remove metadata file to ensure correct parsing of outputs
rm -f output/ml/*.mtd
#parse all of the outputs to a single csv file. if it already the results are appended
python3 parse_outputs.py ml
