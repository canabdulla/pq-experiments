#!/bin/bash
calc_dist=TRUE

CMD="java -Xmx24g -Xms24g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
#enable codegeneration
CONF=" -config dataprep/SystemDS-config.xml" #just for faster training (~7x)

#run the distortion tests with perf. results are saved in output/distortion and perf_output/distortion
run_distortion() {
  local alg=${1}
  if [ "$alg" = "PQ" ]; then
      pq="TRUE"
  else 
      pq="FALSE"
  fi
  file="distortion/$alg $dataset $M $subcentroids $sep"
  #start timer
  start=$(date +%s%N)
  #execute dml script with perf
  sudo perf stat -x \; -o "./perf_output/$file" -d -d -d \
   $CMD $CONF -f experiments/distortion_test.dml -exec singlenode -stats \
      -nvargs dataset=$dataset M=$M calc_dist=$calc_dist subcentroids=$subcentroids pq=$pq sep=$sep application=$application out_file="$file"
  #calculate execution time
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  #append execution time to output
  if [ -f "./output/$file" ]; then
      echo "$alg $dataset M=$M subcentroids=$subcentroids sep=$sep" >> successful_distortion_runs.txt
      sed -i s/$/,"$time"/ "./output/$file"
  else
      echo "$alg $dataset M=$M subcentroids=$subcentroids sep=$sep" >> failed_distortion_runs.txt
  fi
}

#run the distortion tests for different parameters
execute_runs() {
  local M_list=$alg
  local c_list=$2
  dataset=$3

  #run product quantization
  for centroids in $c_list; do
    for M in $M_list; do
      subcentroids=$((centroids / M))
      for sep in FALSE TRUE ; do
        run_distortion PQ
      done
    done
    #run kmeans
    sep=FALSE
    subcentroids=$centroids
    M=1
    run_distortion K-Means
  done
}

#clean the output directory
rm -f output/distortion/*
rm -f perf_output/distortion/*

application="ann"
execute_runs "1 2 4 8" "8 16 32 64 128 256" "sift_base_100k"

application="ml"
execute_runs "1 2 4" "4 8 16 32 64 128 256" "Adult"
execute_runs "1 2 4 8" "8 16 32" "Covtype"
execute_runs "1 2 4 8" "8 16 32 64 128 256" "KDD98"

#remove metadata file to ensure correct parsing of outputs
rm -f output/distortion/*.mtd
#parse all of the outputs to a single csv file. if it already the results are appended
python3 parse_outputs.py dist