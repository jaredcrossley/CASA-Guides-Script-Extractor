import os
import sys
import socket
import platform
import numpy as np #this is a big import for three functions... :(
import copy

#import non-standard Python modules
import benchmark
import parameters

#-I need to figure out if the downloading and untarring is something that we want
# to be timing. If not then I can make it so the loop only downloads (and
# untars?) things once rather than for each benchmark.
#-need to decide where to save the machine information (e.g. txt file somewhere)
#-the sharing and passing around of variables is really a mess between the
# benchmark and machine classes right now
#-need to include check for trying to use dataURL when it is set to None in the
# parameters dictionary
#-need to check that running version of CASA matches the data set name given
#-could shorten up lines that use the jobs dict by defining variables local to
# the particular method for the parts needed e.g. look under runBenchmarks in
# the for loop that actually runs the benchmarks
#-need to change class docstring to standard Python style so information isn't
# redundant but I also still have a record of all the included attributes and
# methods
#-change docstrings to prescribe the function or method's effect as a command
# ("Do this", "Return that"), not as a description; e.g. don't write "Returns
# the pathname ...", instead write "Return the pathname..."

def makeReport(files):
    """ Gather total times and caluclate the mean and standard deviation from
    casa_call.summarize_bench output (.summary files).

    Parameters
    ----------
    files : list (of str)
       List of strings specifying the absolute paths to .summary files from
       benchmarking to gather total times from.

    Returns
    -------
    Tuple containing (average, standard deviation, list of all total times)

    Notes
    -----
    This simply loops over the list in files, searches each for a line starting
    with 'Total time: ' and grabs the total time from that line. From those times
    the average and standard deviation are computed.
    """
    times = np.empty(len(files))
    for i,f in enumerate(files):
        fileObj = open(f)
        for line in fileObj.readlines():
            if line[0:12] == 'Total time: ':
                time = line.split(' ')
                time = time[2]
                time = float(time)
                times[i] = time
                break
        fileObj.close()
    avg = times.mean()
    std = times.std()
    return (avg, std, times)


class machine:
    """ A class associated with a single computer and all of
    the benchmarking done on it.

    Parameters
    ----------

    CASAglobals : dict
        Dictionary returned by Python globals() function within the CASA
        namespace (environment). Simply pass the return value of the globals()
        function from within CASA where this class should be instantiated
        within.

    scriptDir : str
        Absolute path to directory containing the benchmarking module files.

    dataSets : list
        List of strings containing names of data sets to be benchmarked. Names
        must match the dictionary variable names in parameters.py.

    nIters : list
        List of integers specifying how many times each data set should be run
        through benchmarking. These are matched to the data set in the same
        position in the dataSets list.

    skipDownloads : list
        List of booleans specifying if the raw data download step should be
        skipped or not. False means download the data from the URL provided in
        parameters.py variable. These are matched to the data set in the same
        position in the dataSets list.

    steps : list
        List of strings specifying which stage (calibration, imaging or both)
        each set of iterations should run. Accepted values are 'cal', 'im' or
        'both'.

    workDir : str
        Absolute path to directory where all benchmarking will run. A separate
        directory for each data set will be created here and each benchmark
        iteration will be contained in a dedicated directory below that. Defaults
        to current directory.

    Attributes
    ----------

    CASAglobals : dict
        Dictionary returned by Python globals() function within the CASA
        namespace (environment). Simply pass the return value of the globals()
        function from within CASA where this class should be instantiated
        within.

    dataSets : list
        List of strings containing names of data sets to be benchmarked. Names
        must match the dictionary variable names in parameters.py.

    jobs: dict
        Container for each benchmark instance to be run on this machine along
        with information on whether to download the raw data, the number of
        benchmarking iterations desired and which step(s) (cal, im or both) to
        run.

    workDir : str
        Absolute path to directory where all benchmarking will run. A separate
        directory for each data set will be created here and each benchmark
        iteration will be contained in a dedicated directory below that.

        hostName : str
        Name of the computer this class is associated with.

    os : str
        Description of underlying platform associated to hostName.

    lustreAccess : bool
        Determines whether this computer has access to the /lustre/naasc/
        filesystem (it is hard-coded to simply check for the existence of that
        directory).

    pythonVersion : str
        major.minor.patchlevel version number for currently running Python.

    casaVersion : str
        Version number for currently running CASA.

    casaRevision : str
        Revision number for currently running CASA.
    """
    def __init__(self, CASAglobals=None, scriptDir='', dataSets=list(), \
                 nIters=list(), skipDownloads=list(), steps=list(), \
                 workDir='./'):
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::__init__'
        indent = len(fullFuncName) + 2

        #check that we have CASA globals
        if not CASAglobals:
            raise ValueError('Value returned by globals() function in ' + \
                             'CASA environment must be given.')
        self.CASAglobals = CASAglobals

        #add script directory to Python path if need be
        if scriptDir == '':
            raise ValueError('Path to benchmarking scripts must be given.')
        scriptDir = os.path.abspath(scriptDir) + '/'
        self.scriptDir = scriptDir
        if scriptDir not in sys.path:
            sys.path.append(self.scriptDir)

        #store info about which data sets will be benchmarked
        if len(dataSets) == 0:
            raise ValueError('At least one data set must be specified for ' + \
                             'benchmarking.')
        for dataSet in dataSets:
            if not hasattr(parameters, dataSet):
                raise ValueError("Data set name '" + dataSet + \
                                 "' not recognized.")
        self.dataSets = dataSets
        if len(steps) == 0:
            steps = ['both']*len(self.dataSets)
        self.jobs = dict()
        for dataSet in self.dataSets:
            self.jobs[dataSet] = dict()
            self.jobs[dataSet]['benchmarks'] = list()
        if len(nIters) != len(self.dataSets):
            raise ValueError('nIters integer list must be of same length ' + \
                             'as dataSets list.')
        if len(skipDownloads) != len(self.dataSets):
            raise ValueError('skipDownloads boolean list must be of same ' + \
                             'length as dataSets list.')
        if len(steps) != len(self.dataSets):
            raise ValueError('steps string list must be of same length as ' + \
                             'dataSets list.')
        for i,dataSet in enumerate(self.dataSets):
            if type(nIters[i]) != int:
                raise TypeError('nIters must be a list of all integers.')
            if type(skipDownloads[i]) != bool:
                raise TypeError('skipDownloads must be a list of all booleans.')
            if steps[i] != 'cal' and steps[i] != 'im' and steps[i] != 'both':
                raise ValueError('Elements in steps must be either "cal", ' + \
                                 '"im" or "both".')
            self.jobs[dataSet]['nIters'] = nIters[i]
            self.jobs[dataSet]['skipDownload'] = skipDownloads[i]
            self.jobs[dataSet]['step'] = steps[i]

        #initialize the working directory
        if not os.path.isdir(workDir):
            raise ValueError("Working directory '" + workDir + "' " + \
                             'does not exist.')
        if workDir == './': workDir = os.getcwd()
        if workDir[-1] != '/': workDir += '/'
        if workDir[0] != '/':
            raise ValueError('Working directory must be specified as an ' + \
                             'absolute path.')
        self.workDir = workDir

        #gather details of computer and installed packages
        self.hostName = socket.gethostname()
        self.os = platform.platform()
        self.lustreAccess = os.path.isdir('/lustre/naasc/')
        self.pythonVersion = platform.python_version()
        self.casaVersion = self.CASAglobals['casadef'].casa_version
        self.casaRevision = self.CASAglobals['casadef'].subversion_revision


    def runBenchmarks(self, cleanUp=False):
        """ Runs all necessary benchmark class methods for each data set the
        specified number of iterations.

        Parameters
        ----------
        cleanUp : bool
           Determine whether benchmark::removeCurrentRedDir is run at the end of
           each benchmark to conserve disk space. Defaults to False (do not
           remove reduction directory).

        Returns
        -------
        None

        Notes
        -----
        This iterates over each data set setup for benchmarking for the
        associated number of iterations. For each iteration it instantiaes a
        dedicated benchmark object and stores it in the jobs attribute. benchmark
        class methods run are benchmark, createDirTree, downloadData (optional),
        extractData, doScriptExtraction, useOtherBmarkScripts (optional),
        runGuideScript and removeCurrentRedDir (optional). It makes the data set
        directories if they are not already present. It also tries to only do
        the data extraction once:
          -does the extraction on the first iteration
          -if the previous benchmark was successful the next iteration runs
           useOtherBmarkScripts on the previous benchmark instance
          -if the previous failed then it does the extraction on the next like
           normal
        """
        #for telling where printed messages originate from
        fullFuncName = __name__ + '::runBenchmarks'
        indent = len(fullFuncName) + 2

        #setup and run each data set the specified number of iterations
        for dataSet in self.dataSets:
            #setup data set directory
            dataSetDir = self.workDir + dataSet + '-' + self.hostName + '/'
            if not os.path.isdir(dataSetDir):
                os.mkdir(dataSetDir)
            params = getattr(parameters, dataSet)

            #determine source of raw data
            if self.jobs[dataSet]['skipDownload']:
                uncalDataPath = params['uncalDataPath']
                calDataPath = params['calDataPath']
            else:
                uncalDataPath = params['uncalDataURL']
                calDataPath = params['calDataURL']

            #actually run the benchmarks
            for i in range(self.jobs[dataSet]['nIters']):
                b = benchmark.benchmark(scriptDir=self.scriptDir, \
                                 workDir=dataSetDir, \
                                 execStep=self.jobs[dataSet]['step'], \
                                 calSource=params['calibrationURL'], \
                                 imSource=params['imagingURL'], \
                                 uncalDataPath=uncalDataPath, \
                                 calDataPath=calDataPath, \
                                 skipDownload=self.jobs[dataSet]['skipDownload'])
                self.jobs[dataSet]['benchmarks'].append(b)

                b.createDirTree()

                if not self.jobs[dataSet]['skipDownload']:
                    b.downloadData()
                b.extractData()

                #try to only extract scripts once
                if self.jobs[dataSet]['benchmarks'][i-1].status == 'normal' and \
                   i != 0:
                    b.useOtherBmarkScripts(self.jobs[dataSet]['benchmarks'][i-1])
                else:
                    b.doScriptExtraction()
                if b.status == 'failure': continue

                b.runGuideScripts(CASAglobals=self.CASAglobals)

                if cleanUp:
                    b.emptyCurrentRedDir()
