#!/bin/bash

CMD="java -Xmx22g -Xms22g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
#enable codegeneration
CONF=" -config dataprep/SystemDS-config.xml"

#sudo -v

#run the bs tests with perf. results are saved in output/bs and perf_output/bs
run_bs() {
  local alg=${1}
  if [ "$alg" = "BASELINE_SAMPLING" ]; then
      pq="FALSE"
  else 
      pq="TRUE"
  fi
  file="$alg $dataset $M $subcentroids $sep"
  #start timer
  start=$(date +%s%N)
  #execute dml script with perf
  sudo perf stat -x \; -o "./perf_output/bs/$file" -d -d -d \
   $CMD -f experiments/baseline_sampling_test.dml -exec singlenode -stats \
      -nvargs dataset=$dataset M=$M subcentroids=$subcentroids pq=$pq sep=$sep application=$application out_file="$file"
  #calculate execution time
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  #append execution time to output
  #append execution time to output
  sed -i "$ a\\$time;ms;time;;;;" "./perf_output/bs/$file"
}

#run the bs tests for different parameters
execute_runs() {
  local M_list=$1
  local c_list=$2
  dataset=$3
  #run product quantization
  for M in $M_list; do
    subcentroids=0
    centroids=0
    sep=FALSE
    run_bs BASELINE_SAMPLING
    for centroids in $c_list; do
      subcentroids=$((centroids / M))
      for sep in FALSE TRUE ; do
        run_bs PQ
        run_bs PQ-SPACEDECOMP
      done
    done
  done
}

#clean the output directory
rm -f output/bs/*
rm -f perf_output/bs/*

application="bs"
execute_runs "1 2 4" "8 16 32 64 128 256" "Adult"

#remove metadata file to ensure correct parsing of outputs
rm -f output/bs/*.mtd
#parse all of the outputs to a single csv file. if it already the results are appended
python3 parse_outputs.py bs