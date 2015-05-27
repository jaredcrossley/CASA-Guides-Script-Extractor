import subprocess
import os
import sys

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
command = 'ssh -AX cvpost048'
command += " 'export DA_BENCH=yes"
command += "; casa --nologger -c /lustre/naasc/nbrunett/bench_code_devel/" + \
           "CASA-Guides-Script-Extractor/remote_machine_worker.py'"
#print command
#machineProc = subprocess.Popen(command, shell=True)
machineProc = subprocess.Popen(command, shell=True, stdout=devnull, \
                               stderr=devnull)
machineProc.wait()
sys.stdout = oldStdout
sys.stderr = oldStderr
devnull.close()
