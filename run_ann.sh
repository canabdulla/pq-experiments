#!/bin/bash
CMD="java -Xmx12g -Xms12g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
#enable codegeneration
CONF=" -config dataprep/SystemDS-config.xml" #just for faster training (~7x)

#run the ann tests with perf. results are saved in output/ann and perf_output/ann
run_ann() {
  local alg=$1
  if [ "$alg" = "PQ" ]; then
      space_decomp="FALSE"
  else
      space_decomp="TRUE"
  fi
  file="ann/$alg $dataset $M $subcentroids TRUE"
  #start timer
  start=$(date +%s%N)
  #execute dml script with perf
  sudo perf stat -x \; -o "./perf_output/$file" -d -d -d \
  $CMD -f experiments/ann_test.dml -exec singlenode -stats \
      -nvargs M=$M subcentroids=$subcentroids  out_file="$file" space_decomp=$space_decomp
  #calculate execution time
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  #append execution time to output
  if [ -f "./output/$file" ]; then
      sed -i s/$/,"$time"/ "./output/$file"
  fi
}

#run the ann tests for different parameters
execute_runs() {
  local M_list=$1
  local c_list=$2
  dataset=$3
  #run product quantization
  for subcentroids in $c_list; do
    for M in $M_list; do
        run_ann PQ
        run_ann PQ-SPACEDECOMP
    done
  done
}

#clean the output directory
rm -f output/ann/*
rm -f perf_output/ann/*

application="ann"
execute_runs "1 2 4 8 16" "8 16 32 64 128 256 512 1024 2048" "siftsmall_base"

#remove metadata file to ensure correct parsing of outputs
rm -f output/ann/*.mtd
#parse all of the outputs to a single csv file. if it already the results are appended
python3 parse_outputs.py ann
