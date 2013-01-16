#!/bin/env python

import sys, re, numpy, glob

def make_report( globPattern ):
    """
    Generate a report from casa_call.summarize_bench output.

    * globPattern = glob pattern for casa_call.summarize_bench output files to
      process
    """
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
        print_ascii( testName, hostname, times, avg, std )

def print_ascii( testName, hostname, times, avg, std ):
    """ Print 1 row of the summary ASCII table. """
    print "%33s %12s %8.1f %8.1f " % (testName, hostname, avg, std) ,
    for time in times:
        print "%d " % time, 
    print

def print_csv( testName, hostname, times, avg, std ):
    """ Print 1 row of the summary CSV table. """
    print "%33s, %12s, %8.1f, %8.1f " % (testName, hostname, avg, std) ,
    for time in times:
        print "%d, " % time, 
    print

if __name__ == "__main__":
    ''' 
    Take care to avoid undesired shell wildcard expansion when passing a glob pattern in as a 
    command line argument.
    '''
    make_report(sys.argv[1])
