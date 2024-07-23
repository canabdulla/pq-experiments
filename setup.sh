#!/bin/bash

#SYSTEMDS_ROOT env needs to be set

#REMOVE COMMENT TO CLONE SYSTEMDS INTO CURRENT DIRECTORY AND SET ENV VARIABLE
#sudo apt install openjdk-11-jdk
#sudo apt install maven
#git clone https://github.com/apache/systemds.git systemds
#echo 'export SYSTEMDS_ROOT='$(pwd) >> ~/.bashrc
#echo 'export PATH=$SYSTEMDS_ROOT/bin:$PATH' >> ~/.bashrc

#MANUALLY SET SYSTEMDS ENV
SYSTEMDS_ROOT="$HOME/projects/systemds"

dir=$(pwd)
cd "$SYSTEMDS_ROOT" || exit
mvn clean package -P distribution
cd "$dir" || exit
cp "$SYSTEMDS_ROOT"/target/SystemDS.jar .
rm -rf lib
cp -r "$SYSTEMDS_ROOT"/target/lib/ ./