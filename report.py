#!/bin/env python

import sys, re, numpy, glob
from optparse import OptionParser

def make_report( options, globPattern="./*.summary" ):
    """
    Generate a report from casa_call.summarize_bench output (.summary file).
    
    * options = command line options object
    * globPattern = pattern for matching summary files
    """
    # Print table header
    if options.header:
        print_header( options.csv )
    # Iterate through summary files
    files = glob.glob( globPattern )
    for file in files:
        fileObj = open(file)
        summary = fileObj.read()
        fileObj.close()
        # Get test name
        pattern = r'''Summary\ of\ file\ (.*).benchmark.*'''
        match = re.search( pattern, summary )
        testName = match.group(1)
        # Get host name
        pattern = r'''^(Linux|Darwin)\ ([^\ \.]+)'''
        match = re.search( pattern, summary, re.MULTILINE )
        hostname = match.group(2)
        # Get total times
        pattern = r'''^Total\ time:\ ([0-9\.]+)'''
        times = re.findall( pattern, summary, re.MULTILINE )
        for i,time in enumerate(times):
            times[i] = float(time) 
        avg = numpy.average(times)
        std = numpy.std(times)
        # Print summary
        print_row( testName, hostname, times, avg, std, options.csv )

def print_header( csv ):
    """ Print table header """
    format = ""
    if csv:
        format = "%33s, %12s, %8s, %8s, %s"
    else:
        format = "%33s %12s %8s %8s %s"
    print format % ('Script Name', "Host", "AvgTime", "StDTime", "Runtimes (s)")
    if not csv: 
        print format % ("-"*33, "-"*12, "-"*8, "-"*8, "-"*12)

def print_row( testName, hostname, times, avg, std, csv ):
    """ Print 1 row of the summary ASCII table. """
    rowFormat = ""; timeFormat = ""
    if csv:
        rowFormat = "%33s, %12s, %8.1f, %8.1f,"
        timeFormat = "%d, "
    else:
        rowFormat = "%33s %12s %8.1f %8.1f"
        timeFormat = "%d "
    print rowFormat % (testName, hostname, avg, std) ,
    for time in times:
        print timeFormat % time, 
    print

if __name__ == "__main__":
    ''' 
    Take care to avoid undesired shell wildcard expansion when passing a glob
    pattern in as a command line argument.
    '''
    usage = """ %prog [options] """
    parser = OptionParser( usage=usage )
    parser.add_option( '-e', '--header', action="store_false", default=True,
        help="do not write table header" )
    parser.add_option( '--headeronly', action="store_true", default=False,
        help="write only the table header" )
    parser.add_option( '-c', '--csv', action="store_true", default=False,
        help="wite table in comma separated ariable format" )
    (options, args) = parser.parse_args()
    if options.headeronly:
        print_header( options.csv )
    else:
        if len(args) > 1:
            parser.print_help()
            sys.exit(1)
        make_report( options, globPattern=args[0] )
