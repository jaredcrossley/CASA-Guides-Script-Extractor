#!/bin/env bash
#
# Call report.py for all summary files.
#
# This simple script parses benchmark summaries from the hosts listed 
# below in the appropriate benchmarking directory on each host.  The 
# the parsed data is output as a sorted table. A header is appended.
#
# PARAMETERS:
#   1) output = output file name

report=/users/jcrossle/casa/benchmark/report.py
pattern="'*.summary'"
output=$1

ssh gauss $report /export/data_1/jcrossle/benchmark/$pattern > $output
ssh boromir $report /export/raid0/jcrossle/benchmark/$pattern >> $output
ssh gluttony $report /export/data_1/jcrossle/benchmark/$pattern >> $output
ssh multivac08 $report /export/lustre/jcrossle/benchmark/$pattern >> $output

cp $output $output.bkup
echo "              Script Name       Host  AvgTime  StDTime Runtimes (s)" > $output
echo "------------------------- ---------- -------- -------- ------------" >> $output
sort $output.bkup >> $output
rm $output.bkup
