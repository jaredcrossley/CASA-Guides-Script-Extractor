#!/bin/env bash
#
# Functions for CASA Guides benchmark testing.
#
# Import these functions into another bash script by calling '. benchmark.bash'.
#

# Perform general CASA Guides benchmark testing.
# PARAMETERS:
#   1) extractScript = path to CASA Guides script extractor
#   2) CASAGuideURL = URL to CASA Guide
function casaGuidesTest ()
{
    extractScript=$1
    CASAGuideURL=$2
    # Extract script from CASA Guide:
    extractLog=`basename $extractScript`.log
    python $extractScript $CASAGuideURL benchmark >> $extractLog 2>> $extractLog
    # Get name of output Python script (this is the newest python script in pwd)
    local scriptName=`ls -1t *.py | head -n 1`
    # Set name for log file
    local logName=../$scriptName.log
    # Begin test
    echo "Beginning benchmark test of $scriptName"
    echo "Logging to $logName"
    date >> $logName
    /bin/env time -v casapy-stable --nogui -c $scriptName >> $logName 2>> $logName
    local sumName=`ls -1t *.summary | head -n 1`
    cat $sumName >> ../$sumName
    echo "Finished test of $scriptName"
}

# Benchmark test data extraction.
# PARAMETERS:
#   1) dataPath = URL or filesystem path to compressed data
#   2) outFile = file to hold output of 
function extractionTest ()
{
    dataPath=$1
    outFile=$2
    # If dataPath is a URL, download data.
    if [[ ${dataPath} == http* ]]
    then
        echo "Acquiring data by HTTP"
        date >> $outFile
        /bin/env time -v wget -N -q $dataPath >> $outFile 2>> $outFile
        dataPath=`basename $dataPath`
    else
        echo "Data available by filesystem"
    fi
    echo "Extracting data. Logging to $outFile"
    date >> $outFile
    /bin/env time -v tar xzf $dataPath >> $outFile 2>> $outFile
    dir=`basename $dataLustre .tgz`
}
