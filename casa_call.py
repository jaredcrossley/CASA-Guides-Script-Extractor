import time, os
from readcol import readcol
import numpy as np

class Call:
    """
    Class to log times for one task call.
    """

    def __init__(self, 
                 task="", 
                 tag="",
                 begin=True):
        self._task = task
        self._tag = tag
        self._status = "UNSTARTED"
        if begin == True:
            self.begin()

    def begin(self, user_time=None):
        if user_time == None:
            self._start = time.time()
        else:
            self._start=user_time
        self._status = "RUNNING"
        
    def end(self, out_file=None, user_time=None):
        if user_time == None:
            self._stop = time.time()
        else: 
            self._stop = user_time
        self._delta = self._stop - self._start
        self._status = "DONE"
        if out_file != None:
            self.to_file(fname=out_file)

    def to_string(self):
        if self._status != "DONE":
            return "Not finished."
        line = ""
        line += self._task+" "
        line += self._tag+" "
        line += str(self._delta)+" "
        line += str(self._start)+" "
        line += str(self._stop)+"\n"
        return line

    def to_file(self,fname="bench.txt"):
        out_file = open(fname,"a")
        out_file.writelines(self.to_string())
        out_file.close()

def summarize_bench(in_file=None,out_file=None):
    """
    Read and summarize a benchmarking file.
    """
    if in_file == None:
        return
    task, tag, delta, start, stop = readcol(in_file,twod=False)

    dummy = os.popen("date")
    date_stamp = dummy.readlines()
    dummy = os.popen("uname -a")
    uname_stamp = dummy.readlines()
    dummy = os.popen("pwd")
    pwd_stamp = dummy.readline()

    lines = []
    lines.append("Summary of file "+in_file+"\n")
    lines.append(date_stamp[0]+"\n")
    lines.append(uname_stamp[0]+"\n")
    lines.append(pwd_stamp+"\n")
    lines.append("\n")
    total_time = np.max(stop) - np.min(start)
    total_time_hr = total_time / 3600.0
    lines.append("Total time: "+str(total_time)+" ("+str(total_time_hr)+" hr)\n")
    time_logged = np.sum(delta)
    lines.append("Time inside logged tasks: "+str(time_logged)+"\n")
    lines.append("Time outside logged tasks: "+str(total_time-time_logged)+"\n")
    lines.append("Total logged calls: "+str(len(task))+"\n")
    lines.append("Average time per call: "+str(np.mean(delta))+"\n")

    lines.append("\n")

    tasks_called = np.unique(task)
    n_calls = {}
    t_per_call = {}
    tot_t = {}

    for this_task in tasks_called:
        t_per_call[this_task] = np.mean(delta[task == this_task])
        tot_t[this_task] = np.sum(delta[task == this_task])
        n_calls[this_task] = np.sum(task == this_task)

    tot_t_vec = np.zeros_like(tasks_called)
    for i in range(len(tasks_called)):
        tot_t_vec[i] = tot_t[tasks_called[i]]
    order = np.argsort(tot_t_vec)
    tasks_called = tasks_called[order]

    for this_task in tasks_called:
        lines.append(this_task+" "+str(n_calls[this_task])+ \
                         " "+str(t_per_call[this_task])+ \
                         " "+str(tot_t[this_task])+"\n")
    if out_file == None:
        for line in lines:
            print line
    else:
        f = open(out_file,"w")
        f.writelines(lines)
        f.close()
