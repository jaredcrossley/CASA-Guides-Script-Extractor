#!/bin/env bash
#
# Benchmark testing script. Review command line options and arguments by using
# option -h:
#
#   benchmark.sh -h
#

# Set variables, command, options that are different on Mac and RedHat.
if [ `uname` = 'Darwin' ]
then 
    benchmarkDir="$HOME/NRAO/casa/benchmark_code"
    env=/usr/bin/env
    time='time'
elif [ `uname` = 'Linux' ]
then
    benchmarkDir="$PWD"
    env='/bin/env'
    time='time -v'
else
    echo "Error: OS type not identified."
    exit 1
fi

# Perform general CASA Guides benchmark testing.
# PARAMETERS:
#   1) extractScript = path to CASA Guides script extractor
#   2) CASAGuideURL = URL to CASA Guide
#   3) prepOnly = boolean; if true, only prepare directory, do not execute test
function casaGuidesTest ()
{
    extractScript=$1
    CASAGuideURL=$2
    prepOnly=$3
    # Extract script from CASA Guide:
    extractLog=`basename $extractScript`.log
    echo -e "Extracting CASA Guide.\nLogging to $extractLog"
    python $extractScript -b $CASAGuideURL >> $extractLog 2>> $extractLog
    # Get name of output Python script (this is the newest python script in pwd)
    local scriptName=`\ls -1t *.py | head -n 1`
    # Set name for log file
    local logName="../$scriptName.log"
    # Begin test
    if [ ! "$prepOnly" ]
    then
        echo -e "Beginning benchmark test of $scriptName.\nLogging to ${logName##*/}"
        date >> $logName
        $env $time casapy -r 4.0.0 --nologger --nogui -c $scriptName >> $logName 2>> $logName
        local sumName=`\ls -1t *.summary | head -n 1`
        echo -e "\n" >> ../$sumName; cat $sumName >> ../$sumName
        echo "Finished test of $scriptName"
    fi
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
    if [ "$skipDownload" ]
    then
        # Check that the tarball actually exists
        tarball=`basename $dataPath`
        if [ ! -e $tarball ]; then
            echo "Cannot find tarball for extraction:"
            echo $tarball
            echo "Download may be required."
            exit 2
        fi
    else
        # Download data.
        if [[ ${dataPath} == http* ]]
        then
            echo -e "Acquiring data by HTTP.\nLogging to $outFile"
            date >> $outFile
            $env $time wget -N -q --no-check-certificate $dataPath >> $outFile 2>> $outFile
        else
            echo "Data available by filesystem"
            scp elwood:$dataPath ./
        fi
    fi
    tarball=`basename $dataPath`
    date >> $outFile
    # Mac tar does not have --recursive-unlink, so remove dir explicitly
    dirPath=`basename $dataPath .tgz`
    echo "Removing preexisting data."
    rm -rf $dirPath
    echo -e "Extracting data.\nLogging to $outFile"
    $env $time tar -x -z -f $tarball >> $outFile 2>> $outFile
}

# Handle command line options
useURL=
useCWD=
while getopts 'udxhp' OPTION
do
    case $OPTION in
    u)  useURL=1 # Get data by HTTP; else filesystem
        ;;
    x)  useCWD=1 # Use extracted data in CWD; do not download; do not extract
        ;;
    d)  skipDownload=1 # Do not download; use tarball in current directory
        ;;
    p)  prepOnly=1 # Prep the data for benchmark testing, but do not start test
        ;;
    ?|h)  printf "Usage: %s [-u] [-c] [-p] parameters\n" $(basename $0) >&2
        echo "  parameters = path to file containing test parameters" >&2
        echo "  -u = get data by HTTP rather than filesystem" >&2
        echo "  -x = use extracted data; do not download; do not extract" >&2
        echo "  -d = do not download; use tarball in current directory" >&2
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
        dataPath=$dataURL
    else
        extractionTest $dataPath
    fi
fi
dir=`basename $dataPath .tgz`
cd $dir

# Extract and run casa guides tests
for URL in $calibrationURL $imagingURL
do
    extractionScript=$benchmarkDir/extractCASAscript.py
    casaGuidesTest $extractionScript $URL $prepOnly
done
cd ..
echo "Benchmark wrapper finished."
