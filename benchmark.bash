#!/usr/bin/env bash
#
# Benchmark testing script. Review command line options and arguments by using
# option -h:
#
#   benchmark.bash -h
#

# Hardcoded parameters. These are necessary for moving between Linux and Mac.
# Mac:
benchmarkDir='/Users/jcrossle/NRAO/casa/benchmark_code'
env=/usr/bin/env
time='time'
tarExtract='tar -x -z -f'
# # Linux:
# benchmarkDir='/users/jcrossle/casa/benchmark'
# env='/bin/env'
# time='time -v'

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
    $env $time casapy --nogui -c $scriptName >> $logName 2>> $logName
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
    outFile=`basename $dataPath .tgz`.extraction.benchmark
    # If dataPath is a URL, download data.
    if [[ ${dataPath} == http* ]]
    then
        echo "Acquiring data by HTTP. Logging to $outFile"
        date >> $outFile
        $env $time wget -N -q --no-check-certificate $dataPath >> $outFile 2>> $outFile
        dataPath=`basename $dataPath`
    else
        echo "Data available by filesystem"
        scp elwood:$dataPath ./
        dataPath=`basename $dataPath`
    fi
    echo "Extracting data. Logging to $outFile"
    date >> $outFile
    # Mac tar does not have --recursive-unlink, so remove dir explicitly
    dirPath=`basename $dataPath .tgz`
    rm -rf $dirPath
    $env $time tar -x -z -f $dataPath >> $outFile 2>> $outFile
}

# Handle command line options
useURL=
useCWD=
while getopts 'uchp' OPTION
do
    case $OPTION in
    u)  useURL=1 # Get data by HTTP; else filesystem
        ;;
    c)  useCWD=1 # Use data in CWD; do not download; do not extract
        ;;
    p)  prepOnly=1 # Prep the data for benchmark testing, but do not start test
        ;;
    ?|h)  printf "Usage: %s [-u] [-c] [-p] parameters\n" $(basename $0) >&2
        echo "  parameters = path to file containing test parameters" >&2
        echo "  -u = get data by HTTP rather than filesystem" >&2
        echo "  -c = use extracted data in current working directory; do not download" >&2
        echo "  -p = prepare the data only; do not run test" >&2
        echo "  -h = print usage instructions and exit" >&2
        exit 2
        ;;
    esac
done
shift $(($OPTIND -1))

# Get parameters file name from command line.
if [ $# -ne 1 ]
then
    echo "Improper number of arguments." >&2
    exit 1
else
    parameters=$1
fi

# Read the parameter file. Which should contain these variables with string 
# values:
# calibrationURL = URL or path to calibration CASA guide or Python script
# imagingURL = URL or path to imaging CASA guide or Python script
# dataURL = URL to test data (used with -u option)
# dataPath = path to data on filesystem 
source $parameters

# Extract data
if [ ! "$useCWD" ]
then
    if [ "$useURL" ]
    then
        extractionTest $dataURL 
    else
        extractionTest $dataPath
    fi
fi
dir=`basename $dataPath .tgz`
cd $dir

# Run casa guides tests
if [ ! "$prepOnly" ]
then
    for URL in $calibrationURL $imagingURL
    do
        extractionScript=$benchmarkDir/extractCASAscript.py
        casaGuidesTest $extractionScript $URL
    done
fi
cd ..
echo "Benchmark wrapper finished."
