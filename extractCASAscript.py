#!/usr/bin/env python
#
# python script to extract CASA-executable scripts from the CASA
# Guides webpages. This version has been edited to include some
# additional benchmarking functionality.
#
# --- Some specific notes on benchmarking mode ---
# 
# This mode will try to remove interactive components from the script
# and call a small python program to note the start time and stop time
# of each task in a text file. It requires a list of CASA tasks, which
# can be automatically generated using *list_all_tasks.py*.
#
# The intended functionality of the benchmarking mode is (1) to allow
# easy assessment of whether the scripts are working and (2) to
# produce useful benchmarks of performance, e.g., as a function of
# machine.
#
# For this mode to work, you need to have the "casa_call.py" package
# available in your python path. The script should be periodically
# updated to hold an up-to-date task list using "list_all_tasks.py"
# inside the relevant CASA version. Extra tasks in this list probably
# won't hurt.
#
# To invoke benchmarking add the command line parameter "benchmark"
# after the rest of the call.
# 
# -------------------------------------------------
#
# HISTORY
# Jack Gallimore 8/10/09
# Updated to accommodate new web host 10/30/09.
# Bug Fixes 12/17/09 -- jfg
# Bug fixes and added plotants to interactive command list 2/24/10 -- jfg
# Added the ability to make benchmarking, non-interactive scripts aug 11 --- akl
# Updated code to make clean non-interactive; added summary to end of benchmark test. 09/02/2011 -- jhc

# =====================
# IMPORTS
# =====================

import urllib
import urllib2
import sys
import codecs
import re
import string
import os, os.path
from optparse import OptionParser

# =====================
# DEFINITIONS
# =====================

# Expression that define the beginning and end of CASA code blocks in the HTML
beginBlock = "class=\"source-python\""
endBlock = "</pre></div></div>"

# interactives
interactive=re.compile("(plotxy|plotcal|plotms|viewer|plotants)")

# CASA task list (used for benchmarking markup, else ignored)
casa_tasks = ['accum',
            'applycal',
            'asap_init',
            'autoclea',
            'bandpass',
            'blcal',
            'boxi',
            'browsetable',
            'calstat',
            'clean',
            'clearcal',
            'clearplot',
            'clearstat',
            'concat',
            'conjugatevis',
            'csvclea',
            'cvel',
            'deconvolve',
            'exportasd',
            'exportfits',
            'exportuvfits',
            'feather',
            'find',
            'fixplanets',
            'fixvis',
            'flagautocorr',
            'flagcmd',
            'flagdata',
            'flagmanager',
            'fluxscale',
            'ft',
            'gaincal',
            'gencal',
            'hanningsmooth',
            'help par.parametername',
            'help taskname',
            'imcollapse',
            'imcontsub',
            'imfit',
            'imhead',
            'immath',
            'immoments',
            'importaipscaltable',
            'importasdm',
            'importevl',
            'importfits',
            'importfitsidi',
            'importgmr',
            'importoldasd',
            'importuvfits',
            'importvla',
            'imregrid',
            'imsmooth',
            'imstat',
            'imtrans',
            'imval',
            'imview',
            'listcal',
            'listhistory',
            'listobs',
            'listsd',
            'listvis',
            'mosai',
            'msmoments',
            'msview',
            'plotants',
            'plotcal',
            'plotms',
            'plotxy',
            'polcal',
            'rmtables',
            'sdaverage',
            'sdbaseline',
            'sdcal',
            'sdcoadd',
            'sdfit',
            'sdflag',
            'sdflagmanager',
            'sdimaging',
            'sdimprocess',
            'sdlist',
            'sdmath',
            'sdplot',
            'sdsave',
            'sdscale',
            'sdsmooth',
            'sdstat',
            'sdtpimaging',
            'setjy',
            'simdata',
            'slsearch',
            'smoothcal',
            'specfi',
            'splattotable',
            'split',
            'startup',
            'taskhelp',
            'tasklist',
            'testautofla',
            'testconcat',
            'toolhelp',
            'uvcontsub',
            'uvmodelfit',
            'uvsub',
            'viewer',
            'vishead',
            'visstat',
            'widefiel']

# define formatting junk that needs to be filtered
# JFG comments that regular expressions might clean this up
junkStr = ["<div dir=\"ltr\" style=\"text-align: left;\">"]
junkStr = junkStr + ["<div class=\"source-python\" style=\"font-family: monospace;\">"]
junkStr = junkStr + ["<pre>"]
junkStr = junkStr + ["</span>"]
junkStr = junkStr + ["</pre></div></div>"]
junkStr = junkStr + ["&nbsp;"]
paren1 = "&#40;"
paren2 = "&#41;"
brack2 = "&#93;"
brack1 = "&#91;"
sqirl1 = "&#123;"
sqirl2 = "&#125;"
quote1 = "&quot;"
lessthan = "&lt;"
greaterthan = "&gt;"
ampersand = "&amp;"
substr1 = r"<span class=[^>]*>"

# tasks to suppress in benchmarking run
tasks_to_suppress = ["plotms"]

# =====================
# FUNCTIONS
# =====================

def countParen(line):    
    """
    Returns the net open and closed parentheses.
    """
    pcount = 0
    for char in line:
        if char == '(': pcount += 1
        if char == ')': pcount -= 1
    return pcount

def isInput(line):
    """
    Tests if a line is waiting for user input.
    """
    temp = line.find("raw_input")
    return  temp > -1

def extract_task(line):
    """
    Tries to return the task name being called in the line.
    """
    stripped = line.lstrip()
    temp = stripped.find("(")
    if temp == -1:
        return None
    return stripped[0:temp]

def is_task_call(line):
    """
    Tests if the line is a task call.
    """
    if extract_task(line) in casa_tasks:
        return True
    return False

def indentation(line):
    spaces = 0
    active = True
    for char in line:
        if active == False:
            continue
        if char == " ":
            spaces += 1
        else:
            active=False
    return spaces

def add_benchmarking(line,tasknum=0):
    this_task = extract_task(line)
    indents = indentation(line)
    pre_string = ""
    for i in range(indents):
        pre_string+=" "
    before = pre_string+"this_call = casa_call.Call('"+this_task+"','"+str(tasknum)+"')\n"
    after = "\n"+pre_string+"this_call.end(out_file)"
    return before+line+after

def suppress_for_benchmark(line):
    if is_task_call(line) == False:
        return False
    if extract_task(line) in tasks_to_suppress:
        return True
    return False

def make_clean_noninteractive(line):
    """
    Make calls to clean non interactive.

    Clean can be called as a function with parameters specified as function arguments
    or as a function with no parameters in which case the parameters are obtained from 
    the local namespace. Both invocations of clean are made non interactive.
    """
    # First check to see if clean is called with function arguments.
    if is_task_call(line) and extract_task(line) == "clean":
        # Make clean non-interactive
        pattern = r'''interactive\ *=\ *(True|T|true)'''
        new_line = re.sub( pattern, 'interactive = False', line )
        # Remove mask parameter if it exists
        pattern = r'''mask\ *=\ *['"].*['"].*,?'''
        new_line = re.sub( pattern, '', new_line )
        return new_line
    # Second account for parameters being pulled from local namespace
    else:
        pattern = r'''^[ \t]*interactive\ *=\ *(True|T|true)'''
        # If variable interactive is being set, make sure it is set to false.
        if re.match( pattern, line ):
            pattern2 = r'''\ *(True|T|true)'''
            new_line = re.sub( pattern2, ' False', line )
            return new_line
    return line

def suppress_gui( line ):
    """
    Suppress GUIs. Return modified line.

    * line = a python statement
    """
    if is_task_call(line): 
        # Plotcal
        if extract_task(line) == "plotcal":
            # if showgui is specified, make sure it is false
            pattern = r'''showgui\ *=\ *(True|T|true|False|F|false)'''
            new_line = re.sub( pattern, 'showgui = False', line )
            if new_line == line: # no substituion made
                # add showgui=False to parameter list
                pattern = r'''\('''
                new_line = re.sub( pattern, '( showgui=False, ', line )
            return new_line
        # Suppress GUIs for other tasks here...
    return line

# function to clean up html strings (convert html markup to executable python)
def loseTheJunk(line):
    """
    Strip garbage from line.
    """
    outline = line # this should be function'd -- need to replace tgets etc as in first version of script
    outline = re.sub(substr1, r'', outline)
    for junk in junkStr:
        outline = outline.replace(junk, "")
    outline = outline.replace(quote1, "\"")
    outline = outline.replace(paren1, "(")
    outline = outline.replace(paren2, ")")
    outline = outline.replace(brack1, "[")
    outline = outline.replace(brack2, "]")
    outline = outline.replace(sqirl1, "{")
    outline = outline.replace(sqirl2, "}")
    outline = outline.replace(lessthan, "<")
    outline = outline.replace(greaterthan, ">")
    outline = outline.replace(ampersand, "&")

    #some additional parsing -- scripting has slightly different
    #syntax than interactive session for tget, default, and go
    #(presumably among others). 

    newline = outline
    newline = newline.replace(r'tget ', r'tget(')
    newline = newline.replace(r'default ', r'default(')
    if newline == 'go':
        newline = 'go('
    if newline != outline: newline = newline + ')'
    outline = newline
    return outline

def addInteractivePause(outline):
    newoutline = outline
    newoutline += "\ninp()\nprint('When you are done with the graphics window,')\n"
    newoutline += "\nprint('quit that window, and')\n"
    newoutline += "\nuser_check=raw_input('press enter to continue script\\n')\n"
    return newoutline

# Return the pre-material needed to set up benchmarking
def benchmark_header( scriptName='script' ):
    """
    Write the header of the benchmarking script.

    * scriptName = Name of the benchmarking script
    """
    out_file = scriptName.replace('.py','.benchmark.txt')
    lines = []
    lines.append("### Begin Benchmarking Material")
    lines.append("import casa_call")
    lines.append("try:")
    lines.append("    out_file")
    lines.append("except NameError:")
    lines.append("    out_file = '" + out_file + "'")
    lines.append("if os.path.exists(out_file):")
    lines.append("    counter = 1")
    lines.append("    while os.path.exists(out_file+'.'+str(counter)):")
    lines.append("        counter += 1")
    lines.append("    os.system('mv '+out_file+' '+out_file+'.'+str(counter))")
    lines.append("os.system('rm -rf '+out_file)")
    lines.append("### End Benchmarking Material")
    return lines

def pythonize_shell_commands( line ):
    """
    Make casapy-friendly shell commands Python compatible.

    Unix shell commands included below in the 'commands' list can be called
    directly from the casapy prompt. These commands cannot be called from inside
    a Python script. To run these commands in a script, place them in an 
    os.system call.
    
    * line = a python statement
    """
    commands = [ 'ls', 'pwd', 'less', 'pwd', 'cd', 'cat' ]
    firstWord = line.split(' ')[0]
    if firstWord in commands:
        line = 'os.system("' + line + '")'
    return line

def make_system_call_noninteractive( line ):
    """
    Make calls to os.system non-interactive. Return non-interacive line.

    Some shell commands called via os.system require user interaction, such as
    more.  Make these shell calls noninteractive.

    Replacements:

    1) Replace more with cat,
    2) [Add other replacements here...]

    * line = a python statement
    """
    command = ''
    newCommand = ''
    # Extract the system command from the os.system statement
    pattern = r'''os.system\ *\(\ *(['"])(.*)\1\ *\)'''
    matchObj = re.match( pattern, line )
    if matchObj:
        command = matchObj.group(2)
        command = command.strip()
        # Replace more with cat
        pattern2 = r'''^more\ '''
        newCommand = re.sub( pattern2, 'cat ', command )
        # Add additional substutions here...
    newLine = line.replace( command, newCommand, 1 )
    return newLine

def exclude_raw_input( line ):
    """
    Exclude raw_input calls from non-interactive scripts.

    * line = a python statement
    """
    pattern = r'''raw_input\ *\('''
    if re.search( pattern, line ):
        line = ' ' * indentation(line) + '#' + line.replace('\n','')
    return line
    
# start of main code

# =====================
# MAIN PROGRAM
# =====================

def main( URL, options ):
    """ Create a Python script from a CASA Guide or existing Python script.
    
    * URL = URL to a CASA Guide web page (HTML) or a Python script.  
    * options = options object created by optparse.  If options.benchmark
      is true, output a Python benchmarking script.

    If URL to a CASA Guide, extract the Python from the guide and create
    an executable Python script. If options.benchmark is true, produce a 
    benchmark test from the CASA Guide or existing Python script. 

    If URL to a Python script, convert the script to a benchmarking script.
    """

    print "Rest assured. I'm trying to get " + URL + " for you now."

    # See if the user asked for benchmarking mode 
    if options.benchmark:
        print "I will try to write the script in benchmarking mode."

    # Determine if the input file is a Python script
    pyInput = False
    if ( URL[-3:].upper() == '.PY' ):
        pyInput = True

    # Pull the input file across the web or get it from local network
    responseLines = []
    outFile = ''
    if ( URL[:4].upper() == 'HTTP' ):
        req = urllib2.Request(URL)
        response = urllib2.urlopen(req)
        responseLines = response.read().split("\n")
        # Clean up the output file name
        outFile = URL.split('/')[-1]
        if not pyInput: outFile += '.py'
        outFile = outFile.replace("index.php?title=","")
        outFile = outFile.replace(":","")
        outFile = outFile.replace("_","") 
    else:
        print "Copying " + URL + " to CWD."
        os.system('scp elwood:'+URL+' ./')
        outFile = os.path.basename(URL)
        localFile = open( outFile , 'r' )
        responseLines = localFile.read().split("\n")

    print "Things are going well. Let me clean out some of that html markup."

    # Initialize the parser and output line list
    isActive = False
    lineList = []

    if pyInput:
        lineList = responseLines
    else:
        # Loop over the lines read from the web page
        for line in responseLines:
            # If we are not currently reading code, see if this line
            # begins a python code block.
            if (isActive == False):
                temp = line.find(beginBlock)
                if temp > -1:
                    isActive = True
                    outline = loseTheJunk(line)
                    lineList += [outline]
                    temp = line.find(endBlock)
                    if temp > -1:
                        isActive = False
                    line = "DontPrintMe" # avoid double printing if endBlock is on the same line
            if (isActive == True):
                if (line != "DontPrintMe"):
                    outline = loseTheJunk(line)
                    lineList += [outline]
                temp = line.find(endBlock)
                if temp > -1:
                    isActive = False

    # The commands are now loaded into a list of lines.

    # Now compress the lines into individual commands, allowing for
    # commands to span multiple lines. Lines are grouped by closed
    # parentheses.
    compressedList = []
    iline = 0
    while iline < len(lineList):
        line = lineList[iline]
        pcount = countParen(line)
        while(pcount > 0):
            line += '\n'
            iline += 1
            line += lineList[iline]
            pcount = countParen(line)
        line = string.expandtabs(line)
        compressedList += [line]
        iline += 1

    print str(len(lineList))+" total lines become"
    print str(len(compressedList))+" compressed lines"

    for i,line in enumerate(compressedList):
        compressedList[i] = pythonize_shell_commands( compressedList[i] )

    # Now write to disk. Details depend on desired mode.
    if options.benchmark or pyInput:
        task_list = []
        task_nums = []
        print "Writing file for execution in benchmarking mode."
        tasknum = 0
        f = codecs.open(outFile, 'w','utf-8')
        header = benchmark_header( scriptName = outFile )
        for line in header:
            print >>f, line
        for line in compressedList:
            if suppress_for_benchmark(line):
                print >>f, ' ' * indentation(line) + 'pass #' + \
                    line.replace('\n','')
                continue
            line = make_clean_noninteractive(line)
            line = make_system_call_noninteractive(line)
            line = suppress_gui(line)
            line = exclude_raw_input(line)
            if is_task_call(line):                
                this_task = extract_task(line)
                print "I found a task call for ", this_task                
                tasknum += 1
                line = add_benchmarking(line,tasknum)      
                task_list.append(this_task)
                task_nums.append(tasknum)
            print >>f, line
        print >>f, 'casa_call.summarize_bench( out_file, out_file+".summary" )'
        f.close()        
        # write the expectation to a file
        exp_file = outFile+'.expected'
        print "I am writing the expected flow to a file called "+exp_file
        f = codecs.open(exp_file, 'w','utf-8')
        for i in range(len(task_list)):
            print >>f, task_list[i], task_nums[i]
        f.close()
    else:
        print "Writing file for execution in interactive mode."
        f = codecs.open(outFile, 'w','utf-8')
        for line in compressedList:
            mtch = interactive.match(line)
            if (mtch and line.find("showgui=F") == -1): line = addInteractivePause(line)
            print >>f, line
        f.close()
    
    print "Great. I think I just wrote the file " + outFile + " in the current directory. No promises.\n"
    print "In casapy, run the file using\n"
    print "execfile(\"" + outFile + "\")\n"


    
if __name__ == "__main__":
    usage = \
"""usage: %prog [options] URL

The URL should point to a CASA Guide webpage (HTML) or to a Python script.
"""
    parser = OptionParser( usage=usage )
    parser.add_option( '-b', '--benchmark', action="store_true", default=False,
        help="produce benchmark test script" )
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        raise ValueError("")
    main(args[0], options)

# Wish list:
# * Use proper command line option API for benchmark option.
# * Make script so it handles a python script directly.
# * Clean up code by putting stuff from main into functions.
