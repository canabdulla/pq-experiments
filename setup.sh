#!/bin/bash

#SYSTEMDS_ROOT env needs to be set

dir=$(pwd)
cd "$SYSTEMDS_ROOT" || exit
mvn clean package -P distribution
cd "$dir" || exit
cp "$SYSTEMDS_ROOT"/target/SystemDS.jar .
rm -rf lib
cp -r "$SYSTEMDS_ROOT"/target/lib/ ./