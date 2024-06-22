#!/bin/bash
calc_dist=TRUE

CMD="java -Xmx12g -Xms12g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config exp/dataprep/SystemDS-config.xml" #just for faster training (~7x)

#sudo rm output/distortion/*
#sudo rm perf_output/distortion/*

run_perf() {
  local pq=${2}
  start=$(date +%s%N)
  file="distortion/$1 $dataset $M $subcentroids $sep"
  sudo perf stat -x \; -o "./perf_output/$file" -d -d -d $CMD -f distortion_test.dml -exec singlenode -stats \
      -nvargs dataset=$dataset M=$M calc_dist=$calc_dist subcentroids=$subcentroids pq=$pq sep=$sep application=$application
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  if [ ! -f "./output/$file" ]; then
      echo "$1 $dataset M=$M subcentroids=$subcentroids sep=$sep" >> failed_distortion_runs.txt
  else
      echo "$1 $dataset M=$M subcentroids=$subcentroids sep=$sep" >> successful_distortion_runs.txt
      sed -i s/$/,"$time"/ "./output/$file"
  fi
}

execute_runs() {
  local M_list=$1
  local c_list=$2
  dataset=$3
  for centroids in $c_list; do
    #run product quantization
    for M in $M_list; do
      subcentroids=$((centroids / M))
      echo "$centroids $subcentroids $M"
      for sep in FALSE TRUE ; do
        run_perf PQ TRUE
      done
    done
    #run kmeans
    sep=FALSE
    subcentroids=$centroids
    M=1
    run_perf K-Means FALSE
  done
}

application="ann"
execute_runs "1 2 4 8" "8 16 32 64 128 256" "sift_base_100k"

#application="ml"
#execute_runs "1 2 4" "4 8 16 32 64 128" "Adult"
#execute_runs "1 2 4" "4 8 16 32" "Covtype"
#execute_runs "1 2 4 8" "8 16 32 64 128 256" "KDD98"

rm -f output/distortion/*.mtd
python3 parse_outputs.py dist