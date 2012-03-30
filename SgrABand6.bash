#!/bin/env bash

# Benchmark wrapper for SgrA Band 6.

# Inputs
benchmarkScript='/users/jcrossle/casa/benchmark/benchmark.bash'
extractScript='/users/jcrossle/casa/benchmark/extractCASAscript.py'
calibrationScriptURL='https://almascience.nrao.edu/almadata/sciver/SgrABand6/SgrA_Band6_Calibration.py'
imagingScriptURL='https://almascience.nrao.edu/almadata/sciver/SgrABand6/SgrA_Band6_Imaging.py'
dataURL='https://almascience.nrao.edu/almadata/sciver/SgrABand6/SgrA_Band6_UnCalibratedMSAndTablesForReduction.tgz'
#dataLustre='/export/lustre/SV/AntennaeBand7/Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz'
extractBenchmark='SgrABand6.extract.benchmark'

# Handle command line options
useURL=
useCWD=
while getopts 'b:uc' OPTION
do
    case $OPTION in
    b)  scriptDir="$OPTARG"
        echo "Using scripts in $scriptDir"
        benchmarkScript=$scriptDir/benchmark.bash
        extractScript=$scriptDir/extractCASAscript.py
        ;;
    u)  useURL=1 # Get data by HTTP; else filesystem
        ;;
    c)  useCWD=1 # Use data in CWD; do not download
        ;;
    ?)  printf "Usage: %s [-b scriptDir] [-u -c]\n" $(basename $0) >&2
        echo "  scriptDir = directory containing benchmarking scripts" >&2
        echo "  -u = get data by HTTP rather than filesystem" >&2
        echo "  -c = use data in current working directory; do not download" >&2
        exit 2
        ;;
    esac
done
shift $(($OPTIND -1))

# Import functions
. $benchmarkScript

# Extract data
if [ ! "$useCWD" ]
then
    extractionTest $dataURL $extractBenchmark
fi
dir=`basename $dataURL .tgz`
cd $dir

# Run casa guides tests
for URL in $calibrationScriptURL $imagingScriptURL
do
    casaGuidesTest $extractScript $URL
done

cd ..
echo "Benchmark wrapper finished."
