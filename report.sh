#!/bin/env bash
#
# Call report.py for all machines.
#
# This script collects the output of report.py for all machines.  It 
# sort the table, adds a header and sends output to stdout. Review command
# line options using -h:
#
#   report.sh -h
#

pattern="'*.summary'"
output=.report.out 

# Handle command line options (there's only one right now!)
csv=
while getopts 'ch' OPTION
do
    case $OPTION in
    c)  csv='-c' # Use CSV format
        ;;
    ?|h)  printf "Usage: %s [-c] [-h]\n" $(basename $0) >&2
        echo "  -c = output report in comma separated variable format" >&2
        echo "  -h = print usage instructions and exit" >&2
        exit 2
        ;;
    esac
done
shift $(($OPTIND -1))

# Call report.py for each machine; specify location test output for each.
ssh gauss report.py -e ${csv} /export/data_2/jcrossle/benchmark/$pattern > $output
ssh boromir report.py -e ${csv} /export/raid0/jcrossle/benchmark/$pattern >> $output
ssh gluttony report.py -e ${csv} /export/raid5/jcrossle/benchmark/$pattern >> $output
ssh multivac08 report.py -e ${csv} /lustre/naasc/jcrossle/benchmark/$pattern >> $output
ssh beefy report.py -e ${csv} /users/jcrossle/casa/benchmark/beefy/$pattern >> $output
ssh kwaltz report.py -e ${csv} /Users/jcrossle/benchmark/work/$pattern >> $output
# ssh antares $linuxReport /export/data_1/jcrossle/benchmark/$pattern >> $output
# ssh arkleseizure $macReport /Users/jcrossle/NRAO/casa/benchmark_work/$pattern >> $output

# Sort report table
cp $output $output.bkup
sort $output.bkup > $output
rm $output.bkup

# Write table to STDOUT
report.py --headeronly ${csv}
cat $output
rm $output
