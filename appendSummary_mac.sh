#!/bin/env bash
#
# Append *.summary files to files of the same name in the parent directory.
# On Mac, casapy cannot be exeucted from a script; after manual execution,
# use this script to update the summary files.

for file in `ls *.summary`
do
    echo "Appending summary to ../$file"
    cat $file >> ../$file
done
