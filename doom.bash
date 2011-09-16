#!/bin/env bash

# one script to rule them all ...

scriptDir="/users/jcrossle/casa/benchmark"

echo "--> Kicking off NGC3256 test"
$scriptDir/NGC3256Band3.bash $1

echo "--> Kicking off TWHydra test"
$scriptDir/TWHyaBand7.bash $1

echo "--> Kicking off Antennae test"
$scriptDir/AntennaeBand7.bash $1
