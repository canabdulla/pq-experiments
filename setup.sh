#!/bin/bash

#SYSTEMDS_ROOT env needs to be set
sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`
pip install numpy
pip install matplotlib
pip install pandas
pip install h5py
pip install tables

dir=$(pwd)
cd "$SYSTEMDS_ROOT" || exit
mvn clean package -P distribution
cd "$dir" || exit
cp "$SYSTEMDS_ROOT"/target/SystemDS.jar .
rm -rf lib
cp -r "$SYSTEMDS_ROOT"/target/lib/ ./