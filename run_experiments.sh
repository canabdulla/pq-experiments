#!/bin/bash
#file="input/siftsmall_base.hdf5"
file="input/sift_base_100k.hdf5"
dataset=$(echo $file | sed -r "s/.+\/(.+)\..+/\1/")
sample_size=1000
calc_dist=TRUE
#centroids=64

sudo rm output/*
#sudo rm perf_output/*

run_perf() {
  local pq=${2}
  sudo perf stat -x \; -o "./perf_output/$1 $dataset $M $centroids $sample_size FALSE" -d -d -d systemds distortion_test.dml \
      -nvargs dataset=$dataset M=$M calc_dist=$calc_dist sample_size=$sample_size centroids=$centroids pq=$pq sep=FALSE
}

run_perf-l3() {
  local pq=${2}
  sudo perf stat -x \; -o "./perf_output/$1 $dataset $M $centroids $sample_size TRUE" --append \
       -e r0300C0000040FF04 -e r0300C00000400104 -e r430729 systemds distortion_test.dml  \
       -nvargs dataset=$dataset M=$M calc_dist=$calc_dist sample_size=$sample_size centroids=$centroids pq=$pq sep=TRUE
}
for centroids in 64 96 128 192 256; do
  #pq
  for M in 2 4 8 64 128; do
      run_perf pq TRUE
      #run_perf-l3 pq $dataset $M $centroids $sample_size TRUE
  done
  #kmeans as reference
  #run_perf kmeans FALSE
  sudo perf stat -x \; -o "./perf_output/kmeansssss $dataset $M $centroids $sample_size FALSE" -d -d -d systemds distortion_test.dml \
      -nvargs dataset=$dataset M=128 calc_dist=$calc_dist sample_size=50000 centroids=$centroids pq=FALSE sep=FALSE
done


sudo rm output/*.mtd
python3 plot_distortion.py
python3 plot_perf.py