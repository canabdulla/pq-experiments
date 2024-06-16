#!/bin/bash

CMD="java -Xmx24g -Xms24g -cp ./lib/*:./SystemDS.jar org.apache.sysds.api.DMLScript "
CONF=" -config exp/dataprep/SystemDS-config.xml"

$CMD -f exp/dataprep/dataprep_adult.dml -exec singlenode -stats
$CMD -f exp/dataprep/dataprep_KDD98.dml -exec singlenode -stats
$CMD -f exp/dataprep/dataprep_covtype.dml -exec singlenode -stats $CONF
