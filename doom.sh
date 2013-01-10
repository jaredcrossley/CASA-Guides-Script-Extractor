#!/bin/env bash

# one script to rule them all... to rule most... uh, to rule some...

# Set scriptDir to the directory containing the script extractor
# source code.  Comment or uncomment code as you desire.

scriptDir="/users/jcrossle/casa/benchmark"
benchmark=$scriptDir/benchmark.bash

echo "--> Kicking off NGC3256 test"
$benchmark $1 $scriptDir/NGC3256Band3.bash

echo "--> Kicking off TWHydra test"
$benchmark $1 $scriptDir/TWHyaBand7.bash

echo "--> Kicking off Antennae test"
$benchmark $1 $scriptDir/AntennaeBand7.bash

# # Runs under CASA 3.3
# echo "--> Kicking off M100 test"
# $benchmark $1 $scriptDir/M100Band3.bash

# # Runs under CASA 3.3
# echo "--> Kicking off SgrA test"
# $benchmark $1 $scriptDir/SgrABand6.bash

# # Does not yet work with script extractor!
# echo "--> Kicking off IRAS16239 test"
# $benchmark $1 $scriptDir/IRAS16293Band9.bash
