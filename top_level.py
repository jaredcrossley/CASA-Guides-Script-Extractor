#standard library imports
import os
import platform
import shutil
import subprocess
import sys
import time

#library specific imports
import itinerary
import parameters


"""NRAO convenience script for parallel CASA benchmarking.

Purpose
-------
This Python script is intended to simplify the process of running CASA
benchmarking for internal NRAO staff. It makes it possible to clone the
CASA-Guides-Script-Extractor repository, edit a single file to specify what will
be benchmarked and to invoke Python on a single script to handle everything
else. The goal has been to automate as much of the benchmarking and report
generation process and this file is the interface between the user and the
benchmarking code.

Usage
-----
Using this script for benchmarking on NRAO machines on the internal network
is only a two step process. First, you must edit the itinerary.py file included
in this repository to specify which machines will be used, what data sets will
be run, which stages each data set will run through and how many times each
benchmark will be repeated. Directions for editing itinerary.py are included in
that file. The second step is to invoke Python with this file as the only
argument. E.g.

> python /lustre/naasc/nbrunett/CASA-Guides-Script-Extractor/top_level.py

What This Script Does
---------------------
This portion of the benchmarking process was written as a "procedural" Python
script because, at the time of writing, it was the most straightforward way to
provide a simple interface for the user. The tasks perfomed by this script are:

  -collect the hosts, data sets, number of iterations and steps to benchmark
   from itinerary.py
  -modify prelude.py on remote machines, if necessary, to add matplotlib Agg
  -clone repo on remote machines
  -build script to run machine benchmarking on the remote machines
  -copy that script to each remote host to be benchmarking
  -start up, over ssh, CASA on each machine to execute the remote machine
   script
  -remove remote repo copy
  -remove remote machine script copy
  -remove remote casapy and ipython log files
  *[not yet] move results to local machine
  *[not yet] compile results into a single report on local machine

As mentioned above, the results from each machine are not yet moved to the
local machine that is running this script. The results are also still left as
text files from each individual benchmark. It is up to the user, at the time of
this writing, to retrieve all of the results from each remote machine and to
combine them as the user sees fit. The completed workflow will have this script
automating those tasks as well.
"""


def setupDevNull(switch, setupOutput=None):
    """Sets or unsets sys.stdout and sys.stderr to os.devnull.

    Returns
    -------
    If switch == 'on'
       Returns 3-tuple containing original sys.stdout file object, original
       sys.stderr file object and the os.devnull file object.
    If switch == 'off'
       Returns None.

    Parameters
    ----------
    switch : str
       Specifies if stdout and stderr are being set to devnull or returned to
       their default values. Must be either "on" or "off".

    setupOutput : 3-tuple
       Only used when switch == 'off' and it should be the returned 3-tuple from
       when setupDevNull was run with switch == 'on'.

    Notes
    -----
    Intended as a simple convenience function to clean up the main part of this
    script. When a portion of the script should not be sending any output to the
    terminal, and we do not care about logging it, then this function should
    wrap around that section. E.g.

       stdShuffle = setupDevNull(switch='on')
       print 'Python is dumb.'
       setupDevNull(switch='off', setupOutput=stdShuffle)

    Since the above print statement is something we would obviously never want
    to have printed to the terminal and we do not want to keep track of it we
    just wrap it with a couple calls to setupDevNull to keep it quiet.
    """
    if switch == 'on':
        devnull = open(os.devnull, 'w')
        oldStdout = sys.stdout
        oldStderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        return (oldStdout, oldStderr, devnull)
    elif switch == 'off':
        sys.stdout = setupOutput[0]
        sys.stderr = setupOutput[1]
        setupOutput[2].close()
    else:
        raise ValueError('switch must be "on" or "off".')


itinerary = itinerary.itinerary
#make sure itinerary is properly formed
if itinerary.keys() != ['hosts']:
    raise ValueError('itinerary dictionary is malformed. Please check ' + \
                     'template in itinerary.py header against your dictionary.')
if len(itinerary['hosts'].keys()) == 0:
    raise ValueError('itinerary dictionary must contain at least one host.')
acceptedHosts = ['cvpost' + '%03d' % i for i in range(1, 65)]
acceptedHosts.append('gauss')
acceptedHosts.append('technomage')
acceptedHosts.append('starthinker')
for host in itinerary['hosts'].keys():
    if host not in acceptedHosts:
        raise ValueError('"'+host+'" not in list of accepted machines.')
    if len(itinerary['hosts'][host].keys()) != 6:
        raise ValueError(host+' dictionary must have six key, value pairs.')
    if 'dataSets' not in itinerary['hosts'][host].keys():
        raise ValueError(host+' dictionary is missing dataSets entry.')
    if 'nIters' not in itinerary['hosts'][host].keys():
        raise ValueError(host+' dictionary is missing nIters entry.')
    if 'steps' not in itinerary['hosts'][host].keys():
        raise ValueError(host+' dictionary is missing steps entry.')
    if 'scriptsSources' not in itinerary['hosts'][host].keys():
        raise ValueError(host+' dictionary is missing scriptsSources entry.')
    if 'workDir' not in itinerary['hosts'][host].keys():
        raise ValueError(host+' dictionary is missing workDir entry.')
    if len(itinerary['hosts'][host]['dataSets']) == 0:
        raise ValueError(host+' must have at least one dataSet.')
    for dataSet in itinerary['hosts'][host]['dataSets']:
        if type(dataSet) != str:
            raise TypeError(host+' dataSets must be specified with strings.')
        try:
            test = getattr(parameters, dataSet)
        except AttributeError:
            raise ValueError(host+' data set "'+dataSet+'" not in list of ' + \
                             'accepted data sets.')
    if len(itinerary['hosts'][host]['nIters']) != \
       len(itinerary['hosts'][host]['dataSets']):
        raise ValueError('nIters from '+dataSet+' for '+host+' must be the ' + \
                         'same length as the dataSets list.')
    for iters in itinerary['hosts'][host]['nIters']:
        if type(iters) != int:
            raise TypeError(host+' nIters must be a list of only integers.')
        if iters < 1:
            raise ValueError('All '+host+' nIters values must be greater ' + \
                             'than zero.')
    if len(itinerary['hosts'][host]['skipDownloads']) != \
       len(itinerary['hosts'][host]['dataSets']):
        raise ValueError('skipDownloads from '+dataSet+' for '+host+' must ' + \
                         'be the same length as the dataSets list.')
    for skip in itinerary['hosts'][host]['skipDownloads']:
        if type(skip) != bool:
            raise TypeError(host+' skipDownloads must be a list of only ' + \
                            'booleans.')
    if len(itinerary['hosts'][host]['steps']) != \
       len(itinerary['hosts'][host]['dataSets']):
        raise ValueError('steps from '+dataSet+' for '+host+' must be the ' + \
                         'same length as the dataSets list.')
    for step in itinerary['hosts'][host]['steps']:
        if type(step) != str:
            raise TypeError(host+' steps must be a list of only strings.')
        if step != 'both' and step != 'cal' and step != 'im':
            raise ValueError(host+' steps elements must be "both", "cal" ' + \
                             'or "im".')
    if len(itinerary['hosts'][host]['scriptsSources']) != \
       len(itinerary['hosts'][host]['dataSets']):
        raise ValueError('scriptsSources from '+dataSet+' for '+host+ \
                         ' must be the same length as the dataSets list.')
    for source in itinerary['hosts'][host]['scriptsSources']:
        if type(source) != str:
            raise TypeError(host+' scriptsSources must be a list of only ' + \
                            'strings.')
        if source != 'disk' and source != 'web':
            raise ValueError(host+' scriptsSources elements must be "disk" ' + \
                             'or "web".')
    if type(itinerary['hosts'][host]['workDir']) != str:
        raise TypeError('workDir from '+dataSet+' for '+host+' must be ' + \
                        'a string.')
    if len(itinerary['hosts'][host]['workDir']) == 0:
        raise ValueError('workDir from '+dataSet+' for '+host+' cannot ' + \
                        'be an empty string.')
    stdShuffle = setupDevNull(switch='on')
    proc = subprocess.Popen(['ssh', '-AX', host, 'if', '[', '-d', \
                             itinerary['hosts'][host]['workDir'], '];', \
                             'then', 'echo', '1;', 'else', 'echo', '0;', \
                             'fi'], shell=False, stdout=subprocess.PIPE, \
                            stderr=subprocess.PIPE)
    workDirExists = bool(int(proc.communicate()[0].rstrip()))
    setupDevNull(switch='off', setupOutput=stdShuffle)
    if not workDirExists:
        raise ValueError('workDir on '+host+' does not exist.')
    if itinerary['hosts'][host]['workDir'][-1] != '/':
        itinerary['hosts'][host]['workDir'] += '/'
    #make sure itinerary works with the info in parameters.py
    for i,dataSet in enumerate(itinerary['hosts'][host]['dataSets']):
        params = getattr(parameters, dataSet)
        if itinerary['hosts'][host]['skipDownloads'][i] == True:
            if itinerary['hosts'][host]['steps'][i] == 'cal' or \
               itinerary['hosts'][host]['steps'][i] == 'both':
                if params['lustre']['uncalData'] == None or \
                   params['elric']['uncalData'] == None:
                    raise ValueError('The '+dataSet+' uncalibrated data is ' + \
                                     'not available on lustre and/or elric ' + \
                                     'for '+host+'. Revise itinerary or ' + \
                                     'update parameters.py.')
            if itinerary['hosts'][host]['steps'][i] == 'im':
                if params['lustre']['calData'] == None or \
                   params['elric']['calData'] == None:
                    raise ValueError('The '+dataSet+' calibrated data is ' + \
                                     'not available on lustre and/or ' + \
                                     'elric for '+host+'. Revise itinerary ' + \
                                     'or update parameters.py')
        else:
            if itinerary['hosts'][host]['steps'][i] == 'cal' or \
               itinerary['hosts'][host]['steps'][i] == 'both':
                if params['online']['uncalData'] == None:
                    raise ValueError('The '+dataSet+' uncalibrated data is' + \
                                     'not available online for'+host+'. ' + \
                                     'Revise itinerary or update ' + \
                                     'parameters.py.')
            if itinerary['hosts'][host]['steps'][i] == 'im':
                if params['online']['calData'] == None:
                    raise ValueError('The '+dataSet+' calibrated data is ' + \
                                     'not available online for '+host+'. ' + \
                                     'Revise itinerary or update ' + \
                                     'parameters.py.')
        if itinerary['hosts'][host]['steps'][i] == 'cal' or \
           itinerary['hosts'][host]['steps'][i] == 'both':
            if itinerary['hosts'][host]['scriptsSources'][i] == 'web':
                if params['online']['calScript'] == None:
                    raise ValueError('The '+dataSet+' calibration script ' + \
                                     'is not available online for '+host+ \
                                     '. Revise itinerary or update ' + \
                                     'parameters.py.')
            if itinerary['hosts'][host]['scriptsSources'][i] == 'disk':
                if params['lustre']['calScript'] == None or \
                   params['elric']['calScript'] == None:
                    raise ValueError('The '+dataSet+' calibration script ' + \
                                     'is not available on lustre and/or ' + \
                                     'elric for '+host+'. Revise itinerary ' + \
                                     'or update parameters.py.')
        if itinerary['hosts'][host]['steps'][i] == 'im':
            if itinerary['hosts'][host]['scriptsSources'][i] == 'web':
                if params['online']['imScript'] == None:
                    raise ValueError('The '+dataSet+' imaging script is ' + \
                                     'not available online for '+host+'. ' + \
                                     'Revise itinerary or update ' + \
                                     'parameters.py.')
            if itinerary['hosts'][host]['scriptsSources'][i] == 'disk':
                if params['lustre']['imScript'] == None or \
                   params['elric']['imScript'] == None:
                    raise ValueError('The '+dataSet+' imaging script is ' + \
                                     'not available on lustre and/or ' + \
                                     'elric for '+host+'. Revise itinerary ' + \
                                     'or update parameters.py.')
print 'Itinerary from itinerary.py successfully cleared checks.'
print '##Benchmarking to be run is:'
for host in itinerary['hosts'].keys():
    print '  ' + host
    for i,dataSet in enumerate(itinerary['hosts'][host]['dataSets']):
        print '    ' + dataSet
        print '      ' + str(itinerary['hosts'][host]['nIters'][i]) + \
              ' iterations'
        if itinerary['hosts'][host]['steps'][i] == 'both':
            print '      both calibration and imaging steps'
        elif itinerary['hosts'][host]['steps'][i] == 'cal':
            print '      calibration step'
        else:
            print '      imaging step'
print '##'


#add matplotlib backend setting to ~/.casa/prelude.py
for host in itinerary['hosts'].keys():
    #copy prelude.py file here
    stdShuffle = setupDevNull(switch='on')
    ret = subprocess.call(['scp', '-o', 'ForwardAgent=yes',
                           host+':~/.casa/prelude.py', \
                           'working_prelude.py'], \
                          shell=False, stdout=stdShuffle[2], \
                          stderr=stdShuffle[2])
    setupDevNull(switch='off', setupOutput=stdShuffle)
    if ret != 0:
        open('working_prelude.py', 'w').close()

    #add Agg conditional if necessary
    prelude = open('working_prelude.py', 'r+')
    lines = prelude.readlines()
    impOS = False
    impML = False
    bCond = False
    for line in lines:
        if line == 'import os\n':
            impOS = True
        if line == 'import matplotlib\n':
            impML = True
        if 'DA_BENCH' in line:
            bCond = True
    if not impOS:
        lines.insert(0, 'import os\n')
    if not impML:
        lines.insert(0, 'import matplotlib\n')
    if not bCond:
        lines.append("if os.environ.has_key('DA_BENCH'):\n")
        lines.append("    matplotlib.use('Agg')")
    prelude.seek(0, 0)
    prelude.writelines(lines)
    prelude.close()

    #replace original prelude.py file with our checked copy
    stdShuffle = setupDevNull(switch='on')
    subprocess.call(['scp', '-o', 'ForwardAgent=yes', \
                     'working_prelude.py', host+':~/.casa/prelude.py'], \
                    shell=False, stdout=stdShuffle[2], stderr=stdShuffle[2])
    setupDevNull(switch='off', setupOutput=stdShuffle)
    os.remove('working_prelude.py')


#clone repo onto remote machines
#needs to be changed when/if python_translate branch is merged into master
#(-b python_translate part would be removed if so)
for host in itinerary['hosts'].keys():
    #first check if it's already in the workDir
    stdShuffle = setupDevNull(switch='on')
    proc = subprocess.Popen(['ssh', '-AX', host, 'if', '[', '-d', \
                             itinerary['hosts'][host]['workDir']+ \
                             '/CASA-Guides-Script-Extractor', '];', \
                             'then', 'echo', '1;', 'else', 'echo', '0;', \
                             'fi'], shell=False, stdout=subprocess.PIPE, \
                            stderr=subprocess.PIPE)
    repoExists = bool(int(proc.communicate()[0].rstrip()))
    if not repoExists:
        #do the clone since it doesn't exist yet
        subprocess.call(['ssh', '-AX', host, 'cd', \
                         itinerary['hosts'][host]['workDir']+';', 'git', \
                         'clone', '-b', 'python_translate', \
                         'https://github.com/' + \
                         'jaredcrossley/CASA-Guides-Script-Extractor.git'], \
                        shell=False, stdout=stdShuffle[2], stderr=stdShuffle[2])
    setupDevNull(switch='off', setupOutput=stdShuffle)


#build machine script to be executed on remote machines and scp it over
remScripts = list()
for host in itinerary['hosts'].keys():
    remScripts.append(host + '_remote_machine.py')
    macF = open(remScripts[-1], 'w')
    macF.write('import os\n')
    macF.write('\n')
    macF.write('CASAglobals = globals()\n')
    macF.write("scriptDir = '" + itinerary['hosts'][host]['workDir'] + \
               "CASA-Guides-Script-Extractor'\n")
    macF.write("dataSets = " + str(itinerary['hosts'][host]['dataSets']) + "\n")
    macF.write("nIters = " + str(itinerary['hosts'][host]['nIters']) + "\n")
    macF.write("skipDownloads = " + \
               str(itinerary['hosts'][host]['skipDownloads']) + "\n")
    macF.write("steps = " + str(itinerary['hosts'][host]['steps']) + "\n")
    macF.write("scriptsSources = " + \
               str(itinerary['hosts'][host]['scriptsSources']) + "\n")
    macF.write("workDir = '" + itinerary['hosts'][host]['workDir'] + "'\n")
    macF.write('quiet = True\n')
    macF.write('#add script directory to Python path if need be\n')
    macF.write("scriptDir = os.path.abspath(scriptDir) + '/'\n")
    macF.write('if scriptDir not in sys.path:\n')
    macF.write('    sys.path.append(scriptDir)\n')
    macF.write('\n')
    macF.write('import machine\n')
    macF.write('\n')
    macF.write('bMarker = machine.machine(CASAglobals=CASAglobals, \\\n')
    macF.write('                         scriptDir=scriptDir, \\\n')
    macF.write('                         dataSets=dataSets, \\\n')
    macF.write('                         nIters=nIters, \\\n')
    macF.write('                         skipDownloads=skipDownloads, \\\n')
    macF.write('                         steps=steps, \\\n')
    macF.write('                         workDir=workDir, \\\n')
    macF.write('                         scriptsSources=scriptsSources, \\\n')
    macF.write('                         quiet=quiet)\n')
    macF.write('bMarker.runBenchmarks(cleanUp=True)\n')
    macF.close()
    stdShuffle = setupDevNull(switch='on')
    subprocess.call(['scp', '-o', 'ForwardAgent=yes', remScripts[-1], \
                     host+':'+itinerary['hosts'][host]['workDir']], \
                    shell=False, stdout=stdShuffle[2], stderr=stdShuffle[2])
    setupDevNull(switch='off', setupOutput=stdShuffle)
    os.remove(remScripts[-1])


#kick off benchmarking on each host
print 'Launching benchmarking jobs on each machine.'
stdShuffle = setupDevNull(switch='on')
cmdP1 = 'ssh -AX '
cmdP2 = " 'export DA_BENCH=yes; cd "
cmdP3 = '; casa --nologger -c '
procs = list()
for i,host in enumerate(itinerary['hosts'].keys()):
    cmdTot = cmdP1 + host + cmdP2 + itinerary['hosts'][host]['workDir'] + \
             cmdP3 + itinerary['hosts'][host]['workDir'] + remScripts[i] + "'"
    procs.append(subprocess.Popen(cmdTot, shell=True, \
                                  stdout=stdShuffle[2], stderr=stdShuffle[2]))
    #in case same workDir used for multiple machines
    time.sleep(10)
    while os.path.exists(itinerary['hosts'][host]['workDir'] + '/casapy.log'):
        time.sleep(10)
for i in range(len(procs)):
    procs[i].wait()
setupDevNull(switch='off', setupOutput=stdShuffle)
print 'All benchmarking jobs are finished.'
print 'Finishing file cleanup.'


#remove remote repo and machine script
for i,host in enumerate(itinerary['hosts'].keys()):
    stdShuffle = setupDevNull(switch='on')
    subprocess.call(['ssh', '-AX', host, 'rm', '-rf', \
                     itinerary['hosts'][host]['workDir']+ \
                     '/CASA-Guides-Script-Extractor', \
                     itinerary['hosts'][host]['workDir']+remScripts[i]], \
                    shell=False, stdout=stdShuffle[2], stderr=stdShuffle[2])
    setupDevNull(switch='off', setupOutput=stdShuffle)


#remove remote casapy and ipython log files
for host in itinerary['hosts'].keys():
    stdShuffle = setupDevNull(switch='on')
    subprocess.call(['ssh', '-AX', host, 'rm', '-rf', \
                     itinerary['hosts'][host]['workDir']+'casapy*.log', \
                     itinerary['hosts'][host]['workDir']+'ipython*.log'], \
                    shell=False, stdout=stdShuffle[2], stderr=stdShuffle[2])
    setupDevNull(switch='off', setupOutput=stdShuffle)
