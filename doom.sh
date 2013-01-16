#!/bin/env bash
# AUTHOR: Anand Crossle (jcrossle@nrao.edu)
# LICENSE: GPLv3

# one script to rule them all... to rule most... uh, to rule some...

# Set scriptDir to the directory containing the script extractor
# source code.  Comment or uncomment code as you desire.

echo Where would you like CASA tarballs, data and log files to
echo be located?  Please pick a spot with a large amount of space
echo
DESTDIR="$PWD"
read -p "[$DESTDIR]: " TDIR
if [ "$TDIR" != "" ]; then
    DESTDIR="$TDIR"
fi
echo
while [ ! -d "$DESTDIR" ]; do
    echo Warning, $DESTDIR is not a directory. Should we create
    echo it?
    read -p "[yes/no]: " CONFIRM
    if [ "$CONFIRM" == "yes" ]; then
        mkdir -p $DESTDIR
        if [ $? -ne 0 ]; then
            echo Could not create $DESTDIR , probably a permissions issue
            echo Aborting script.
            exit 1
        fi
    fi
    
done

scriptDir="$PWD"
if [ ! -e $scriptdir ]; then
    mkdir -p $scriptdir
fi

PYTHONPATH=$scriptDir:$PYTHONPATH
export PYTHONPATH

benchmark=$scriptDir/benchmark.sh

echo "--> Kicking off NGC3256 test"
$benchmark $1 $scriptDir/NGC3256Band3.sh

echo "--> Kicking off TWHydra test"
$benchmark $1 $scriptDir/TWHyaBand7.sh

echo "--> Kicking off Antennae test"
$benchmark $1 $scriptDir/AntennaeBand7.sh

# # Runs under CASA 3.3
# echo "--> Kicking off M100 test"
# $benchmark $1 $scriptDir/M100Band3.sh

# # Runs under CASA 3.3
# echo "--> Kicking off SgrA test"
# $benchmark $1 $scriptDir/SgrABand6.sh

# # Does not yet work with script extractor!
# echo "--> Kicking off IRAS16239 test"
# $benchmark $1 $scriptDir/IRAS16293Band9.sh
