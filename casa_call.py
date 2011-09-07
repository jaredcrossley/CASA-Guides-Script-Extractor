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

    lines = []
    lines.append("Summary of file "+in_file)
    total_time = np.max(stop) - np.min(start)
    lines.append("Total time: "+str(total_time))
    time_logged = np.sum(delta)
    lines.append("Time inside logged tasks: "+str(time_logged))
    lines.append("Time outside logged tasks: "+str(total_time-time_logged))
    lines.append("Total logged calls: "+str(len(task)))
    lines.append("Average time per call: "+str(np.mean(delta)))
    tasks_called = np.unique(task)
    for this_task in tasks_called:
        mean_time = np.mean(delta[task == this_task])
        lines.append(this_task+" "+str(mean_time))
    if out_file == None:
        for line in lines:
            print line

