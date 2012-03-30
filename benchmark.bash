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
    python $extractScript -b $CASAGuideURL >> $extractLog 2>> $extractLog
    # Get name of output Python script (this is the newest python script in pwd)
    local scriptName=`\ls -1t *.py | head -n 1`
    # Set name for log file
    local logName="../$scriptName.log"
    # Begin test
    echo "Beginning benchmark test of $scriptName. Logging to ${logName##*/}"
    date >> $logName
    /bin/env time -v casapy --nogui -c $scriptName >> $logName 2>> $logName
    local sumName=`\ls -1t *.summary | head -n 1`
    cat $sumName >> ../$sumName
    echo "Finished test of $scriptName"
}

# Extract data for a benchmark test. Recursively remove any files or dirctories
# in the way so the newly extracted data set will be pristine.
# PARAMETERS:
#   1) dataPath = URL or filesystem path to compressed data
#   2) outFile = file to hold output of script
function extractionTest ()
{
    dataPath=$1
    outFile=$2
    # If dataPath is a URL, download data.
    if [[ ${dataPath} == http* ]]
    then
        echo "Acquiring data by HTTP. Logging to $outFile"
        date >> $outFile
        /bin/env time -v wget -N -q $dataPath >> $outFile 2>> $outFile
        dataPath=`basename $dataPath`
    else
        echo "Data available by filesystem"
    fi
    echo "Extracting data. Logging to $outFile"
    date >> $outFile
    /bin/env time -v tar --recursive-unlink -x -z -f $dataPath >> $outFile 2>> $outFile
}
