#!/bin/env bash

# one script to rule them all ...

scriptDir="/users/jcrossle/casa/benchmark"
benchmark=$scriptDir/benchmark.bash

echo "--> Kicking off NGC3256 test"
$benchmark $1 $scriptDir/NGC3256Band3.bash

echo "--> Kicking off TWHydra test"
$benchmark $1 $scriptDir/TWHyaBand7.bash

echo "--> Kicking off Antennae test"
$benchmark $1 $scriptDir/AntennaeBand7.bash

echo "--> Kicking off M100 test"
$benchmark $1 $scriptDir/M100Band3.bash

echo "--> Kicking off SgrA test"
$benchmark $1 $scriptDir/SgrABand6.bash
