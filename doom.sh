#!/bin/env bash
# AUTHOR: Anand Crossle (jcrossle@nrao.edu)
# LICENSE: GPLv3

# one script to rule them all... 

echo "--> Kicking off NGC3256 test"
benchmark.sh $@ NGC3256Band3_41

echo "--> Kicking off TWHydra test"
benchmark.sh $@ TWHydraBand7_41

echo "--> Kicking off Antennae test"
benchmark.sh $@ AntennaeBand7_41

echo "--> Kicking off 2011_0_00099_S test"
benchmark.sh $@ 2011_0_00099_S

# # Does not yet work with script extractor!
# echo "--> Kicking off IRAS16239 test"
# $benchmark $1 $scriptDir/IRAS16293Band9.sh

# # Runs under CASA 3.3
# echo "--> Kicking off M100 test"
# $benchmark $1 $scriptDir/M100Band3.sh

# # Runs under CASA 3.3
# echo "--> Kicking off SgrA test"
# $benchmark $1 $scriptDir/SgrABand6.sh
