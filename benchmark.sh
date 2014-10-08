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
    env=/usr/bin/env
    time='time'
    echo "Under Mac OS casapy cannot be started from a script. I will prepare "
    echo "the data for benchmark testing and give you the commands for "
    echo "executing the tests."
    prepOnly=1 
elif [ `uname` = 'Linux' ]
then
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
    $extractScript -b $CASAGuideURL >> $extractLog 2>> $extractLog
    # Get name of output Python script (this is the newest python script in pwd)
    local scriptName=`\ls -1t *.py | head -n 1`
    # Set name for log file
    local logName="../$scriptName.log"
    # Begin test
    execCommand="$env $time casapy -r $casapyVersion --nologger --nogui -c $scriptName >> $logName 2>> $logName"
    echo prepOnly = $prepOnly
    if [ ! "$prepOnly" ]
    then
        echo -e "Beginning benchmark test of $scriptName.\nLogging to ${logName##*/}"
        date >> $logName
        $execCommand
        local sumName=`\ls -1t *.summary | head -n 1`
        echo -e "\n" >> ../$sumName; cat $sumName >> ../$sumName
        echo "Finished test of $scriptName"
    else
        echo Manually start test with command:
        echo $execCommand
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
            tarball=`basename $dataPath`
        else
            echo "Data available by filesystem"
            tarball=$dataPath
        fi
    fi
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
casapyVersion=4.1.0 # default casapy version
while getopts 'udxhpr:' OPTION
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
    r)  casapyVersion="$OPTARG"
        ;;
    ?|h)  printf "Usage: %s [-u] [-c] [-p] [-r version] CASAGuideName\n" $(basename $0) >&2
        echo "  CASAGuideName = Name of CASA Guide from list below" >&2
        echo "  -u = get data by HTTP rather than filesystem" >&2
        echo "  -x = use extracted data; do not download; do not extract" >&2
        echo "  -d = do not download; use tarball in current directory" >&2
        echo "  -p = prepare the data only; do not run test" >&2
        echo "  -r VERSION = use specific casapy VERSION" >&2
        echo "  -h = print usage instructions and exit" >&2
        echo "" >&2
        echo "  Available CASA Guide Names:" >&2
	echo "  NGC3256Band3_42  TWHydraBand7_42  AntennaeBand7_42  IRASBand9_42  (CASA 4.2)" >&2
        echo "  NGC3256Band3_41  TWHydraBand7_41  AntennaeBand7_41  (CASA 4.1)" >&2
        echo "  NGC3256Band3     TWHydraBand7     AntennaeBand7     (CASA 4.0)" >&2
        echo "  NGC3256Band3_34  TWHydraBand7_34  AntennaeBand7_34  (CASA 3.4)" >&2
        echo "" >&2
        echo "  Scripts for internal testing:" >&2
        echo "  2011_0_00099_S                                      (CASA 4.0)" >&2
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
fi
paramSet=$1

# Source the parameter set file.
source parameters.sh

# Set parameters specified on the command line by calling the function of the
# same name. Exit if the function does not exist.
if type $paramSet > /dev/null
then
    $paramSet
else
    echo "Parameter set does not exist: $paramSet"
    exit 1
fi

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
    casaGuidesTest extractCASAscript.py $URL $prepOnly
done
cd ..
echo "Benchmark wrapper finished."
