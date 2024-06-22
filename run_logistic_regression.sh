#!/bin/bash

CMD="java -Xmx12g -Xms12g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config exp/dataprep/SystemDS-config.xml"

run_reg() {
  dataset=$2
  start=$(date +%s%N)
  file="ml/$1 $dataset $M $subcentroids $sep"
  sudo perf stat -x \; -o "./perf_output/ml/$1 $dataset $M $subcentroids $sep" -d -d -d \
   $CMD -f logistic_regression.dml \
   -nvargs dataset="$dataset" M=$M subcentroids=$subcentroids pq=$pq sep=$sep \
   -exec singlenode -stats
  end=$(date +%s%N)
  time=$((($end-$start) / 1000000 - 1500))
  if [ ! -f "./output/$file" ]; then
      echo "$1 $dataset M=$M subcentroids=$subcentroids sep=$sep" >> failed_ml_runs.txt
  else
      echo "$1 $dataset M=$M subcentroids=$subcentroids sep=$sep" >> successful_ml_runs.txt
      sed -i s/$/,"$time"/ "./output/$file"
  fi
#  sed -i s/$/,"$time"/ "./output/ml/$1 $dataset $M $subcentroids $sep"
}

execute_runs() {
  local M_list=$1
  local c_list=$2
  local dataset=$3

  #execute baseline
  pq=FALSE
  M=0
  subcentroids=0
  sep=FALSE
  run_reg Baseline "$dataset"

  pq=TRUE
  for M in $M_list; do
    for centroids in $c_list; do
      subcentroids=$((centroids / M))
      for sep in FALSE TRUE; do
        run_reg PQ "$dataset"
      done
    done
  done
}

rm -f output/ml/*
rm -f perf_output/ml/*

#clustering with 64 or more centroids causes kmeans to fail because the wcss is 0
execute_runs "1 2 4" "4 8 16 32 64 128 256" "Adult"
execute_runs "1 2 4 8" "8 16 32" "Covtype"
execute_runs "1 2 4 8" "8 16 32 64 128 256" "KDD98"

rm -f output/ml/*.mtd
python3 parse_outputs.py ml
