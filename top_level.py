import os
import platform
import shutil
import subprocess
import sys
import time

###what this script does/will do###
#-collects the hosts, data sets, number of iterations and steps to benchmark
#  [ ]written
#  [ ]tested
#  [ ]i'm happy
#-modifies prelude.py on remote machines if necessary to add matplotlib Agg
# setting
#  [x]written
#  [ ]tested
#  [ ]i'm happy
#-copies repo files to remote machines
#  [ ]written
#  [ ]tested
#  [ ]i'm happy
#-builds script to run machine benchmarking on the remote machines
#  [x]written
#  [ ]tested
#  [ ]i'm happy
#-copies that file to each remote host to be benchmarking
#  [ ]written
#  [ ]tested
#  [ ]i'm happy
#-starts up, over ssh, CASA on each machine to execute the remote machine script
#  [x]written
#  [x]tested
#  [x]i'm happy
#-removes remote repo copy
#  [ ]written
#  [ ]tested
#  [ ]i'm happy
#-removes remote machine script copy
#  [ ]written
#  [ ]tested
#  [ ]i'm happy
#-removes remote casapy and ipython log files
#  [ ]written
#  [ ]tested
#  [ ]i'm happy
#-?moves results to local machine
#-?compiles results into a single report on local machine
#-?should a lot of the checks that are done in the classes be done here too (for
#  example: setting skipDownloads=True for a data set that isn't stored on
#  lustre) :/ this would be because error messages would be maybe directed to
#  some random log file and wouldn't be presented plainly

#think about how to reduce chance of shell-injection in the subprocess calls
#that start the benchmarking; maybe have a set of hosts that are acceptable and
#thus can't be anything malicious

def setupDevNull(switch, setupOutput=None):
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


#add matplotlib backend setting to ~/.casa/prelude.py
#this needs to be thoroughly tested
hosts = ['cvpost048', 'cvpost064']
filerDone = False
for host in hosts:
    #determine if remote host is linux or Mac
    stdShuffle = setupDevNull(switch='on')
    proc = subprocess.Popen(['ssh', '-AX', host, 'uname', '-s'], shell=False, \
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    kernel = proc.communicate()[0].rstrip()
    setupDevNull(switch='off', setupOutput=stdShuffle)

    #linux machines (assumed to be on the filer) only need to be checked once
    if 'Darwin' not in kernel and filerDone:
        continue

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
    prelude = open('working_prelude', 'r+')
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
    #only need to do it once for machines on the filer
    if 'Darwin' not in kernel:
        filerDone = True


#build machine script to be executed on remote machines
#needs to be generalized when aqcuiring benchmarking itinerary is handled here
#the code being written needs to be carefully inspected so I'm happy with it
macF = open('remote_machine.py', 'w')
macF.write('import os\n')
macF.write('\n')
macF.write('CASAglobals = globals()\n')
macF.write("scriptDir = '/lustre/naasc/nbrunett/bench_code_devel/' + \\n")
macF.write("            'CASA-Guides-Script-Extractor'\n")
macF.write("dataSets = ['x2012_1_00912_S_43', 'NGC3256Band3_43']\n")
macF.write('nIters = [2, 2]\n')
macF.write('skipDownloads = [True, False]\n')
macF.write("steps = ['both', 'im']\n")
macF.write("scriptsSources = ['disk', 'web']\n")
macF.write("workDir = '/lustre/naasc/nbrunett/bench_code_devel/testing/' + \\n")
macF.write("          'test_remote_subprocess'\n")
macF.write('quiet = True\n')
macF.write('#add script directory to Python path if need be\n')
#is this needed...?
macF.write("scriptDir = os.path.abspath(scriptDir) + '/'\n")
macF.write('if scriptDir not in sys.path:\n')
macF.write('    sys.path.append(scriptDir)\n')
macF.write('\n')
macF.write('import machine\n')
macF.write('\n')
macF.write('cvpost = machine.machine(CASAglobals=CASAglobals, \\n')
macF.write('                         scriptDir=scriptDir, \\n')
macF.write('                         dataSets=dataSets, \\n')
macF.write('                         nIters=nIters, \\n')
macF.write('                         skipDownloads=skipDownloads, \n')
macF.write('                         steps=steps, \\n')
macF.write('                         workDir=workDir, \\n')
macF.write('                         scriptsSources=scriptsSources, \\n')
macF.write('                         quiet=quiet)\n')
macF.write('cvpost.runBenchmarks(cleanUp=True)\n')
macF.close()


#kick off benchmarking on each host
stdShuffle = setupDevNull(switch='on')
sys.stderr = devnull
cmdBeg = 'ssh -AX '
cmdEnd = " 'export DA_BENCH=yes; casa --nologger -c /lustre/naasc/nbrunett/" + \
         "bench_code_devel/CASA-Guides-Script-Extractor/" + \
         "remote_machine_worker.py'"
procs = list()
for host in hosts:
    procs.append(subprocess.Popen(cmdBeg+host+cmdEnd, shell=True, \
                                  stdout=stdShuffle[2], stderr=stdShuffle[2]))
    #not general at all!
    #for log files on shared home directory
    time.sleep(10)
    while os.path.exists('/users/nbrunett/casapy.log'):
        time.sleep(10)
for i in range(len(procs)):
    procs[i].wait()
setupDevNull(switch='off', setupOutput=stdShuffle)
