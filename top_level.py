import subprocess
import os
import sys
import time

#add matplotlib backend setting to ~/.casa/prelude.py
#only works for linux machines on shared home directory filer
preludePath = os.path.expanduser('~')
preludePath += '/.casa/prelude.py'
if not os.path.isfile(preludePath):
    open(preludePath, 'w').close()
prelude = open(preludePath, 'r+')
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

#this works for benchmark and machine!
devnull = open(os.devnull, 'w')
oldStdout = sys.stdout
oldStderr = sys.stderr
sys.stdout = devnull
sys.stderr = devnull
cmdBeg = 'ssh -AX '
cmdEnd = " 'export DA_BENCH=yes; casa --nologger -c /lustre/naasc/nbrunett/" + \
         "bench_code_devel/CASA-Guides-Script-Extractor/" + \
         "remote_machine_worker.py'"
hosts = ['cvpost048', 'cvpost064']
procs = list()
for host in hosts:
    procs.append(subprocess.Popen(cmdBeg+host+cmdEnd, shell=True, \
                                  stdout=devnull, stderr=devnull))
    #not general at all!
    #for log files on shared home directory
    time.sleep(10)
    while os.path.exists('/users/nbrunett/casapy.log'):
        time.sleep(10)
for i in range(len(procs)):
    procs[i].wait()
sys.stdout = oldStdout
sys.stderr = oldStderr
devnull.close()
