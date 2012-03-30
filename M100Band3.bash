#!/bin/env bash

# Benchmark wrapper for M100 Band 3.

# Inputs
benchmarkScript='/users/jcrossle/casa/benchmark/benchmark.bash'
extractScript='/users/jcrossle/casa/benchmark/extractCASAscript.py'
calibrationScriptURL='https://almascience.nrao.edu/almadata/sciver/M100Band3/M100_Band3_Calibration.py'
imagingScriptURL='https://almascience.nrao.edu/almadata/sciver/M100Band3/M100_Band3_Imaging.py'
dataURL='https://almascience.nrao.edu/almadata/sciver/M100Band3/M100_Band3_UnCalibratedMSAndTablesForReduction.tgz'
#dataLustre='/export/lustre/SV/AntennaeBand7/Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz'
extractBenchmark='M100Band3.extract.benchmark'

# Handle command line options
useURL=
while getopts 'b:u' OPTION
do
    case $OPTION in
    b)  scriptDir="$OPTARG"
        echo "Using scripts in $scriptDir"
        benchmarkScript=$scriptDir/benchmark.bash
        extractScript=$scriptDir/extractCASAscript.py
        ;;
    u)  useURL=1 # Get data by HTTP; else filesystem
        ;;
    ?)  printf "Usage: %s [-b scriptDir] [-u]\n" $(basename $0) >&2
        echo "  scriptDir = directory containing benchmarking scripts" >&2
        echo "  -u = get data by HTTP rather than filesystem" >&2
        exit 2
        ;;
    esac
done
shift $(($OPTIND -1))

# Import functions
. $benchmarkScript

# Extract data
extractionTest $dataURL $extractBenchmark
cd $dir

# Run casa guides tests
for URL in $calibrationScriptURL $imagingScriptURL
do
    casaGuidesTest $extractScript $URL
done

cd ..
echo "Benchmark wrapper finished."
