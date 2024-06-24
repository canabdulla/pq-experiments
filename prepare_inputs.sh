#!/bin/bash

CMD="java -Xmx12g -Xms12g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config dataprep/SystemDS-config.xml"

$CMD -f dataprep/dataprep_adult.dml -exec singlenode -stats
$CMD -f dataprep/dataprep_KDD98.dml -exec singlenode -stats
$CMD -f dataprep/dataprep_covtype.dml -exec singlenode -stats $CONF
