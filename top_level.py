import subprocess
import os
import sys

#this only does the job for unix machines that share the home directory
#swap around ~/.casa/prelude.py so we can set matplotlib to Agg
HOME = os.path.expanduser('~')
os.rename(HOME+'/.casa/prelude.py', HOME+'/.casa/prelude_backup.py')
pre = open(HOME+'/.casa/prelude.py', 'w')
pre.write('import matplotlib\n')
pre.write("matplotlib.use('Agg')\n")
pre.close()

#this works for benchmark and machine!
devnull = open(os.devnull, 'w')
oldStdout = sys.stdout
oldStderr = sys.stderr
sys.stdout = devnull
sys.stderr = devnull
command = 'export DA_BENCH=yes'
command += '; casa --nologger -c test_machine_curr_dir.py'
machineProc = subprocess.Popen(command, shell=True, stdout=devnull, \
                               stderr=devnull)
#machineProc = subprocess.Popen(['casa', '--nologger', \
#                                '-c test_machine_curr_dir.py'], shell=False, \
#                               stdout=devnull, stderr=devnull)
machineProc.wait()
sys.stdout = oldStdout
sys.stderr = oldStderr
devnull.close()

#again, only works on linux machines that share the home directory
#swap the prelude files back
os.remove(HOME+'/.casa/prelude.py')
os.rename(HOME+'/.casa/prelude_backup.py', HOME+'/.casa/prelude.py')
