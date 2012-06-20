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

linuxReport=/users/jcrossle/casa/benchmark/report.py
macReport=/Users/jcrossle/NRAO/casa/benchmark_code/report.py
pattern="'*.summary'"
output=$1

ssh gauss $linuxReport /export/data_1/jcrossle/benchmark/$pattern > $output
ssh boromir $linuxReport /export/raid0/jcrossle/benchmark/$pattern >> $output
ssh gluttony $linuxReport /export/data_1/jcrossle/benchmark/$pattern >> $output
ssh multivac08 $linuxReport /export/lustre/jcrossle/benchmark/$pattern >> $output
ssh arkleseizure $macReport /Users/jcrossle/NRAO/casa/benchmark_work/$pattern >> $output

cp $output $output.bkup
echo "              Script Name         Host  AvgTime  StDTime Runtimes (s)" > $output
echo "------------------------- ------------ -------- -------- ------------" >> $output
sort $output.bkup >> $output
rm $output.bkup
